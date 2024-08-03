const component = require("../../component.js");
module.exports = function (RED) {
  function I_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const I_gate_component = new component.Component("I_gate",{});
      component.addComponent(msg, I_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("I_gate", I_gateNode);
}