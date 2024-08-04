const component = require("../../component.js");
module.exports = function (RED) {
  function RY_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    const theta = config.theta
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const RY_gate_component = new component.Component("RY_gate",{});
      RY_gate_component.parameters["qbit"] = qbit;
      RY_gate_component.parameters["theta"] = theta;
      component.addComponent(msg, RY_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("RY_gate", RY_gateNode);
}