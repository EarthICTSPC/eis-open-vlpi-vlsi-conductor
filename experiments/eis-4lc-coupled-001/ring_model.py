"""Reference RK4 model for the DeBenedictis four-node 4LC ring.

Parameter values must come from extraction or measurement for physical claims.
The unit tests use synthetic values only to check equations and numerical behavior.
"""
from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Callable, Sequence

V4 = tuple[float, float, float, float]
S8 = tuple[float, float, float, float, float, float, float, float]
Drive = Callable[[float], V4]


def _v4(xs: Sequence[float], name: str) -> V4:
    if len(xs) != 4:
        raise ValueError(f"{name} must have exactly four entries")
    return tuple(float(x) for x in xs)  # type: ignore[return-value]


@dataclass(frozen=True)
class RingParameters:
    # L[n], R[n] lie on edge Pn -> P(n+1 mod 4).
    inductance_h: V4
    branch_resistance_ohm: V4
    # Resonator shunt C[n] and first-order EO load-to-ground equivalent.
    shunt_capacitance_f: V4
    eo_load_capacitance_f: V4
    eo_load_conductance_s: V4

    @classmethod
    def from_sequences(cls, inductance_h: Sequence[float],
                       branch_resistance_ohm: Sequence[float],
                       shunt_capacitance_f: Sequence[float],
                       eo_load_capacitance_f: Sequence[float] = (0, 0, 0, 0),
                       eo_load_conductance_s: Sequence[float] = (0, 0, 0, 0)):
        obj = cls(_v4(inductance_h, "inductance_h"),
                  _v4(branch_resistance_ohm, "branch_resistance_ohm"),
                  _v4(shunt_capacitance_f, "shunt_capacitance_f"),
                  _v4(eo_load_capacitance_f, "eo_load_capacitance_f"),
                  _v4(eo_load_conductance_s, "eo_load_conductance_s"))
        obj.validate()
        return obj

    def validate(self):
        for n, x in enumerate(self.inductance_h):
            if not math.isfinite(x) or x <= 0:
                raise ValueError(f"L{n} must be finite and > 0")
        for n, x in enumerate(self.shunt_capacitance_f):
            if not math.isfinite(x) or x <= 0:
                raise ValueError(f"C{n} must be finite and > 0")
        for name, xs in (("R", self.branch_resistance_ohm),
                         ("C_load", self.eo_load_capacitance_f),
                         ("G_load", self.eo_load_conductance_s)):
            for n, x in enumerate(xs):
                if not math.isfinite(x) or x < 0:
                    raise ValueError(f"{name}[{n}] must be finite and >= 0")

    @property
    def total_node_capacitance_f(self) -> V4:
        return tuple(self.shunt_capacitance_f[n] + self.eo_load_capacitance_f[n]
                     for n in range(4))  # type: ignore[return-value]


@dataclass(frozen=True)
class Sample:
    time_s: float
    state: S8
    stored_energy_j: float
    input_power_w: float
    dissipated_power_w: float


def ring_laplacian(v: V4) -> V4:
    """Laplacian for the actual cycle graph P0-P1-P2-P3-P0."""
    return (2*v[0]-v[1]-v[3], 2*v[1]-v[2]-v[0],
            2*v[2]-v[3]-v[1], 2*v[3]-v[0]-v[2])


def ideal_modes() -> dict[str, tuple[V4, float]]:
    return {
        "common": ((1, 1, 1, 1), 0),
        "quadrature_cos": ((1, 0, -1, 0), 2),
        "quadrature_sin": ((0, 1, 0, -1), 2),
        "alternating": ((1, -1, 1, -1), 4),
    }


def ideal_quadrature_frequency_hz(L_h: float, C_total_f: float) -> float:
    if L_h <= 0 or C_total_f <= 0:
        raise ValueError("L and C must be positive")
    return math.sqrt(2/(L_h*C_total_f))/(2*math.pi)


