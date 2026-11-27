import Lean

open Lean

namespace EIS

inductive ComponentKind where
  | laser
  | mmi1x2
  | mmi2x2
  | fanoutTree
  | mziCell
  | balancedPhotodetector
  deriving Repr, BEq, DecidableEq, Inhabited, ToJson, FromJson

inductive EvidenceClass where
  | tianReported
  | sourceInterpretation
  | eisArchitectureChoice
  | sourceUnknown
  | eisAssumed
  | simulated
  deriving Repr, BEq, DecidableEq, Inhabited, ToJson, FromJson

structure ParameterValue where
  name : String
  value : String
  unit : String
  evidence : EvidenceClass
  deriving Repr, Inhabited, ToJson, FromJson

structure PortRef where
  instanceId : String
  portName : String
  deriving Repr, BEq, DecidableEq, Inhabited, ToJson, FromJson

structure ComponentInstance where
  id : String
  kind : ComponentKind
  ports : List String
  parameters : List ParameterValue := []
  deriving Repr, Inhabited, ToJson, FromJson

structure OpticalConnection where
  source : PortRef
  target : PortRef
  deriving Repr, Inhabited, ToJson, FromJson

structure Netlist where
  schemaVersion : Nat := 1
  name : String
  instances : List ComponentInstance
  connections : List OpticalConnection
  inputs : List PortRef
  outputs : List PortRef
  deriving Repr, Inhabited, ToJson, FromJson

def hasPort (n : Netlist) (p : PortRef) : Bool :=
  n.instances.any (fun inst =>
    inst.id == p.instanceId && inst.ports.contains p.portName)

def instanceIdsUnique (n : Netlist) : Bool :=
  (n.instances.map (·.id)).length ==
    ((n.instances.map (·.id)).eraseDups).length

def endpoints (c : OpticalConnection) : List PortRef :=
  [c.source, c.target]

def connectionEndpointsExist (n : Netlist) : Bool :=
  n.connections.all (fun c => hasPort n c.source && hasPort n c.target)

def boundaryPortsExist (n : Netlist) : Bool :=
  n.inputs.all (hasPort n) && n.outputs.all (hasPort n)

def noSelfConnections (n : Netlist) : Bool :=
  n.connections.all (fun c => c.source != c.target)

def noRepeatedConnectionEndpoint (n : Netlist) : Bool :=
  let used := n.connections.flatMap endpoints
  used.length == used.eraseDups.length

def boundaryPortsDisjoint (n : Netlist) : Bool :=
  let boundary := n.inputs ++ n.outputs
  boundary.length == boundary.eraseDups.length

def validateNetlist (n : Netlist) : Bool :=
  n.schemaVersion == 1 &&
  instanceIdsUnique n &&
  connectionEndpointsExist n &&
  boundaryPortsExist n &&
  noSelfConnections n &&
  noRepeatedConnectionEndpoint n &&
  boundaryPortsDisjoint n

end EIS
