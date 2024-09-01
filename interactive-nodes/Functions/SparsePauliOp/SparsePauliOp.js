const component = require("../../component.js");

module.exports = function (RED) {
  function sparse_pauli_opNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const terms = config.terms ? config.terms.split(",").map(term => term.trim()) : [];
      const coefficients = config.coefficients
        ? config.coefficients.split(",").map(Number)
        : [];

      if (terms.length !== coefficients.length) {
        node.error("Number of terms and coefficients must match");
        return;
      }
      const sparse_pauli_op_component = new component.Component(
        "sparse_pauli_op",
        {}
      );
      sparse_pauli_op_component.parameters["variable"] = config.variable;
      sparse_pauli_op_component.parameters["pauli_list"] = terms;
      sparse_pauli_op_component.parameters["coeffs"] = coefficients;
      component.addComponent(msg, sparse_pauli_op_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("sparse-pauli-op", sparse_pauli_opNode);
};
