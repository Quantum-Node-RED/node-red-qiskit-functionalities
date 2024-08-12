const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function drawCircuitNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const draw_component = new component.Component("draw_circuit", {});
      draw_component.parameters[constants.CIRCUIT_NAME] = msg.payload.currentNode.parameters.circuit_name;
      component.addComponent(msg, draw_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("draw_circuit", drawCircuitNode);
}