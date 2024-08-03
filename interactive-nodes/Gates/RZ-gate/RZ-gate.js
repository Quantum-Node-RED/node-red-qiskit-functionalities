const component = require("../../component.js");
module.exports = function (RED) {
  function RZ_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const RZ_gate_component = new component.Component("RZ_gate",{});
      component.addComponent(msg, RZ_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("RZ_gate", RZ_gateNode);
}