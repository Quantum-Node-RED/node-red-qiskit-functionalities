const component = require("../../component.js");
const constants = require('../../constants.js');

module.exports = function (RED) {
  function Quantum_Circuit_BeginNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    // Get the input name
    const nodeName = config.name

    node.on("input", function (msg) {
      msg.payload = msg.payload || {};

      // Store the number of expected qubits in flow context
      node.context().flow.set(constants.EXPECTED_QUBITS, 0);

      // Add the Quantum Circuit Begin component
      const Quantum_Circuit_Begin_component = new component.Component(
        constants.QUANTUM_CITCUIT_BEGIN_COMPONENT_NAME,
        {}
      );
      Quantum_Circuit_Begin_component.parameters["name"] = nodeName;
      component.addComponent(msg, Quantum_Circuit_Begin_component);

      // Send the message with the updated payload
      node.send(msg);
    });
  }

  RED.nodes.registerType("Quantum_Circuit_Begin", Quantum_Circuit_BeginNode);
};
