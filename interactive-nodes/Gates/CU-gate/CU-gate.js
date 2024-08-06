const component=require('../../component.js');
const constants = require('../../constants.js');
module.exports = function (RED) {
  function CU_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const CU_gate = new component.Component("CU_gate",{});
      CU_gate.parameters["theta"] = parseFloat(config.theta);
      CU_gate.parameters["phi"] = parseFloat(config.phi);
      CU_gate.parameters["lam"] = parseFloat(config.lambda);
      CU_gate.parameters["gamma"] = parseFloat(config.gamma);
      CU_gate.parameters["control_qubit"] = parseInt(config.control_qubit);
      CU_gate.parameters["target_qubit"] = msg.payload["qubit_id"];
      CU_gate.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, CU_gate);
      node.send(msg);
    });
  }
  RED.nodes.registerType("CU_gate", CU_gateNode);
}