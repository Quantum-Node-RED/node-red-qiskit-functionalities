const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function drawNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const output_type = config.output_type
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const draw_component = new component.Component("draw",{});
      draw_component.parameters["output_type"] = output_type;
      draw_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, draw_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("draw", drawNode);
}