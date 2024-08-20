const component = require("../../component.js");

module.exports = function (RED) {
  function applyHamiltonianNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      // Parse terms and coefficients from the config
      const terms = config.terms ? config.terms.split(",") : [];
      const coefficients = config.coefficients
        ? config.coefficients.split(",").map(Number)
        : [];

      if (terms.length !== coefficients.length) {
        node.error("Number of terms and coefficients must match");
        return;
      }

      // Construct the Hamiltonian
      const hamiltonian = constructHamiltonian(terms, coefficients);

      // Add the Hamiltonian Construction component
      const apply_hamiltonian_component = new component.Component(
        "apply_hamiltonian",
        {}
      );
      apply_hamiltonian_component.parameters["operator_name"] = config.operator;
      component.addComponent(msg, apply_hamiltonian_component);

      node.send(msg);
    });
  }
  RED.nodes.registerType("apply_hamiltonian", applyHamiltonianNode);

  function constructHamiltonian(terms, coefficients) {
    const hamiltonianTerms = [];

    terms.forEach((term, index) => {
      hamiltonianTerms.push({
        coeff: coefficients[index],
        pauli: term,
      });
    });

    return { terms: hamiltonianTerms };
  }
};
