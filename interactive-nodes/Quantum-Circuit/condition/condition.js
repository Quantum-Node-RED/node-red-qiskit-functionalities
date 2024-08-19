const component = require("../../component.js");
module.exports = function (RED) {
  function conditionNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const condition = JSON.parse(config.condition);
    node.context().set('circuit_condition', condition);
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const condition_component = new component.Component("condition", {});
      condition_component.parameters["condition"] = JSON.stringify(condition);
      component.addComponent(msg, condition_component);
      node.send(msg);
    });
  }
    
  RED.nodes.registerType("condition", conditionNode);
};