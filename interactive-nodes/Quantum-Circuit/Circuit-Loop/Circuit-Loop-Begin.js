const component = require("../../component.js");
const constants = require("../../constants.js");
module.exports = function (RED) {
  function Circuit_Loop_Begin_Node(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      //Keeps track of number of qubits being used inside the Circuit Loop
      node.context().flow.get("loop_expected_qubit", 0);
      //Keeps track of number of qubits being used inside the Circuit (not the loop)
      //Beginning of the Circuit Loop may or may not have qubits before it
      //Case 1: QC_Begin > CL_Begin > Qubit > CL_End > QC_End 
      //Case 2: QC_Begin > Qubit > CL_Begin > CL_End > QC_End 
      //Case 3: QC_Begin > CL_Begin > CL_End > Qubit > QC_End 
      //Case 4: Qc_Begin > Qubit > CL_Begin > Qubit > CL_End > QC_End 
      //Case 5: QC_Begin > CL_Begin > Qubit > CL_End > Qubit > QC_End  
      //Case 6: Qc_Begin > Qubit > CL_Begin > CL_End > Qubit > QC_End 
      //Case 7: Qc_Begin > Qubit > CL_Begin > Qubit > CL_End > Qubit > QC_End 
      //Case 8: QC_Begin > CL_Begin > CL_End > QC_End 
      
      currentNode=msg.payload.currentNode;
      const circuit_name = node.context().flow.get(constants.CIRCUIT_NAME);
      const connectedPaths = node._wireCount || 0;
      const expectedQubits = node.context().flow.get("expectedQubits");
      const iterations=parseInt(config.iterations || 0);

      // TODO: Circuit_Loop and Quantum_Circuit components have same
      // logic to aggregate paths, with some differences in reference component name 
      // from where to aggregate paths. Thus needs a function to be reused.

      //If the current node is a qubit or a gate,you need to aggreate the paths (Case 2,Case 4,Case 6,Case 7)
      if (currentNode.name==constants.QUBITS_COMPONENT_NAME || /_gate$/.test(currentNode.name)){
        aggregatePath(expectedQubits,circuit_name,connectedPaths,node,msg,iterations);
        node.context().flow.set("has_circuit_loop",true);
      }
      
      // If the current node is Quantum Circuit Begin, there are no paths to aggregate (Case 1,Case 3,Case 5)
      // Circuit loop set up is done
      else if (currentNode.name==constants.QUANTUM_CIRCUIT_BEGIN_COMPONENT_NAME){
        node.context().flow.set(constants.EXPECTED_QUBITS, 0);
        if (msg.payload && msg.payload.structure) {
          for (let i = 0; i < msg.payload.structure.length; i++) {
              if (msg.payload.structure[i].name === constants.QUANTUM_CIRCUIT_BEGIN_COMPONENT_NAME) {
                  msg.payload.structure[i].parameters.num_qbits = connectedPaths; 
                  msg.payload.structure[i].parameters.num_cbits = connectedPaths;
                  break;
              }
          }
      }
        const Circuit_Loop_Begin_component = new component.Component(
          constants.CIRCUIT_LOOP_BEGIN_COMPONENT_NAME,
          { circuit_name: circuit_name,
            num_qbits: connectedPaths,
            iterations:iterations
          }
        );
        component.addComponent(msg, Circuit_Loop_Begin_component);
        node.context().flow.set("has_circuit_loop",true);
        node.send(msg);
      }

    });
  }
    
  RED.nodes.registerType("Circuit_Loop_Begin", Circuit_Loop_Begin_Node);
};


function aggregatePath(expectedQubits,circuit_name,connectedPaths,node,msg,iterations){
  if (expectedQubits === null || expectedQubits === undefined) {
    node.error(
      "expectedQubits not initialized. Ensure Quantum_Circuit_Begin node is setting this correctly."
    );
    return;
  }

  // Retrieve or initialize the current execution state
  let state = node.context().flow.get("executionState") || {
    receivedQubits: 0,
    structure: []
  };

  if (state.receivedQubits === 0) {
    // This is the first qubit received in this execution
    node.log("Starting path aggregation for Circuit Loop (components before Circuit_Loop_Begin).");
    node.log(`Expected qubits initialized to ${expectedQubits}`);
    state.structure = []; // Reset the structure for a new execution
  }

  

  // First Path Logic
  // Push all the components until the Quantum_Circuit_Begin component is seen
  if (state.receivedQubits === 0) {
    for (let component_ of msg.payload.structure) {
      state.structure.push(component_);
      if (
        component_.name === constants.CIRCUIT_LOOP_BEGIN_COMPONENT_NAME &&
        component_.parameters.circuit_name === circuit_name
      ) {
        break;
      }
    }
  }

  // Last Path Logic
  // Push Components only after the Quantum_Circuit_Begin component is seen
  else if (state.receivedQubits === expectedQubits - 1) {
    let collecting = false;
    for (let component_ of msg.payload.structure) {
      if (
        component_.name === constants.QUANTUM_CIRCUIT_BEGIN_COMPONENT_NAME &&
        component_.parameters.circuit_name === circuit_name
      ) {
        collecting = true;
        continue;
      }
      if (collecting) {
        state.structure.push(component_);
      }
    }
    const Circuit_Loop_Begin_component = new component.Component(
      constants.CIRCUIT_LOOP_BEGIN_COMPONENT_NAME,
      { circuit_name: circuit_name ,
        num_qbits: connectedPaths,
        iterations:iterations
      }
    );
    state.structure.push(Circuit_Loop_Begin_component);

    let new_payload = {};
    new_payload.structure = state.structure;
    new_payload.currentNode = Circuit_Loop_Begin_component;
    msg.payload = new_payload;

    // set the expected qubits to 0, to set up for Circuit Loop
    node.context().flow.set(constants.EXPECTED_QUBITS, 0);
    // Here we are not resetting the circuit name as it is still begin used in the Quantum Circuit 
    node.context().flow.set("executionState", null); // Clear the execution state

    node.send(msg);

    return; // Exit after sending the last path
  }

  // Middle Qubit Logic
  // Push Components only after the Quantum_Circuit_Begin component is seen and until the Circuit Loop End component is seen
  else {
    let collecting = false;
    for (let component_ of msg.payload.structure) {
      if (
        component_.name === constants.QUANTUM_CIRCUIT_BEGIN_COMPONENT_NAME &&
        component_.parameters.circuit_name === circuit_name
      ) {
        collecting = true;
        continue;
      }
      if (collecting) {
        state.structure.push(component_);
      }
      if (
        component_.name === constants.CIRCUIT_LOOP_BEGIN_COMPONENT_NAME &&
        component_.parameters.circuit_name === circuit_name
      ) {
        break;
      }
    }
  }

  // Increment the received qubits counter and save the state
  state.receivedQubits += 1;
  node.context().flow.set("executionState", state);
}