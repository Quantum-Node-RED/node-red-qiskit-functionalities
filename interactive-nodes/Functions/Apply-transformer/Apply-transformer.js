const component = require('../../component.js');
const constants = require('../../constants.js');
module.exports = function (RED) {
  function apply_transformerNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const apply_transformer_component = new component.Component("apply_transformer", {});
      apply_transformer_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, apply_transformer_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("apply_transformer", apply_transformerNode);
}