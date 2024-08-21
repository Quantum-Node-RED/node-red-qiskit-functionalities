const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function forEndNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const for_end_component = new component.Component("for_end",{});
      for_end_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, for_end_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("for_end", forEndNode);
}