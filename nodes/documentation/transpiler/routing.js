const runPythonScript = require("../../pythonShell");

module.exports = function (RED) {
  function RoutingNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;
    node.on('input', async function (msg) {
      const result = await new Promise((resolve, reject) => {
        const options = {
          
        };
        runPythonScript(__dirname, "routing.py", options, (err, results) => {
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
  RED.nodes.registerType("routing", RoutingNode);
}