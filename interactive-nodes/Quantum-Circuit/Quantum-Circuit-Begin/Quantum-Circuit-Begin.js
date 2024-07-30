const component = require("../../component.js");

module.exports = function (RED) {
  function Quantum_Circuit_BeginNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      msg.payload = msg.payload || {};

      // Store the number of expected qubits in flow context
      node.context().flow.set("expectedQubits", 0);

      // Add the Quantum Circuit Begin component
      const Quantum_Circuit_Begin_component = new component.Component(
        "Quantum_Circuit_Begin",
        {}
      );
      component.addComponent(msg, Quantum_Circuit_Begin_component);

      // Send the message with the updated payload
      node.send(msg);
    });
  }

  RED.nodes.registerType("Quantum_Circuit_Begin", Quantum_Circuit_BeginNode);
};
