const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function CCX_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const CCX_gate_component = new component.Component("CCX_gate",{});
      CCX_gate_component.parameters["control_qubit1"] = parseInt(config.control_qubit1);
      CCX_gate_component.parameters["control_qubit2"] = parseInt(config.control_qubit2);
      CCX_gate_component.parameters["target_qubit"] = msg.payload["qubit_id"];
      CCX_gate_component.parameters["sequence_no"]=config.sequence_no;
      CCX_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, CCX_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("CCX_gate", CCX_gateNode);
}