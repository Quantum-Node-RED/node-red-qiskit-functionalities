const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function Toffoli_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const Toffoli_gate_component = new component.Component("Toffoli_gate",{});
      Toffoli_gate_component.parameters["qbit"] = qbit;
      Toffoli_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, Toffoli_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("Toffoli_gate", Toffoli_gateNode);
}