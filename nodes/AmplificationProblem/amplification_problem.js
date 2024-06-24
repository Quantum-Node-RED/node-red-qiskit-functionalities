const runPythonScript = require("../runPythonScript");

module.exports = function (RED) {
  function AmplificationProblemNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", async function (msg) {
      const result = await new Promise((resolve, reject) => {
        const options = {}; 
        runPythonScript(__dirname, "amplification_problem.py", options, (err, results) => {
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
  RED.nodes.registerType("amplification-problem", AmplificationProblemNode);
};
