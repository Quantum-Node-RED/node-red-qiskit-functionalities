const component=require('../../component.js');
const constants = require('../../constants.js');
module.exports = function (RED) {
  function matrixNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    const var_name = config.name
    const matrix = config.matrix

    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const matrix_component = new component.Component(constants.MATRIX_COMPONENT_NAME,{});
      matrix_component.parameters["var_name"] = var_name;
      matrix_component.parameters["matrix"] = matrix;
      matrix_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, matrix_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("matrix", matrixNode);
};
