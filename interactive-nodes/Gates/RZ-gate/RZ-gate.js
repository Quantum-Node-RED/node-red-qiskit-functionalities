const component = require("../../component.js");
module.exports = function (RED) {
  function RZ_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    const theta = config.theta
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const RZ_gate_component = new component.Component("RZ_gate",{});
      RZ_gate_component.parameters["qbit"] = qbit;
      RZ_gate_component.parameters["theta"] = theta;
      component.addComponent(msg, RZ_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("RZ_gate", RZ_gateNode);
}