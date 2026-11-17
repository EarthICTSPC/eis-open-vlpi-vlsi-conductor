import Lean

/-!
# EIS-TIDY3D-LEAN-001 — Lean-owned SOI directional-coupler specification

All dimensions are integer nanometres at the formal/Python boundary.
Permittivities and all geometry values in the initial example are explicitly
ASSUMED and illustrative. They are not foundry PDK data or measured values.
-/

namespace EISKKA.Tidy3D

structure DirectionalCouplerSpec where
  specId : String
  wavelengthNm : Nat
  coreWidthNm : Nat
  coreHeightNm : Nat
  gapNm : Nat
  couplingLengthNm : Nat
  accessLengthNm : Nat
  boxThicknessNm : Nat
  substrateThicknessNm : Nat
  corePermittivity : String
  oxidePermittivity : String
  domainXNm : Nat
  domainYNm : Nat
  domainZNm : Nat
  domainCenterZNm : Int
  gridStepsPerWavelength : Nat
  wavelengthMinNm : Nat
  wavelengthMaxNm : Nat
  wavelengthSamples : Nat
  evidenceClass : String
  processStatus : String
  phasorConvention : String
  deriving Repr, Inhabited

def WellFormed (s : DirectionalCouplerSpec) : Prop :=
  s.wavelengthNm > 0 ∧
  s.coreWidthNm > 0 ∧
  s.coreHeightNm > 0 ∧
  s.gapNm > 0 ∧
  s.couplingLengthNm > 0 ∧
  s.accessLengthNm > 0 ∧
  s.boxThicknessNm > 0 ∧
  s.substrateThicknessNm > 0 ∧
  s.domainXNm > s.couplingLengthNm + 2 * s.accessLengthNm ∧
  s.domainYNm > 2 * (s.coreWidthNm + s.gapNm) ∧
  s.domainZNm > s.boxThicknessNm + s.substrateThicknessNm + s.coreHeightNm ∧
  s.gridStepsPerWavelength > 0 ∧
  s.wavelengthMinNm > 0 ∧
  s.wavelengthMaxNm > s.wavelengthMinNm ∧
  s.wavelengthSamples ≥ 2 ∧
  s.corePermittivity ≠ "" ∧
  s.oxidePermittivity ≠ "" ∧
  s.evidenceClass = "assumed" ∧
  s.phasorConvention = "exp(+i omega t)"

/--
A transparent teaching baseline for the first SOI directional coupler.
The silicon and oxide permittivities are approximate illustrative inputs.
The BOX and silicon substrate thicknesses are geometry placeholders.
-/
def illustrativeSOI : DirectionalCouplerSpec :=
  { specId := "EIS-SOI-DC-ILLUSTRATIVE-001"
    wavelengthNm := 1550
    coreWidthNm := 450
    coreHeightNm := 220
    gapNm := 200
    couplingLengthNm := 8000
    accessLengthNm := 4000
    boxThicknessNm := 2000
    substrateThicknessNm := 2000
    corePermittivity := "12.1104"
    oxidePermittivity := "2.085136"
    domainXNm := 18000
    domainYNm := 4500
    domainZNm := 6400
    domainCenterZNm := -1020
    gridStepsPerWavelength := 20
    wavelengthMinNm := 1500
    wavelengthMaxNm := 1600
    wavelengthSamples := 31
    evidenceClass := "assumed"
    processStatus := "illustrative_not_foundry_PDK"
    phasorConvention := "exp(+i omega t)" }

theorem illustrativeSOI_wellFormed : WellFormed illustrativeSOI := by
  decide

private def nfield (key : String) (value : Nat) : String × Json :=
  (key, Json.str (toString value))

/-- Machine-readable interchange contract. Physical quantities remain strings
so consumers must explicitly parse and convert units rather than guess. -/
def toJson (s : DirectionalCouplerSpec) : Json :=
  Json.mkObj
    [ ("schema_version", Json.str "0.1")
    , ("spec_id", Json.str s.specId)
    , nfield "wavelength_nm" s.wavelengthNm
    , nfield "core_width_nm" s.coreWidthNm
    , nfield "core_height_nm" s.coreHeightNm
    , nfield "gap_nm" s.gapNm
    , nfield "coupling_length_nm" s.couplingLengthNm
    , nfield "access_length_nm" s.accessLengthNm
    , nfield "box_thickness_nm" s.boxThicknessNm
    , nfield "substrate_thickness_nm" s.substrateThicknessNm
    , ("core_permittivity", Json.str s.corePermittivity)
    , ("oxide_permittivity", Json.str s.oxidePermittivity)
    , nfield "domain_x_nm" s.domainXNm
    , nfield "domain_y_nm" s.domainYNm
    , nfield "domain_z_nm" s.domainZNm
    , ("domain_center_z_nm", Json.str (toString s.domainCenterZNm))
    , nfield "grid_steps_per_wavelength" s.gridStepsPerWavelength
    , nfield "wavelength_min_nm" s.wavelengthMinNm
    , nfield "wavelength_max_nm" s.wavelengthMaxNm
    , nfield "wavelength_samples" s.wavelengthSamples
    , ("evidence_class", Json.str s.evidenceClass)
    , ("process_status", Json.str s.processStatus)
    , ("phasor_convention", Json.str s.phasorConvention)
    , ("geometry_authority", Json.str "EIS Lean4 specification")
    , ("solver_authority", Json.str "Flexcompute Tidy3D FDTD")
    , ("launch_policy", Json.str "explicit_user_action_required")
    ]

end EISKKA.Tidy3D
