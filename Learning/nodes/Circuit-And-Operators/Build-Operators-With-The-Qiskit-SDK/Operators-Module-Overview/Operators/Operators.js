const runPythonScript = require("../../../../pythonShell");

module.exports = function (RED) {
  function OperatorsNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;
    node.matrix = config.matrix;

    node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });

    node.on("input", async function (msg) {
      node.status({ fill: "green", shape: "dot", text: "You have learned this node." });
      const option = {
        matrix: node.matrix
      };
      const result = await new Promise((resolve, reject) => {
        runPythonScript(__dirname, "Operators.py", option, (err, results) => {
          if (err) reject(err);
          resolve(results);
        });
      });

      try {
        const newMsg = {
          payload: result
        };
        node.send(newMsg);
      } catch (e) {
        node.error(e);
      }
    });

    node.on('close', function () {
      node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });
    });
  }
  RED.nodes.registerType("operators", OperatorsNode);
};
