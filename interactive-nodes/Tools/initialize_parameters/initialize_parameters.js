const component = require("../../component.js");
module.exports = function (RED) {
  function initializeParametersNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const initialize_parameters_component = new component.Component("initialize_parameters", {});
      initialize_parameters_component.parameters["num_thetas"] = config.num_thetas || 0;
      component.addComponent(msg, initialize_parameters_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("initialize_parameters", initializeParametersNode);
}