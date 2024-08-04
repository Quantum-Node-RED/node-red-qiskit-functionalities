const component = require("../../component.js");

module.exports = function (RED) {
  function Quantum_Circuit_EndNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    // State object to track qubits
    const state = {
      qubits: [],
      expectedQubits: 0, // Set to 0 initially to indicate it should be retrieved dynamically
      receivedQubits: 0
    };

    node.on("input", function (msg) {
      // Retrieve the number of expected qubits from flow context if not already set
      if (state.expectedQubits === 0) {
        state.expectedQubits = node.context().flow.get("expectedQubits") || 1; // Default to 1 if not set
      }

      // Extract the qubit and its gates from the message
      const currentStructure = msg.payload.structure;
      const qubitNode = currentStructure.find((node) => node.name === "qbit");

      // // Add the qubit to the temporary state
      // qubitNode.parameters["id"] = state.receivedQubits;
      state.qubits.push(qubitNode);
      state.receivedQubits++;


      // Check if all expected qubits have been received
      if (state.receivedQubits === state.expectedQubits) {
        const output = [];
        //Add root compoenent to the structure output
        output.push(
          currentStructure.find((node) => node.name === "root")
        );
        // Add Quantum_Circuit_Begin component to the structure output
        output.push(
          currentStructure.find((node) => node.name === "Quantum_Circuit_Begin")
        );

        // Push each qubit in state qubits to output
        state.qubits.forEach((qubit) => {
          output.push(qubit);
        });

        // Add the Quantum_Circuit_End component
        const Quantum_Circuit_End_component = new component.Component(
          "Quantum_Circuit_End",
          {}
        );

        output.push(Quantum_Circuit_End_component);
        msg.payload.currentNode = Quantum_Circuit_End_component;
        msg.payload.no_of_components = msg.payload.no_of_components + 1;

        msg.payload.structure = output;

        // Send the aggregated message
        node.send(msg);

        // Reset state for next aggregation
        state.qubits = [];
        state.receivedQubits = 0;
        state.expectedQubits = 0; 
        node.context().flow.set("expectedQubits", undefined);
        node.context().flow.set("expectedQubits",undefined);
        node.context().flow.set("circuit_name",undefined);
      }
    });
  }

  RED.nodes.registerType("Quantum_Circuit_End", Quantum_Circuit_EndNode);
};
