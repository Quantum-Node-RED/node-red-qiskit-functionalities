const runPythonScript = require("../../pythonShell");

module.exports = function (RED) {
  function GroverIterationNode(config) {
    RED.nodes.createNode(this, config);
    this.iterators = config.iterators;
    this.input = config.input
    this.growthRate = config.growthRate;
    this.sampleFromIterations = config.sampleFromIterations;
    var node = this;
    node.on("input", async function (msg) {
      const result = await new Promise((resolve, reject) => {
        const options = {
          iterators: node.iterators,
          input : node.input,
          growthRate: node.growthRate,
          sampleFromIterations: node.sampleFromIterations,
          target : msg.payload.result.target
        }; 
        runPythonScript(__dirname, "Grover_iteration.py", options, (err, results) => {
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
  RED.nodes.registerType("Grover_iteration", GroverIterationNode);
};
