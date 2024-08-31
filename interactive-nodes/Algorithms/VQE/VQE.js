const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function VQENode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const VQE_component = new component.Component("VQE", {});
      VQE_component.parameters["var_result"] = config.varResult;
      VQE_component.parameters["estimator"] = config.estimatorName;
      VQE_component.parameters["ansatz"] = config.ansatzName;
      VQE_component.parameters["optimizer"] = config.optimizerName;
      VQE_component.parameters["operator"] = config.operatorName
      component.addComponent(msg, VQE_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("VQE", VQENode);
}