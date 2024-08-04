const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function RZ_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    const theta = config.theta
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const RZ_gate_component = new component.Component("RZ_gate",{});
      RZ_gate_component.parameters["qbit"] = msg.payload["qubit_id"];
      RZ_gate_component.parameters["theta"] = theta;
      RZ_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, RZ_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("RZ_gate", RZ_gateNode);
}