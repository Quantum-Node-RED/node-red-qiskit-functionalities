const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function I_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const I_gate_component = new component.Component("I_gate",{});
      I_gate_component.parameters["qbit"] = qbit;
      I_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, I_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("I_gate", I_gateNode);
}