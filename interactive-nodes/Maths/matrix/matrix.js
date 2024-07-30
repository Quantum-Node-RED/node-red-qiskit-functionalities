const component=require('../../component.js');
module.exports = function (RED) {
  function matrixNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
     msg.payload = msg.payload || {};
     const matrix_component = new component.Component("matrix",{});
     component.addComponent(msg, matrix_component);
     node.send(msg);
    });
  }
  RED.nodes.registerType("matrix", matrixNode);
}