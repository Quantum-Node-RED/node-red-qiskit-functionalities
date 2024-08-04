const component=require('../../component.js');
const constants = require('../../constants.js');
module.exports = function (RED) {
  function CZ_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const CZ_gate_component = new component.Component("CZ_gate",{});
      CZ_gate_component.parameters["control_qubit"] = config.control_qubit;
      CZ_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      CZ_gate_component.parameters["target_qubit"] = msg.payload["qubit_id"];
      component.addComponent(msg, CZ_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("CZ_gate", CZ_gateNode);
}