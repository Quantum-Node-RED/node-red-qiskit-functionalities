const component = require("../../component.js");
module.exports = function (RED) {
  function U_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const U_gate_component = new component.Component("U_gate",{});
      component.addComponent(msg, U_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("U_gate", U_gateNode);
}