const runPythonScript = require("../../../../pythonShell");

module.exports = function (RED) {
  function OperatorsNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;
    node.matrix = config.matrix;

    node.on("input", async function (msg) {
      const option = {
        matrix: node.matrix,
      };
      const result = await new Promise((resolve, reject) => {
        runPythonScript(__dirname, "operators.py", option, (err, results) => {
          if (err) reject(err);
          resolve(results);
        });
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
  RED.nodes.registerType("operators", OperatorsNode);
};
