const component=require('../../component.js');
module.exports = function (RED) {
  function CX_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const CX_gate_component = new component.Component("CX_gate",{});
      CX_gate_component.parameters["qbit"] = qbit;
      component.addComponent(msg, CX_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("CX_gate", CX_gateNode);
}