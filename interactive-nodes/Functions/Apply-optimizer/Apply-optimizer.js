const component = require("../../component.js");
module.exports = function (RED) {
  function apply_optimizerNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const apply_optimizer_component = new component.Component(
        "apply_optimizer",
        {}
      );
      apply_optimizer_component.parameters["variable"] = config.variable;
      apply_optimizer_component.parameters["cost_function"] =
        config.costFunction;
      apply_optimizer_component.parameters["circuit_name"] = config.circuit;
      apply_optimizer_component.parameters["param_vector"] = config.paramVector;
      apply_optimizer_component.parameters["hamiltonian"] = config.hamiltonian;
      apply_optimizer_component.parameters["estimator"] = config.estimator;
      apply_optimizer_component.parameters["optimizer"] = config.optimizer;
      component.addComponent(msg, apply_optimizer_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("apply_optimizer", apply_optimizerNode);
};
