const runPythonScript = require("../../../../../pythonShell");

module.exports = function (RED) {
  function TensorProduct(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;
    node.pauli_1 = config.pauli_1;
    node.pauli_2 = config.pauli_2;

    node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });

    node.on("input", async function (msg) {
      node.status({ fill: "green", shape: "dot", text: "You have learned this node." });
      const option = {
        pauli_1: node.pauli_1,
        pauli_2: node.pauli_2,
      };
      const result = await new Promise((resolve, reject) => {
        runPythonScript(
          __dirname,
          "tensor-product.py",
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
  RED.nodes.registerType("Tensor-Product", TensorProduct);
};
