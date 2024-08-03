const component = require("../../component.js");
module.exports = function (RED) {
  function RX_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const RX_gate_component = new component.Component("RX_gate",{});
      component.addComponent(msg, RX_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("RX_gate", RX_gateNode);
}