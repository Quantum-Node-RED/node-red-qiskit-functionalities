const runPythonScript = require("../../../../pythonShell");

module.exports = function (RED) {
  function PauliOperationsNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;
    node.operator = config.operator;

    node.on("input", async function (msg) {
      const option = {
        operator: node.operator,
      };
      const result = await new Promise((resolve, reject) => {
        runPythonScript(
          __dirname,
          "pauli-operations.py",
          option,
          (err, results) => {
            if (err) reject(err);
            resolve(results);
          }
        );
      });

      try {
        const newMsg = {
          payload: result,
        };
        node.send(newMsg);
      } catch (e) {
        node.error(e);
      }
    });
  }
  RED.nodes.registerType("pauli-operations", PauliOperationsNode);
};
