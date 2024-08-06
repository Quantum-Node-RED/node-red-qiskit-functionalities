const component = require("../../component.js");
const constants = require("../../constants.js");

module.exports = function (RED) {
  function qbitNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      msg.payload = msg.payload || {};

      // Access the flow context to get the current value of expectedQubits
      let expectedQubits = node.context().flow.get(constants.EXPECTED_QUBITS);
      if (expectedQubits === null || expectedQubits === undefined) {
        expectedQubits = 0; // Ensure it's initialized
      }

      // Add the qbit component as a child
      const qbit_component = new component.Component(
        constants.QUBITS_COMPONENT_NAME,
        {}
      );
      qbit_component.parameters["id"] = expectedQubits;

      // Get the name of the circuit from Quantum Circuit Begin component
      qbit_component.parameters[constants.CIRCUIT_NAME] = node
        .context()
        .flow.get(constants.CIRCUIT_NAME);
      msg.payload["qubit_id"] = qbit_component.parameters["id"];

      component.addComponent(msg, qbit_component);

      // Increment the number of expected qubits
      expectedQubits += 1;

      // Update the flow context with the new value
      node.context().flow.set(constants.EXPECTED_QUBITS, expectedQubits);

      // Send the message onward
      node.send(msg);
    });
  }

  RED.nodes.registerType("qbit", qbitNode);
};
