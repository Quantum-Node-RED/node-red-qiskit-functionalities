const component = require("../../component.js");
module.exports = function (RED) {
  function custom_programmingNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    this.exampleText = config.exampleText;

    // console.log(this.exampleText);


    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const custom_code_component = new component.Component(
        "custom_programming",
        {}
      );
      custom_code_component.parameters["custom_code"] = this.exampleText;
      component.addComponent(msg, custom_code_component);
      // msg.payload={result: this.exampleText};
      node.send(msg);
    });
  }
  RED.nodes.registerType("custom_programming", custom_programmingNode);
};
