const component = require("../../component.js");
module.exports = function (RED) {
  function initializeParametersNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const draw_component = new component.Component("initialize_parameters", {});
      draw_component.parameters["num_thetas"] = config.num_thetas || 0;
      component.addComponent(msg, draw_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("initialize_parameters", initializeParametersNode);
}