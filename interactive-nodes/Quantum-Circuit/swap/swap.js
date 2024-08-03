const component = require("../../component.js");
const constants = require('../../constants.js');

module.exports = function (RED) {
  function swapNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const control = config.control
    const target = config.target

    node.on("input", function (msg) {
      msg.payload = msg.payload || {};

      const swap_component = new component.Component(constants.SWAP_COMPONENT_NAME, {});
      swap_component.parameters["control"] = control;
      swap_component.parameters["target"] = target;

      component.addComponent(msg, swap_component);

      // Send the message onward
      node.send(msg);
    });
  }

  RED.nodes.registerType("swap_component", swapNode);
};
