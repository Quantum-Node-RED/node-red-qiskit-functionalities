const runPythonScript = require("../../pythonShell");

module.exports = function (RED) {
  function classicEigensolverNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;
    node.on('input', async function (msg) {
      const result = await new Promise((resolve, reject) => {
        const option = {
          optimal_value: msg.payload.result.optimal_value,
          paulis: msg.payload.result.paulis
        };
        runPythonScript(__dirname, "classicEigensolver.py", option, (err, results) => {
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
  RED.nodes.registerType("classicEigensolver", classicEigensolverNode);
}