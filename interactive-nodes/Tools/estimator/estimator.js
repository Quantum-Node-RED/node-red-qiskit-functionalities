const component = require("../../component.js");
module.exports = function (RED) {
  function estimatorNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const draw_component = new component.Component("estimator", {});
      component.addComponent(msg, draw_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("estimator", estimatorNode);
}