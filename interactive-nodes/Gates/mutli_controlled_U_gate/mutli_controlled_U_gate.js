const component = require("../../component.js");
module.exports = function (RED) {
  function mutli_controlled_U_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const mutli_controlled_U_gate_component = new component.Component("mutli_controlled_U_gate",{});
      mutli_controlled_U_gate_component.parameters["qbit"] = qbit;
      component.addComponent(msg, mutli_controlled_U_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("mutli_controlled_U_gate", mutli_controlled_U_gateNode);
}