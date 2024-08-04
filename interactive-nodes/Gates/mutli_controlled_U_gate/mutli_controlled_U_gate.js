const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function mutli_controlled_U_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const mutli_controlled_U_gate_component = new component.Component("mutli_controlled_U_gate",{});
      mutli_controlled_U_gate_component.parameters["qbit"] = qbit;
      mutli_controlled_U_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, mutli_controlled_U_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("mutli_controlled_U_gate", mutli_controlled_U_gateNode);
}