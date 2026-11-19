# EIS KKA Python reference — amplitude/phase trajectory

The Python implementation is an independent numerical reference, not generated from Lean and not a proof.

Canonical conventions:
- Physical field: Re(E_phasor exp(+i omega t)).
- H(u) = A(u) exp(i phi(u)); A is field-amplitude transmission, not intensity.
- Phase is in radians and must be unwrapped over the finite-difference interval.
- kappa_A = d(phi)/d(ln A) = (d phi/du) / ((dA/du)/A).
- If intensity I is proportional to A², kappa_I = kappa_A/2.
- The trajectory is undefined at A=0 or where d(ln A)/du=0.

The finite-difference functions require caller-supplied amplitude and phase functions. They do not assume a foundry-specific EAM, SOI, MZI, SiN or TFLN transfer law.

For the reference MZI transfer H(u)=(1+exp(iu))/2, on 0<u<pi:
A(u)=cos(u/2), phi(u)=u/2, and kappa_A(u)=-cot(u/2).
This is one topology/reference example, not a universal MZI or KKA law.

The existing detector reference uses normalized dimensionless field envelopes. Its responsivity is therefore A per normalized-power unit unless the caller explicitly maps |E|² to watts, in which case the responsivity is A/W. The ideal 50:50 balanced output is signed and equals 2 R Re(a conj(b)); branch gains and offsets remain explicit.

Run from the repository root:
python -m unittest discover -s tests -v
