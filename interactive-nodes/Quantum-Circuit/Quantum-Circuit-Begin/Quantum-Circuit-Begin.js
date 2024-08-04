const component = require("../../component.js");
const constants = require('../../constants.js');

module.exports = function (RED) {
  function Quantum_Circuit_BeginNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      msg.payload = msg.payload || {};

      // Store the number of expected qubits in flow context
      node.context().flow.set(constants.EXPECTED_QUBITS, 0);
      // Count the number of wires connected to this node
      let connectedPaths = node._wireCount || 0;
      // Add the Quantum Circuit Begin component
      const Quantum_Circuit_Begin_component = new component.Component(
        constants.QUANTUM_CIRCUIT_BEGIN_COMPONENT_NAME,
        {}
      );
      // Set parameter the expected qubits for the Quantum Circuit Begin component
      Quantum_Circuit_Begin_component.parameters["circuit_name"] = config.circuit_name;
      Quantum_Circuit_Begin_component.parameters["num_qbits"] = connectedPaths;
      node.context().flow.set(constants.CIRCUIT_NAME, config.circuit_name);
      component.addComponent(msg, Quantum_Circuit_Begin_component);

      // Send the message with the updated payload
      node.send(msg);
    });
  }

  RED.nodes.registerType("Quantum_Circuit_Begin", Quantum_Circuit_BeginNode);
};
