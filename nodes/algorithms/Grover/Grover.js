const runPythonScript = require("../../pythonShell");

module.exports = function (RED) {
  function GroverNode(config) {
    RED.nodes.createNode(this, config);
    this.oracleType = config.oracleType;
    this.iterators = config.iterators;
    this.input = config.input
    this.growthRate = config.growthRate;
    this.sampleFromIterations = config.sampleFromIterations;
    this.target = config.target;
    var node = this;
    node.on("input", async function (msg) {
      const result = await new Promise((resolve, reject) => {
        const options = {
          target: node.target,
          oracleType: node.oracleType,
          iterators: node.iterators,
          input : node.input,
          growthRate: node.growthRate,
          sampleFromIterations: node.sampleFromIterations
        }; 
        runPythonScript(__dirname, "Grover.py", options, (err, results) => {
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
  RED.nodes.registerType("Grover", GroverNode);
};
