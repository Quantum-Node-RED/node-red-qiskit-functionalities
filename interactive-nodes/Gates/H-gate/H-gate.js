const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function H_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const H_gate_component = new component.Component("H_gate",{});
      H_gate_component.parameters["qbit"] = msg.payload["qubit_id"];
      H_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, H_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("H_gate", H_gateNode);
}