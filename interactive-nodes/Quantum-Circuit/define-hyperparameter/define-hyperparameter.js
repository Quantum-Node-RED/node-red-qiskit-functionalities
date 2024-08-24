const component = require("../../component.js");
module.exports = function (RED) {
  function define_hyperparameterNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    let hyperparameters = JSON.parse(config.hyperparameters);
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const define_hyperparameter_component = new component.Component(
        "define_hyperparameter",
        {}
      );
      define_hyperparameter_component.parameters["hyperparameters"] =
        JSON.stringify(hyperparameters);
      component.addComponent(msg, define_hyperparameter_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("define_hyperparameter", define_hyperparameterNode);
};
