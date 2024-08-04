const component = require("../../component.js");
module.exports = function (RED) {
  function barrierNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const barrier_component = new component.Component("barrier", {});
      barrier_component.parameters["qbit"] = qbit
      barrier_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, barrier_component);
      node.send(msg);
    });
  }
    
  RED.nodes.registerType("barrier", barrierNode);
};
