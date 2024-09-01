const component = require("../../component.js");

module.exports = function (RED) {
  function buildHamiltonianOperatorFromWeightMatrixNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      // Add the Hamiltonian Construction component
      const build_hamiltonian_operator_from_weight_matrix_component =
        new component.Component(
          "build_hamiltonian_operator_from_weight_matrix",
          {}
        );
      build_hamiltonian_operator_from_weight_matrix_component.parameters[
        "operator_name"
      ] = config.operator;
      build_hamiltonian_operator_from_weight_matrix_component.parameters[
        "weight_matrix"
      ] = config.weight_matrix;
      component.addComponent(
        msg,
        build_hamiltonian_operator_from_weight_matrix_component
      );

      node.send(msg);
    });
  }
  RED.nodes.registerType(
    "build_hamiltonian_operator_from_weight_matrix",
    buildHamiltonianOperatorFromWeightMatrixNode
  );
};
