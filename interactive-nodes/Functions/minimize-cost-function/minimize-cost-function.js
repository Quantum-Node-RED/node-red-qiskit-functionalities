const component = require("../../component.js");
module.exports = function (RED) {
  function minimizeCostFunctionNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const minimize_cost_function_component = new component.Component("minimize-cost-function", {});
      minimize_cost_function_component.parameters["circuit_name"] = config.circuit_name;
      minimize_cost_function_component.parameters["hamiltonian_name"] = config.hamiltonian_name;
      component.addComponent(msg, minimize_cost_function_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("minimize-cost-function", minimizeCostFunctionNode);
};
