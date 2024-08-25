const component = require("../../component.js");
module.exports = function (RED) {
  function printNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const print_component = new component.Component("print", {});
      print_component.parameters["variable"] = config.variable;
      component.addComponent(msg, print_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("print", printNode);
};
