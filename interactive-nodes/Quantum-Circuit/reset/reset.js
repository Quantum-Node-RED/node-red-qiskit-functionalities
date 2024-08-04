const component = require("../../component.js");
const constants = require('../../constants.js');

module.exports = function (RED) {
  function resetNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbits = config.reset_qubits

    node.on("input", function (msg) {
      msg.payload = msg.payload || {};

      const reset_component = new component.Component(constants.RESET_COMPONENT_NAME, {});
      // qubit: qubit(s) to reset
      reset_component.parameters["qbit"] = qbits;
      reset_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, reset_component);

      // Send the message onward
      node.send(msg);
    });
  }

  RED.nodes.registerType("reset", resetNode);
};
