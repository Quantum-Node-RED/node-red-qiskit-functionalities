const component = require("../../component.js");
module.exports = function (RED) {
  function execute_quantum_circuit_with_samplerNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const execute_quantum_circuit_with_sampler_component =
        new component.Component("execute_quantum_circuit_with_sampler", {});
      execute_quantum_circuit_with_sampler_component.parameters["variable"] =
        config.variable;
      execute_quantum_circuit_with_sampler_component.parameters[
        "circuit_name"
      ] = config.circuit_name;
      execute_quantum_circuit_with_sampler_component.parameters["sampler"] =
        config.sampler;
      execute_quantum_circuit_with_sampler_component.parameters["result"] =
        config.result;
      execute_quantum_circuit_with_sampler_component.parameters[
        "param_vector"
      ] = config.parameterVector;
      component.addComponent(
        msg,
        execute_quantum_circuit_with_sampler_component
      );
      node.send(msg);
    });
  }
  RED.nodes.registerType(
    "execute_quantum_circuit_with_sampler",
    execute_quantum_circuit_with_samplerNode
  );
};
