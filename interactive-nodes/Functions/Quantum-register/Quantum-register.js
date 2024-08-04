const component=require('../../component.js');
const constants = require('../../constants.js');

module.exports = function (RED) {
  function Quantum_registerNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    const var_name = config.name;
    const num_qubits = config.num_qubits;

    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const quantum_register_component = new component.Component(constants.QUANTUM_REGISTER_COMPONENT_NAME,{});
      quantum_register_component.parameters["var_name"] = var_name;
      quantum_register_component.parameters["num_bits"] = num_qubits;
      quantum_register_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, quantum_register_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("Quantum-register", Quantum_registerNode);
}