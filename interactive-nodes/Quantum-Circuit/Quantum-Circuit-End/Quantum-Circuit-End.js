const component = require("../../component.js");
const constants = require("../../constants.js");

module.exports = function (RED) {
  function Quantum_Circuit_EndNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      // Ensure payload structure exists
      msg.payload = msg.payload || {};
      // TODO: Refactor below to an aggregating function and reuse it in Circuit_Loop_End/Begin and Quantum_Circuit_End 
      
      // Retrieve the number of expected qubits/circuit name from flow context at the start of each path aggregation
      let expectedQubits = node.context().flow.get("expectedQubits");
      let circuit_name = node.context().flow.get(constants.CIRCUIT_NAME);


      if (expectedQubits === null || expectedQubits === undefined) {
        node.error(
          "expectedQubits not initialized. Ensure Quantum_Circuit_Begin node/Circuit_Loop_End node is setting this correctly."
        );
        return;
      }

      let currentNode = msg.payload.currentNode;
      if (currentNode.name=="Circuit_Loop_End"){
        // No need to aggregate paths at  Quantum_Circuit_End as only one path is expected 
        node.context().flow.set("expectedQubits", null);
        node.context().flow.set(constants.CIRCUIT_NAME, null);
        node.context().flow.set("executionState", null); 
        node.context().flow.set("has_circuit_loop", null);

        const Quantum_Circuit_End_component = new component.Component(
          constants.QUANTUM_CIRCUIT_END_COMPONENT_NAME,
          { circuit_name: circuit_name }
        );
        component.addComponent(msg, Quantum_Circuit_End_component);
        node.send(msg);
      }

      else{
        aggregatePath(expectedQubits,circuit_name,node,msg);
      }
    });
  }

  RED.nodes.registerType("Quantum_Circuit_End", Quantum_Circuit_EndNode);
};







function aggregatePath(expectedQubits,circuit_name,node,msg)
{
  node.log("Aggregating path for Quantum Circuit End");
  node.log(`has_circuit_loop: ${node.context().flow.get("has_circuit_loop")}`);
  // Retrieve or initialize the current execution state
  let has_circuit_loop = node.context().flow.get("has_circuit_loop");
  let state = node.context().flow.get("executionState") || {
    receivedQubits: 0,
    structure: []
  };

  if (state.receivedQubits === 0) {
    // This is the first qubit received in this execution
    node.log("Starting path aggregation for Quantum Circuits (between Quantum_Circuit_Begin and End).");
    node.log(`Expected qubits initialized to ${expectedQubits}`);
    state.structure = []; // Reset the structure for a new execution
  }

      

  // First Qubit Logic
  if (state.receivedQubits === 0) {
    for (let component_ of msg.payload.structure) {
      state.structure.push(component_);
      if (
        component_.name === "Quantum_Circuit_End" &&
            component_.parameters.circuit_name === circuit_name
      ) {
        break;
      }
    }
  }
  // Last Qubit Logic
  else if (state.receivedQubits === expectedQubits - 1) {
    let collecting = false;
    let has_circuit_loop = node.context().flow.get("has_circuit_loop");
    for (let component_ of msg.payload.structure) {
      if (
        !has_circuit_loop &&
        component_.name === constants.QUANTUM_CIRCUIT_BEGIN_COMPONENT_NAME &&
            component_.parameters.circuit_name === circuit_name
      ) {
        collecting = true;
        continue;
      }
      else if (
        has_circuit_loop && 
        component_.name === constants.CIRCUIT_LOOP_END_COMPONENT_NAME &&
        component_.parameters.circuit_name === circuit_name
      )
      {
        collecting=true;
        continue;
      }
      if (collecting) {
        state.structure.push(component_);
      }
    }
    const Quantum_Circuit_End_component = new component.Component(
      "Quantum_Circuit_End",
      { circuit_name: circuit_name }
    );
    state.structure.push(Quantum_Circuit_End_component);

    let new_payload = {};
    new_payload.structure = state.structure;
    new_payload.currentNode = Quantum_Circuit_End_component;
    msg.payload = new_payload;

    // Reset flow context after completing the execution
    node.context().flow.set("expectedQubits", null);
    node.context().flow.set(constants.CIRCUIT_NAME, null);
    node.context().flow.set("executionState", null);
    node.context().flow.set("has_circuit_loop", null);

    node.send(msg);

    return; // Exit after sending the last qubit
  }
  // Middle Qubit Logic
  else {
    let collecting = false;
    for (let component_ of msg.payload.structure) {
      if (
        !has_circuit_loop &&
            component_.name === constants.QUANTUM_CIRCUIT_BEGIN_COMPONENT_NAME &&
            component_.parameters.circuit_name === circuit_name 
      )
      {
        collecting = true;
        continue;
      }
      else if (has_circuit_loop && component_.name === constants.CIRCUIT_LOOP_END_COMPONENT_NAME
        && component_.parameters.circuit_name === circuit_name
      )
      {
        collecting=true;
        continue;
      }

      if (collecting) {
        state.structure.push(component_);
      }
      if (
        component_.name === constants.QUANTUM_CIRCUIT_END_COMPONENT_NAME &&
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