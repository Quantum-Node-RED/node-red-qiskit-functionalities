const component=require('../../component.js');
module.exports = function (RED) {
  function CZ_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const CZ_gate_component = new component.Component("CZ_gate",{});
      component.addComponent(msg, CZ_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("CZ_gate", CZ_gateNode);
}