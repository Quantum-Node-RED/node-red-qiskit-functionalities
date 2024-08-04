const component = require("../../component.js");
module.exports = function (RED) {
  function U_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    const theta = config.theta
    const phi = config.phi
    const lambda = config.lambda
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const U_gate_component = new component.Component("U_gate",{});
      U_gate_component.parameters["theta"] = theta;
      U_gate_component.parameters["phi"] = phi;
      U_gate_component.parameters["lambda"] = lambda;
      U_gate_component.parameters["qbit"] = qbit;
      component.addComponent(msg, U_gate_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("U_gate", U_gateNode);
}