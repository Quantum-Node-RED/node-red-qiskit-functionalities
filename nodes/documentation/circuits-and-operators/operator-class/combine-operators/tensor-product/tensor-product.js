const runPythonScript = require("../../../../../pythonShell");

module.exports = function (RED) {
  function TensorProduct(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;
    node.pauli_1 = config.pauli_1;
    node.pauli_2 = config.pauli_2;

    node.on("input", async function (msg) {
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
  }
  RED.nodes.registerType("Tensor-Product", TensorProduct);
};
