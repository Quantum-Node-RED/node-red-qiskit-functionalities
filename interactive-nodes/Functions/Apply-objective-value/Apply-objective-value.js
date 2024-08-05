const component = require("../../component.js");
module.exports = function (RED) {
  function apply_objective_valueNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const apply_objective_value_component = new component.Component(
        "apply_objective_value",
        {}
      );
      apply_objective_value_component.parameters["binary_vector"] =
        "objective_value";
      apply_objective_value_component.parameters["matrix"] = [];
      apply_objective_value_component.parameters["var_result"] =
        "objective_value";
      component.addComponent(msg, apply_objective_value_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("apply_objective_value", apply_objective_valueNode);
};
