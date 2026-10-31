# EIS power-domain co-design: EIS-ADIA-IO-001 / EIS-MZI-EO-001 / EIS-COPOWER-001

**Status:** Draft formal contracts; Lean CI compilation pending. No device characterization or energy measurement is claimed.

## 1. Separate power domains

EIS treats the system as three coordinated physical domains:

1. **VLSI control:** reversible/adiabatic digital control and I/O, potentially powered by a multiphase trapezoidal power-clock.
2. **Electro-optic interface:** electrical phase/data modulation, with load-specific drive and return-path behavior.
3. **VLPI optical field:** optical energy supplied by a laser and transformed by optical structures; detector and readout form a separate measurement boundary.

The RISC-V ISA does not make a circuit adiabatic. A concrete controller must use a reversible/adiabatic implementation and preserve enough state/history for internal transitions to be invertible. External I/O commit is an explicit boundary with an audit record; it is not declared reversible.

## 2. Tian et al.: what the shared ground does and does not show

Tian et al., *Photonic transformer chip: interference is all you need*, PhotoniX 6, 45 (2025), report a silicon photonic chip with TiN resistive thermo-optic heaters. The methods section says each phase-shifter heater has an individual drive trace and that ground connections for phase shifters in a column are shared and connected to one ground pad.

This establishes a shared common electrical reference/current-return connection for the heater network. It does **not** establish regenerative energy recovery. In the reported heater implementation, electrical energy is intentionally dissipated as heat in the TiN resistor to change optical phase. A common ground conductor is not, by itself, a regenerative converter or a supply reservoir able to absorb returned charge.

The formal model records ground-pad presence separately from the return-path properties not reported by the paper: closed-loop connection to a regenerative supply, bidirectional driver capability, a sink able to absorb energy, and an energy-balance verification. Those fields are UNKNOWN rather than silently marked true or false. The device is classified as thermo-optic resistive. This is a fail-closed evidence classification, not a claim that the paper proves the ground circuit physically cannot be connected to a regenerative supply.

This is an evidence-bound reading of the reported implementation, not a claim that no future thermal-energy harvesting method could recover any fraction of heat. Such a method needs a separate thermal-energy model and measured evidence.

## 3. What counts as a return-to-supply path?

For a lumped capacitive EO phase shifter, an electrical recovery claim requires more than a ground pad. At minimum, the driver/load/supply loop needs:

- a closed, intentional return path;
- bidirectional current handling during discharge/recovery;
- a regenerative rail or resonant reservoir capable of accepting returned energy;
- timing/impedance compatibility with the modulator capacitance and series resistance;
- an energy-flow balance: gross supply draw = returned-to-supply energy + dissipated energy + energy retained at cycle end.

A shared ground conductor may be part of that loop. The conductor can carry return current, but only a demonstrated bidirectional driver and energy-absorbing supply/reservoir make the path regenerative. The ground connection alone is not the recovery element.

For an ideal lumped RC load under a linear voltage ramp:

\[
E_{\mathrm{ramp,loss}} = \frac{R C^2 (\Delta V)^2}{T_{\mathrm{ramp}}}.
\]

The Lean theorem records that, in this simple model, if T_ramp ≥ 2 R C, the loss in one ramp is no greater than stored capacitor energy C (ΔV)^2 / 2. This is an analytical model property, not measured device efficiency. The complete cycle must include both ramps, driver losses, parasitics, leakage, clock generation, and retained energy.

Terminated traveling-wave EO devices and thermo-optic heaters do not receive this capacitive energy-recovery credit by analogy. They need their own electrical and thermal models.

## 4. Contract boundaries

### EIS-ADIA-IO-001

- Full controller state includes registers, queues, and transaction history.
- Internal transition has explicit forward/backward functions with inverse laws.
- Forward steps do not discard existing transaction history.
- Trapezoidal power-clock has positive ramp/hold durations and a parameterized phase-rail count.
- Switch events obey turn-on-near-zero-voltage and turn-off-near-zero-current tolerances.
- Bus request/response/commit timestamps obey declared handshake order.
- External I/O commit is a separate boundary with an audit record binding request and pre-commit state.

This is not yet a transistor-level reversible RISC-V implementation or proof that physical switching is adiabatic.

### EIS-MZI-EO-001

- Identify the phase-shifter device class.
- Record effective capacitance, series resistance, voltage swing, rise/fall times, hold time, leakage, bandwidth, settling time, phase shift, and insertion loss.
- Identify the return topology explicitly.
- Distinguish ground/reference and dissipative termination from regenerative supply/resonant reservoir.
- Define gross draw, returned-to-supply energy, dissipation, and retained energy with a balance equation.
- Keep optical path energy separate from electrical driver energy.

The first RC ramp model applies only where the declared lumped-capacitor/series-resistance equivalent circuit is valid. The initial integrated contract requires a measured-hardware energy-balance grade before assigning a nonzero energy-return credit to the system ledger. Analytic and circuit-simulation evidence can inform design but do not count as measured recovery.

### EIS-COPOWER-001

- Bind controller and EO timing so phase settling precedes optical sampling and sampling occurs inside the controller hold window.
- Bind EO gross draw and returned energy to the system ledger.
- Keep laser wall-plug energy, optical launch energy, optical path loss, and detector/readout energy in separate domains.
- Count a recovery credit only once and never infer it from a shared ground alone.

## 5. Evidence and non-claims

Current status:
- **Specified:** abstract Lean contracts and theorem statements.
- **Analytically modeled:** ideal lumped RC linear-ramp loss equation and energy-ledger identities.
- **Not yet verified:** Lean compilation/CI for these new modules.
- **Not established:** EIS PDK phase-shifter equivalent circuit, actual supply/driver schematic, return-current path, measured recovery fraction, energy per accepted useful transformation, thermal behavior, or fabricated-device conformance.

No hardware claim of adiabatic operation, zero-energy switching, or measured recovery should be made until the selected device/driver/supply loop is characterized and energy balance is measured at a declared boundary.

## Source

Tian, Y., Xiang, S., Guo, X. et al. “Photonic transformer chip: interference is all you need.” *PhotoniX* 6, 45 (2025). https://doi.org/10.1186/s43074-025-00182-7
