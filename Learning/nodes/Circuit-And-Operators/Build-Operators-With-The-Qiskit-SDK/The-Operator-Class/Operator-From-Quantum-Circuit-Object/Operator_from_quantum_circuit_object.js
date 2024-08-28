const runPythonScript = require("../../../../pythonShell");

module.exports = function (RED) {
  function OperatorFromQuantumCircuitObject(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;

    node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });

    node.on("input", async function (msg) {
      node.status({ fill: "green", shape: "dot", text: "You have learned this node." });
      const option = {};
      const result = await new Promise((resolve, reject) => {
        runPythonScript(
          __dirname,
          "Operator_from_quantum_circuit_object.py",
          option,
          (err, results) => {
            if (err) reject(err);
            resolve(results);
          }
        );
      });

      const newMsg = {
        payload: result
      };
      node.send(newMsg);
    });

    node.on('close', function () {
      node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });
    });
  }
  RED.nodes.registerType(
    "Operator-From-Quantum-Circuit-Object",
    OperatorFromQuantumCircuitObject
  );
};
