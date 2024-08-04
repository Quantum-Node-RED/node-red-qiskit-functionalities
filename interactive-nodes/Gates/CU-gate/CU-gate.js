const component=require('../../component.js');
module.exports = function (RED) {
  function CU_gateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbit = config.qbit
    const theta = config.theta
    const phi = config.phi
    const lambda = config.lambda
    const gamma = config.gamma
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const CU_gate = new component.Component("CU_gate",{});
      CU_gate.parameters["theta"] = theta;
      CU_gate.parameters["phi"] = phi;
      CU_gate.parameters["lambda"] = lambda;
      CU_gate.parameters["gamma"] = gamma;
      CU_gate.parameters["qbit"] = qbit;
      component.addComponent(msg, CU_gate);
      node.send(msg);
    });
  }
  RED.nodes.registerType("CU_gate", CU_gateNode);
}