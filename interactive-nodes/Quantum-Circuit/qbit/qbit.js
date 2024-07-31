const component = require("../../component.js");

module.exports = function (RED) {
  function qbitNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      msg.payload = msg.payload || {};

      // Access the flow context to get the current value of expectedQubits
      let expectedQubits = node.context().flow.get("expectedQubits") || 0;

      // Add the qbit component as a child
      const qbit_component = new component.Component("qbit", {});
      qbit_component.parameters["id"] = expectedQubits;
      component.addComponent(msg, qbit_component);

      // Increment the number of expected qubits
      expectedQubits += 1;

      // Update the flow context with the new value
      node.context().flow.set("expectedQubits", expectedQubits);
      // Send the message onward
      node.send(msg);
    });
  }

  RED.nodes.registerType("qbit", qbitNode);
};
