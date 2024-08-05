const component = require("../../component.js");
module.exports = function (RED) {
  function sparse_pauli_opNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const sparse_pauli_op_component = new component.Component(
        "sparse_pauli_op",
        {}
      );
      component.addComponent(msg, sparse_pauli_op_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("sparse_pauli_op", sparse_pauli_opNode);
};
