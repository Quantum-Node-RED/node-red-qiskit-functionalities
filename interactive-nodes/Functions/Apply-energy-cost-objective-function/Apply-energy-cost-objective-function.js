const component = require("../../component.js");
module.exports = function (RED) {
  function apply_energy_cost_objective_functionNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const apply_energy_cost_objective_function_component =
        new component.Component("apply_energy_cost_objective_function", {});
      apply_energy_cost_objective_function_component.parameters["var_result"] =
        "energy_cost_objective_function";
      component.addComponent(
        msg,
        apply_energy_cost_objective_function_component
      );
      node.send(msg);
    });
  }
  RED.nodes.registerType(
    "apply_energy_cost_objective_function",
    apply_energy_cost_objective_functionNode
  );
};
