const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function RX_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    const theta = config.theta
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const RX_gate_component = new component.Component("RX_gate",{});
      RX_gate_component.parameters["qbit"] = qbit;
      RX_gate_component.parameters["theta"] = theta;
      RX_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, RX_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("RX_gate", RX_gateNode);
}