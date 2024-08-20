const runPythonScript = require("../../../../pythonShell");

module.exports = function (RED) {
  function SparsePauliOpNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;
    node.op1 = config.op1;
    node.op1_num_qubits = config.op1_num_qubits;

    node.on("input", async function (msg) {
      const option = {
        op1: {
          sparse_list: node.op1,
          num_qubits: parseInt(node.op1_num_qubits),
        },
      };
      const result = await new Promise((resolve, reject) => {
        runPythonScript(
          __dirname,
          "sparse-pauli-op.py",
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
  RED.nodes.registerType("sparse-pauli-op", SparsePauliOpNode);
};
