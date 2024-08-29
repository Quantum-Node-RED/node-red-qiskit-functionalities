const runPythonScript = require("../../pythonShell");

module.exports = function (RED) {
  function BuildOracleNode(config) {
    RED.nodes.createNode(this, config);
    this.target = config.target;
    this.gates = config.gates;
    var node = this;
    node.on("input", async function (msg) {
      const result = await new Promise((resolve, reject) => {
        let options = {};
        if (msg.payload && msg.payload.gates) {
          options = {
            target: node.target,
            gates: msg.payload.gates
          };
        } else {
          options = {
            target: node.target,
            gates: node.gates
          };
        }
        runPythonScript(__dirname, "build_oracle.py", options, (err, results) => {
          if (err) {
            node.error("Error running Python script: " + err);
            return reject(err);
          }
          return resolve(results);
        });
      });

      const newMsg = {
        payload: result
      };
      node.send(newMsg);
    });
  }
  RED.nodes.registerType("Build-Oracle", BuildOracleNode);
};
