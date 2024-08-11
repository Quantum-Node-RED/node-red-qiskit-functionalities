const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function mutli_controlled_U_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const mutli_controlled_U_gate_component = new component.Component("mutli_controlled_U_gate", {});
      mutli_controlled_U_gate_component.parameters["theta"] = parseFloat(config.theta);
      mutli_controlled_U_gate_component.parameters["phi"] = parseFloat(config.phi);
      mutli_controlled_U_gate_component.parameters["lam"] = parseFloat(config.lambda);
      mutli_controlled_U_gate_component.parameters["num_of_control_qubits"] = parseInt(config.num_of_control_qubits);
      mutli_controlled_U_gate_component.parameters["list_of_control_qubits"] = parseInt(config.list_of_control_qubits);
      mutli_controlled_U_gate_component.parameters["target_qubit"] = msg.payload["qubit_id"];
      mutli_controlled_U_gate_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, mutli_controlled_U_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("mutli_controlled_U_gate", mutli_controlled_U_gateNode);
}