def derivative(p: RingParameters, s: S8, u: V4) -> S8:
    """KCL: Ctot[n] Vdot[n]=u[n]-(i[n]-i[n-1])-G[n]V[n].
    KVL: L[n] idot[n]=V[n]-V[n+1]-R[n]i[n].
    """
    v, i = s[:4], s[4:]
    ctot = p.total_node_capacitance_f
    dv, di = [], []
    for n in range(4):
        prev, nxt = (n-1) % 4, (n+1) % 4
        dv.append((u[n] - (i[n]-i[prev]) -
                   p.eo_load_conductance_s[n]*v[n])/ctot[n])
        di.append((v[n]-v[nxt] -
                   p.branch_resistance_ohm[n]*i[n])/p.inductance_h[n])
    return tuple(dv+di)  # type: ignore[return-value]


def stored_energy_j(p: RingParameters, s: S8) -> float:
    v, i = s[:4], s[4:]
    c = p.total_node_capacitance_f
    return (sum(0.5*c[n]*v[n]**2 for n in range(4)) +
            sum(0.5*p.inductance_h[n]*i[n]**2 for n in range(4)))


def input_power_w(s: S8, u: V4) -> float:
    return sum(s[n]*u[n] for n in range(4))


def dissipated_power_w(p: RingParameters, s: S8) -> float:
    v, i = s[:4], s[4:]
    return (sum(p.branch_resistance_ohm[n]*i[n]**2 for n in range(4)) +
            sum(p.eo_load_conductance_s[n]*v[n]**2 for n in range(4)))


def energy_rate_w(p: RingParameters, s: S8, ds: S8) -> float:
    v, i, dv, di = s[:4], s[4:], ds[:4], ds[4:]
    c = p.total_node_capacitance_f
    return (sum(c[n]*v[n]*dv[n] for n in range(4)) +
            sum(p.inductance_h[n]*i[n]*di[n] for n in range(4)))


def _axpy(a: S8, b: S8, k: float) -> S8:
    return tuple(a[n]+k*b[n] for n in range(8))  # type: ignore[return-value]


def rk4_step(p: RingParameters, s: S8, t: float, h: float, drive: Drive) -> S8:
    if not math.isfinite(h) or h <= 0:
        raise ValueError("time step must be finite and positive")
    k1 = derivative(p, s, drive(t))
    k2 = derivative(p, _axpy(s, k1, h/2), drive(t+h/2))
    k3 = derivative(p, _axpy(s, k2, h/2), drive(t+h/2))
    k4 = derivative(p, _axpy(s, k3, h), drive(t+h))
    return tuple(s[n]+h*(k1[n]+2*k2[n]+2*k3[n]+k4[n])/6
                 for n in range(8))  # type: ignore[return-value]


def simulate(p: RingParameters, initial: S8, duration_s: float, dt_s: float,
             drive: Drive | None = None, sample_every: int = 1) -> list[Sample]:
    """Time-domain RK4 reference; not an EM/PDK simulator."""
    if not math.isfinite(duration_s) or duration_s <= 0:
        raise ValueError("duration must be finite and positive")
    if sample_every < 1:
        raise ValueError("sample_every must be >= 1")
    ufn = drive or (lambda _t: (0.0, 0.0, 0.0, 0.0))
    steps = math.ceil(duration_s/dt_s)
    s, t, result = initial, 0.0, []
    for k in range(steps+1):
        u = ufn(t)
        if k % sample_every == 0 or k == steps:
            result.append(Sample(t, s, stored_energy_j(p, s),
                                 input_power_w(s, u), dissipated_power_w(p, s)))
        if k == steps:
            break
        h = min(dt_s, duration_s-t)
        s = rk4_step(p, s, t, h, ufn)
        t += h
    return result


def voltage_mode_projection(v: V4) -> dict[str, float]:
    """Coordinates of node voltage in the four ideal basis vectors, not modal energy."""
    result = {}
    for name, (basis, _lam) in ideal_modes().items():
        norm2 = sum(x*x for x in basis)
        result[name] = sum(v[n]*basis[n] for n in range(4))/norm2
    return result


def assert_matched_eo_load(room_temp: RingParameters, hki: RingParameters,
                           tolerance: float = 0.0) -> None:
    """Reject candidate comparisons that quietly change the EO load."""
    for field in ("eo_load_capacitance_f", "eo_load_conductance_s"):
        a, b = getattr(room_temp, field), getattr(hki, field)
        if any(abs(a[n]-b[n]) > tolerance for n in range(4)):
            raise ValueError(f"candidate EO loads differ in {field}")
