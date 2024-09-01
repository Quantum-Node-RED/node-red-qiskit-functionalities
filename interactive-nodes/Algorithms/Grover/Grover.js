const component = require("../../component.js");

module.exports = function (RED) {
  function GroverNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const Grover_component = new component.Component("QAOA", {});
      Grover_component.parameters["oracleType"] = config.oracleType;
      Grover_component.parameters["iterators"] = config.iterators;
      Grover_component.parameters["input"] = config.input;
      Grover_component.parameters["growthRate"] = config.growthRate;
      Grover_component.parameters["sampleFromIterations"] = config.sampleFromIterations;
      Grover_component.parameters["target"] = config.target;
      component.addComponent(msg, Grover_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("Grover", GroverNode);
};
