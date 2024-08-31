const runPythonScript = require("../../pythonShell");

module.exports = function (RED) {
  function wholeQAOA(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.option = config.option; // Read the dropdown option from the config
    node.hamiltonian = config.hamiltonian; // Read the input for hamiltonian from the config
    node.adjacent_matrices = config.adjacent_matrices; // Read the input for w from the config
    node.reps = config.reps; // Read the integer input for reps from the config
    node.seed = config.seed; // Read the integer input for seed from the config

    node.on("input", async function (msg) {
      const result = await new Promise((resolve, reject) => {
        const option = {
          hamiltonian: node.hamiltonian,
          // 'w' represents the adjacency matrix of the graph.
          // It defines the weights of edges between nodes in the graph.
          adjacent_matrices: node.adjacent_matrices,
          // 'reps' specifies the number of repetitions (or layers) in the QAOA algorithm.
          // It controls the depth of the quantum circuit used by QAOA.
          reps: node.reps || 2,

          // 'seed' is used to initialize the random number generator for reproducibility.
          // It ensures consistent results across different runs of the algorithm.
          seed: node.seed || 10598,

          // Include the selected dropdown option
          QAOA_problems: node.option,
        };
        runPythonScript(__dirname, "whole-QAOA.py", option, (err, results) => {
          if (err) return reject(err);
          return resolve(results);
        });
      });

      const newMsg = {
        payload: result,
      };
      node.send(newMsg);
    });
  }
  RED.nodes.registerType("whole_QAOA", wholeQAOA);
};
