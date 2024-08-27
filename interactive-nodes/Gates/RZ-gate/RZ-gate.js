const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function RZ_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const RZ_gate_component = new component.Component("RZ_gate", {});
      RZ_gate_component.parameters["qbit"] = msg.payload["qubit_id"];
      RZ_gate_component.parameters["theta"] = parseFloat(config.theta);
      RZ_gate_component.parameters["mode"] = config.mode;
      RZ_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      RZ_gate_component.parameters["sequence_no"] = config.sequence_no;
      component.addComponent(msg, RZ_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("RZ_gate", RZ_gateNode);
}