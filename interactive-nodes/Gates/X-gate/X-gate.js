const component = require("../../component.js");
module.exports = function (RED) {
  function X_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const X_gate_component = new component.Component("X_gate",{});
      X_gate_component.parameters["qbit"] = qbit
      component.addComponent(msg, X_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("X_gate", X_gateNode);
}