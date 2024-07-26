module.exports = function (RED) {
  function HamiltonianConstructionNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      if (!msg.payload) {
        msg.payload = {};
      }

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
      msg.payload.hamiltonian = hamiltonian;
      node.send(msg);
    });
  }
  RED.nodes.registerType(
    "Hamiltonian-Construction",
    HamiltonianConstructionNode
  );

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
