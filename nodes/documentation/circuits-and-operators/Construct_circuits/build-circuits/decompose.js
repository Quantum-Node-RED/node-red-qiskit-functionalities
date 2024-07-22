const runPythonScript = require("../../../../pythonShell");

module.exports = function (RED) {
  function decomposeNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;
    node.info = config.info;
    
    node.on("input", async function () {
      const result = await new Promise((resolve, reject) => {
        runPythonScript(__dirname, "decompose.py", arg=null, (err, results) => {
          if (err) reject(err);
          else resolve(results);
        });
      });

      const newMsg = {
        payload: result
      };
      node.send(newMsg);
    });
  }
  RED.nodes.registerType("decompose", decomposeNode);
};