const component=require('../../component.js');
const constants = require('../../constants.js');

module.exports = function (RED) {
    function Classical_registerNode(config) {
      RED.nodes.createNode(this, config);
      var node = this;

      const var_name = config.name;
      const num_qubits = config.num_qubits;

      node.on('input', function (msg) {
        msg.payload = msg.payload || {};
        const Classical_register_component = new component.Component(constants.CLASSICAL_REGISTER_COMPONENT_NAME,{});
        Classical_register_component.parameters["var_name"] = var_name;
        Classical_register_component.parameters["num_bits"] = num_qubits;
        component.addComponent(msg, Classical_register_component);
        node.send(msg);
      });
    }
    RED.nodes.registerType("Classical-register", Classical_registerNode);
  }