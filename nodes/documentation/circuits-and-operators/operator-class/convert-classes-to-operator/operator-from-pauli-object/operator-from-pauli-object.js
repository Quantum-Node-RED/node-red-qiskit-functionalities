const runPythonScript = require("../../../../../pythonShell");

module.exports = function (RED) {
  function OperatorFromPauli(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;
    node.pauli = config.pauli;

    node.on("input", async function (msg) {
      const option = {
        pauli: node.pauli,
      };
      const result = await new Promise((resolve, reject) => {
        runPythonScript(
          __dirname,
          "operator-from-pauli-object.py",
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
  RED.nodes.registerType("Operator-From-Pauli", OperatorFromPauli);
};
