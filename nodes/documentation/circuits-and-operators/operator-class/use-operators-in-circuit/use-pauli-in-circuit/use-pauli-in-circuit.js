const runPythonScript = require("../../../../../pythonShell");

module.exports = function (RED) {
  function UsePauliInCircuit(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;
    node.pauli = config.pauli;

    node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });

    node.on("input", async function (msg) {
      node.status({ fill: "green", shape: "dot", text: "You have learned this node." });
      const option = {
        pauli: node.pauli,
      };
      const result = await new Promise((resolve, reject) => {
        runPythonScript(
          __dirname,
          "use-pauli-in-circuit.py",
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

    node.on('close', function () {
      node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });
    });
  }
  RED.nodes.registerType("Use-Pauli-In-Circuit", UsePauliInCircuit);
};
