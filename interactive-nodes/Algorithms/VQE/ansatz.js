const runPythonScript = require("../../pythonShell");

module.exports = function (RED) {
  function ansatzNode(config) {
    RED.nodes.createNode(this, config);

    this.rotationLayers = config.rotationLayers;
    this.entanglementLayers = config.entanglementLayers;

    var node = this;
    node.on('input', async function (msg) {
      const option = {
        numQubits: msg.payload.numQubits,
        paulis: msg.payload.paulis,
        rotationLayers: node.rotationLayers,
        entanglementLayers: node.entanglementLayers
      };
      const result = await new Promise((resolve, reject) => {
        runPythonScript(__dirname, "ansatz.py", option, (err, results) => {
          if (err) throw err;
          return resolve(results);
        });
      });

      const newMsg = {
        payload: option,
        result: result
      };
      node.send(newMsg);
    });
  }
  RED.nodes.registerType("ansatz", ansatzNode);
}