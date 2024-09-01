const component = require("../../component.js");
module.exports = function (RED) {
  function parameter_conditionNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const parameter_condition = JSON.parse(config.parameter_condition);
    node.context().set('parameter_circuit_condition', parameter_condition);
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const parameter_condition_component = new component.Component("parameter_condition", {});
      parameter_condition_component.parameters["parameter_condition"] = JSON.stringify(parameter_condition);
      component.addComponent(msg, parameter_condition_component);
      node.send(msg);
    });
  }
    
  RED.nodes.registerType("parameter_condition", parameter_conditionNode);
};