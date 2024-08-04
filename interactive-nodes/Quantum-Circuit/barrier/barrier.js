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
      component.addComponent(msg, barrier_component);
      node.send(msg);
    });
  }
    
  RED.nodes.registerType("barrier", barrierNode);
};
