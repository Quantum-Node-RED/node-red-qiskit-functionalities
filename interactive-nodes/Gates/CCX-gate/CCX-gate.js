const component = require("../../component.js");
module.exports = function (RED) {
  function CCX_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const CCX_gate_component = new component.Component("CCX_gate",{});
      CCX_gate_component.parameters["qbit"] = qbit;
      component.addComponent(msg, CCX_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("CCX_gate", CCX_gateNode);
}