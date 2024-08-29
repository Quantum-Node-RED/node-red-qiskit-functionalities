const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function SX_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const SX_gate_component = new component.Component("SX_gate",{});
      SX_gate_component.parameters["qbit"] = msg.payload["qubit_id"];  
      SX_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      SX_gate_component.parameters["sequence_no"]=config.sequence_no;
      component.addComponent(msg, SX_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("SX_gate", SX_gateNode);
}