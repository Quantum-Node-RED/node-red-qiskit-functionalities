const component = require("../../component.js");
module.exports = function (RED) {
  function define_samplerNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const define_sampler_component = new component.Component(
        "define_sampler",
        {}
      );
      define_sampler_component.parameters["variable"] = config.variable;
      component.addComponent(msg, define_sampler_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("define_sampler", define_samplerNode);
};
