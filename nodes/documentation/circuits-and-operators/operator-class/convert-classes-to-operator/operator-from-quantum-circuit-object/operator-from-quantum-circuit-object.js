const runPythonScript = require("../../../../../pythonShell");

module.exports = function (RED) {
  function OperatorFromQuantumCircuitObject(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;

    node.on("input", async function (msg) {
      const option = {};
      const result = await new Promise((resolve, reject) => {
        runPythonScript(
          __dirname,
          "operator-from-quantum-circuit-object.py",
          option,
          (err, results) => {
            if (err) reject(err);
            resolve(results);
          }
        );
      });

      const newMsg = {
        payload: result,
      };
      node.send(newMsg);
    });
  }
  RED.nodes.registerType(
    "Operator-From-Quantum-Circuit-Object",
    OperatorFromQuantumCircuitObject
  );
};
