const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function X_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const X_gate_component = new component.Component("X_gate",{});
      X_gate_component.parameters["qbit"] = msg.payload["qubit_id"];   
      X_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, X_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("X_gate", X_gateNode);
}