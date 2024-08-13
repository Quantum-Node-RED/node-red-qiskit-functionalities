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
      apply_optimizer_component.parameters["var_result"] = "optimizer_result";
      apply_optimizer_component.parameters["optimizer"] = config.optimizer;
      component.addComponent(msg, apply_optimizer_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("apply_optimizer", apply_optimizerNode);
};
