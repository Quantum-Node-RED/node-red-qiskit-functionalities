const component = require("../../component.js");
module.exports = function (RED) {
  function phaseNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    const theta = config.theta
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const phase_component = new component.Component("phase",{});
      phase_component.parameters["qbit"] = qbit;
      phase_component.parameters["theta"] = theta;
      component.addComponent(msg, phase_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("phase", phaseNode);
}