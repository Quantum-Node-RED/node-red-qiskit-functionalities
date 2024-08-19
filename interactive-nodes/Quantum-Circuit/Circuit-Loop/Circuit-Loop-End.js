const component = require("../../component.js");
const constants = require("../../constants.js");
module.exports = function (RED) {
  function Circuit_Loop_End_Node(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      //TODO: Refactor the aggregating function 

      // Retrieve the number of expected qubits from flow context at the start of each new execution
      let expectedQubits = node.context().flow.get(constants.EXPECTED_QUBITS);
      let connectedPaths = node._wireCount || 0;
      let currentNode=msg.payload.currentNode;
      let circuit_name = node.context().flow.get(constants.CIRCUIT_NAME);
      if (expectedQubits === null || expectedQubits === undefined) {
        node.error(
          "expectedQubits not initialized. Ensure Circuit_Loop_Begin node is setting this correctly."
        );
        return;
      }

      if (currentNode.name=="Circuit_Loop_Begin")
      {
        const Circuit_Loop_End_component = new component.Component(
          constants.CIRCUIT_LOOP_END_COMPONENT_NAME,
          { circuit_name: circuit_name,
            num_qbits: connectedPaths
          }
        );
        component.addComponent(msg, Circuit_Loop_End_component);
        node.send(msg);
      }
      else{
        aggregatePaths(expectedQubits,circuit_name,connectedPaths,node,msg);
      }
      
     
    });
  }
    
  RED.nodes.registerType("Circuit_Loop_End", Circuit_Loop_End_Node);
};




function aggregatePaths(expectedQubits,circuit_name,connectedPaths,node,msg)
{
  // Retrieve or initialize the current execution state
  let state = node.context().flow.get("executionState") || {
    receivedQubits: 0,
    structure: []
  };

  if (state.receivedQubits === 0) {
    // This is the first qubit received in this execution
    node.log("Starting Circuit Loop  aggregation.");
    node.log(`Expected qubits initialized to ${expectedQubits}`);
    state.structure = []; // Reset the structure for a new execution
  }
  // First Qubit Logic
  // Push all the components until you see Circuit_Loop_End component
  if (state.receivedQubits === 0) {
    for (let component_ of msg.payload.structure) {
      state.structure.push(component_);
      if (
        component_.name === "Circuit_Loop_End" &&
        component_.parameters.circuit_name === circuit_name
      ) {
        break;
      }
    }
  }
  // Last Qubit Logic
  // Collect components after the Circuit_Loop_Begin component
  else if (state.receivedQubits === expectedQubits - 1) {
    let collecting = false;
    for (let component_ of msg.payload.structure) {
      if (component_.name==="hyper_parameters" || component_.name==="condition")
      {
        continue;
      }
      if (
        component_.name === "Circuit_Loop_Begin" &&
        component_.parameters.circuit_name === circuit_name
      ) {
        collecting = true;
        continue;
      }
      if (collecting) {
        state.structure.push(component_);
      }
    }
    const Circuit_Loop_End_component = new component.Component(
      "Circuit_Loop_End",
      { circuit_name: circuit_name,
        num_qbits: connectedPaths
      }
    );
    state.structure.push(Circuit_Loop_End_component);

    let new_payload = {};
    new_payload.structure = state.structure;
    new_payload.currentNode = Circuit_Loop_End_component;
    msg.payload = new_payload;

    // Reset flow context after completing the execution
    node.context().flow.set("expectedQubits", 0);
    // Circuit Name is not reset as it is still inside Qunaum Circuit
    node.context().flow.set("executionState", null); // Clear the execution state

    

    node.send(msg);

    return; // Exit after sending the last qubit
  }
  // Middle Qubit Logic
  else {
    let collecting = false;
    for (let component_ of msg.payload.structure) {
      if (component_.name==="hyper_parameters" || component_.name==="condition")
      {
        continue;
      }
      if (
        component_.name === "Circuit_Loop_Begin" &&
        component_.parameters.circuit_name === circuit_name
      ) {
        collecting = true;
        continue;
      }
      if (collecting) {
        state.structure.push(component_);
      }
      if (
        component_.name === "Circuit_Loop_End" &&
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