const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function U_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const U_gate_component = new component.Component("U_gate",{});
      U_gate_component.parameters["theta"] = config.theta;
      U_gate_component.parameters["phi"] = config.phi;
      U_gate_component.parameters["lam"] = config.lambda;
      U_gate_component.parameters["qbit"] = node.context().flow.get(constants.EXPECTED_QUBITS) || 0;
      U_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, U_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("U_gate", U_gateNode);
}