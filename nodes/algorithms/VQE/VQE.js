const runPythonScript = require("../../pythonShell");

module.exports = function (RED) {
  function VQENode(config) {
    RED.nodes.createNode(this, config);

    this.rotationLayers = config.rotationLayers;
    this.entanglementLayers = config.entanglementLayers;
    this.hamiltonianPauli = config.hamiltonianPauli;
    this.hamiltonianCoeffs = config.hamiltonianCoeffs;
    this.optimizer = config.optimizer;
    this.maxiter = config.maxiter;

    var node = this;
    node.on('input', async function (msg) {
      const result = await new Promise((resolve, reject) => {
        const option = {
          numQubits: msg.payload.numQubits,
          rotationLayers: node.rotationLayers,
          entanglementLayers: node.entanglementLayers,
          hamiltonianPauli: node.hamiltonianPauli,
          hamiltonianCoeffs: node.hamiltonianCoeffs,
          optimizer: node.optimizer,
          maxiter: node.maxiter
        };
        runPythonScript(__dirname, "VQE.py", option, (err, results) => {
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
  RED.nodes.registerType("VQE", VQENode);
}