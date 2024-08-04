const component=require('../../component.js');
const constants = require('../../constants.js');
module.exports = function (RED) {
  function transformer_matrix_pauliNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const transformer_matrix_pauli_component = new component.Component("transformer_matrix_pauli",{});
      transformer_matrix_pauli_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, transformer_matrix_pauli_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("transformer_matrix_pauli", transformer_matrix_pauliNode);
}