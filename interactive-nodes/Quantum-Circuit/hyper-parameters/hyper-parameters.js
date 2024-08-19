const component = require("../../component.js");
module.exports = function (RED) {
  function hyper_parametersNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const hyper_parameters = JSON.parse(config.hyper_parameters);
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const hyper_parameters_component = new component.Component("hyper_parameters", {});
      hyper_parameters_component.parameters["hyper_parameters"] = JSON.stringify(hyper_parameters);
      component.addComponent(msg, hyper_parameters_component);
      node.send(msg);
    });
  }
    
  RED.nodes.registerType("hyper_parameters", hyper_parametersNode);
};