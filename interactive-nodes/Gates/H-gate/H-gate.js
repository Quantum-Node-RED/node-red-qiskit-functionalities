const component = require("../../component.js");
module.exports = function (RED) {
  function H_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const H_gate_component = new component.Component("H_gate",{});
      H_gate_component.parameters["qbit"] = qbit;
      component.addComponent(msg, H_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("H_gate", H_gateNode);
}