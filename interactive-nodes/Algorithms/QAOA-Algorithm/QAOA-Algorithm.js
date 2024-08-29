const component = require("../../component.js");

module.exports = function (RED) {
  function QAOAAlgorithm(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const QAOA_component = new component.Component("QAOA", {});
      QAOA_component.parameters["sampler"] = "Sampler()";
      QAOA_component.parameters["optimizer"] = config.optimizer;
      QAOA_component.parameters["reps"] = config.reps;
      QAOA_component.parameters["var_result"] = "result";
      component.addComponent(msg, QAOA_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("QAOA-Algorithm", QAOAAlgorithm);
};
