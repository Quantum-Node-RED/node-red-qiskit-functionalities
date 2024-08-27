const component = require("../../component.js");
const constants = require("../../constants.js");

module.exports = function (RED) {
  function qubitNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      msg.payload = msg.payload || {};

      // Access the flow context to get the current value of expectedQubits
      let expectedQubits = node.context().flow.get(constants.EXPECTED_QUBITS);
      if (expectedQubits === null || expectedQubits === undefined) {
        expectedQubits = 0; // Ensure it's initialized
      }

      // Add the qubit component as a child
      const qubit_component = new component.Component(
        constants.QUBITS_COMPONENT_NAME,
        {}
      );
      qubit_component.parameters["id"] = expectedQubits;

      // Get the name of the circuit from Quantum Circuit Begin component
      qubit_component.parameters[constants.CIRCUIT_NAME] = node
        .context()
        .flow.get(constants.CIRCUIT_NAME);
      msg.payload["qubit_id"] = qubit_component.parameters["id"];

      component.addComponent(msg, qubit_component);

      // Increment the number of expected qubits
      expectedQubits += 1;

      // Update the flow context with the new value
      node.context().flow.set(constants.EXPECTED_QUBITS, expectedQubits);

      // Send the message onward
      node.send(msg);
    });
  }

  RED.nodes.registerType("qubit", qubitNode);
};
