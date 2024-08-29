const runPythonScript = require("../../pythonShell");

module.exports = function (RED) {
  function VQEIterationNode(config) {
    RED.nodes.createNode(this, config);

    this.maxiter = config.maxiter;

    var node = this;
    node.on('input', async function (msg) {
      const result = await new Promise((resolve, reject) => {
        const option = {
          numQubits: msg.payload.numQubits,
          rotationLayers: msg.payload.rotationLayers,
          entanglementLayers: msg.payload.entanglementLayers,
          hamiltonianPauli: msg.payload.hamiltonianPauli,
          hamiltonianCoeffs: msg.payload.hamiltonianCoeffs,
          paulis: msg.payload.paulis,
          optimizer: msg.payload.optimizer,
          maxiter: node.maxiter
        };
        runPythonScript(__dirname, "VQEIteration.py", option, (err, results) => {
          if (err) throw err;
          return resolve(results);
        });
      });

      const newMsg = {
        payload: result
      };
      node.send(newMsg);
    });
  }
  RED.nodes.registerType("VQEIteration", VQEIterationNode);
}