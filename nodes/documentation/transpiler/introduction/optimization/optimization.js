const runPythonScript = require("../../../../pythonShell");

module.exports = function (RED) {
  function OptimizationNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;
    node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });

    node.on('input', async function (msg) {
      node.status({ fill: "green", shape: "dot", text: "You have  learned this node." });
      const result = await new Promise((resolve, reject) => {
        const options = {
          
        };
        runPythonScript(__dirname, "optimization.py", options, (err, results) => {
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

    node.on('close', function () {
      node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });
    });
  }
  RED.nodes.registerType("optimization", OptimizationNode);
}