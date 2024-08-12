const component = require("../../component.js");
const constants = require("../../constants.js");

module.exports = function (RED) {
  function Quantum_Circuit_EndNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      // Ensure payload structure exists
      msg.payload = msg.payload || {};

      // Retrieve the number of expected qubits from flow context at the start of each new execution
      let expectedQubits = node.context().flow.get("expectedQubits");
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
        node.log("Starting new circuit execution.");
        node.log(`Expected qubits initialized to ${expectedQubits}`);
        state.structure = []; // Reset the structure for a new execution
      }

      let circuit_name = node.context().flow.get(constants.CIRCUIT_NAME);

      // Log the current state for debugging
      node.log(
        `Received qubits: ${state.receivedQubits}, Expected qubits: ${expectedQubits}`
      );

      // First Qubit Logic
      if (state.receivedQubits === 0) {
        node.log("First Qubit");
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
        node.log("Last Qubit");
        let collecting = false;
        for (let component_ of msg.payload.structure) {
          if (
            component_.name === "Quantum_Circuit_Begin" &&
            component_.parameters.circuit_name === circuit_name
          ) {
            collecting = true;
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
        node.context().flow.set("executionState", null); // Clear the execution state

        node.send(msg);

        return; // Exit after sending the last qubit
      }
      // Middle Qubit Logic
      else {
        node.log("Middle Qubit");
        let collecting = false;
        for (let component_ of msg.payload.structure) {
          if (
            component_.name === "Quantum_Circuit_Begin" &&
            component_.parameters.circuit_name === circuit_name
          ) {
            collecting = true;
            continue;
          }
          if (collecting) {
            state.structure.push(component_);
          }
          if (
            component_.name === "Quantum_Circuit_End" &&
            component_.parameters.circuit_name === circuit_name
          ) {
            break;
          }
        }
      }

      // Increment the received qubits counter and save the state
      state.receivedQubits += 1;
      node.context().flow.set("executionState", state);
    });
  }

  RED.nodes.registerType("Quantum_Circuit_End", Quantum_Circuit_EndNode);
};
