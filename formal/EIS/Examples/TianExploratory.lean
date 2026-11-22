import Lean
import EIS.Netlist

open Lean
open EIS

namespace EIS.Examples.TianExploratory

def param (name value unit : String) (evidence : EvidenceClass) : ParameterValue :=
  { name := name, value := value, unit := unit, evidence := evidence }

def port (instanceId portName : String) : PortRef :=
  { instanceId := instanceId, portName := portName }

def connect (a ap b bp : String) : OpticalConnection :=
  { source := port a ap, target := port b bp }

def suffix2 (n : Nat) : String :=
  if n < 10 then "0" ++ toString n else toString n

def channelId (prefix : String) (n : Nat) : String :=
  prefix ++ suffix2 n

def fanoutPorts : List String :=
  ["in"] ++ (List.range 10).map (fun i => "out_" ++ suffix2 (i + 1))

def mziParameters (role : String) (channel : String) : List ParameterValue :=
  [ param "phase_shifters" "3" "count" .tianReported
  , param "splitter" "mmi1x2" "component_kind" .tianReported
  , param "combiner" "mmi2x2" "component_kind" .tianReported
  , param "role" role "text" .sourceInterpretation
  , param "channel" channel "index" .sourceInterpretation
  , param "waveguide_width_nm" "450" "nm" .tianReported
  , param "waveguide_height_nm" "220" "nm" .tianReported
  , param "heater_material" "TiN" "text" .tianReported
  , param "heater_length_um" "200" "um" .tianReported
  , param "heater_width_um" "2" "um" .tianReported
  , param "heater_thickness_nm" "120" "nm" .tianReported
  , param "heater_sheet_resistance_ohm_sq" "12" "ohm/sq" .tianReported
  , param "mmi1x2_length_um" "unknown" "um" .sourceUnknown
  , param "mmi1x2_width_um" "unknown" "um" .sourceUnknown
  , param "mmi2x2_length_um" "unknown" "um" .sourceUnknown
  , param "mmi2x2_width_um" "unknown" "um" .sourceUnknown
  ]

def mziInstance (id role channel : String) : ComponentInstance :=
  { id := id
    kind := .mziCell
    ports := ["in", "out", "out_complement"]
    parameters := mziParameters role channel }

def fanoutInstance (id : String) : ComponentInstance :=
  { id := id
    kind := .fanoutTree
    ports := fanoutPorts
    parameters :=
      [ param "fanout" "10" "count" .eisArchitectureChoice
      , param "geometry_status" "logical_only" "text" .eisArchitectureChoice
      , param "physical_decomposition" "unknown" "text" .sourceUnknown
      ] }

def inputSplit : ComponentInstance :=
  { id := "input_split_mmi"
    kind := .mmi1x2
    ports := ["in", "out_a", "out_b"]
    parameters :=
      [ param "mmi1x2_length_um" "unknown" "um" .sourceUnknown
      , param "mmi1x2_width_um" "unknown" "um" .sourceUnknown
      ] }

def outputMmi (n : Nat) : ComponentInstance :=
  { id := channelId "output_mmi_" n
    kind := .mmi2x2
    ports := ["in_a", "in_b", "out", "out_complement"]
    parameters :=
      [ param "channel" (toString n) "index" .sourceInterpretation
      , param "mmi2x2_length_um" "unknown" "um" .sourceUnknown
      , param "mmi2x2_width_um" "unknown" "um" .sourceUnknown
      ] }

def detector (n : Nat) : ComponentInstance :=
  { id := channelId "BPD_" n
    kind := .balancedPhotodetector
    ports := ["optical_in", "electrical_out"]
    parameters := [param "channel" (toString n) "index" .sourceInterpretation] }

def channels : List Nat := (List.range 10).map (fun i => i + 1)

def instances : List ComponentInstance :=
  [ { id := "laser_in", kind := .laser, ports := ["out"] }
  , inputSplit
  , fanoutInstance "A_fanout_tree"
  , mziInstance "MZI_B_SHARED" "shared_B" "B"
  , fanoutInstance "B_broadcast_tree"
  ] ++
  channels.flatMap (fun n =>
    [ mziInstance (channelId "MZI_A_" n) "A" (toString n)
    , outputMmi n
    , detector n
    ])

def connections : List OpticalConnection :=
  [ connect "laser_in" "out" "input_split_mmi" "in"
  , connect "input_split_mmi" "out_a" "A_fanout_tree" "in"
  , connect "input_split_mmi" "out_b" "MZI_B_SHARED" "in"
  , connect "MZI_B_SHARED" "out" "B_broadcast_tree" "in"
  ] ++
  channels.flatMap (fun n =>
    let suffix := suffix2 n
    [ connect "A_fanout_tree" ("out_" ++ suffix) (channelId "MZI_A_" n) "in"
    , connect (channelId "MZI_A_" n) "out" (channelId "output_mmi_" n) "in_a"
    , connect "B_broadcast_tree" ("out_" ++ suffix) (channelId "output_mmi_" n) "in_b"
    , connect (channelId "output_mmi_" n) "out" (channelId "BPD_" n) "optical_in"
    ])

def tianExploratoryNetlist : Netlist :=
  { schemaVersion := 1
    name := "EIS_TIAN_INSPIRED_PTC_10_OUTPUT_EXPLORATORY"
    instances := instances
    connections := connections
    inputs := [port "laser_in" "out"]
    outputs := channels.map (fun n => port (channelId "BPD_" n) "electrical_out") }

#eval IO.println ("validateNetlist=" ++ toString (validateNetlist tianExploratoryNetlist))
#eval IO.println (Json.compress (toJson tianExploratoryNetlist))

end EIS.Examples.TianExploratory
