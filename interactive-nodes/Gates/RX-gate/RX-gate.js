const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function RX_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const RX_gate_component = new component.Component("RX_gate", {});
      RX_gate_component.parameters["qbit"] = msg.payload["qubit_id"];
      RX_gate_component.parameters["theta"] = parseFloat(config.theta);
      RX_gate_component.parameters["mode"] = config.mode;
      RX_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, RX_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("RX_gate", RX_gateNode);
}