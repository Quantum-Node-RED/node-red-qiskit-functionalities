const runPythonScript = require("../../.././../../pythonShell");

module.exports = function (RED) {
  function Circuits_diagramsNodes(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;
    node.info = config.info;
    
    node.on("input", async function () {
      const result = await new Promise((resolve, reject) => {
        runPythonScript(__dirname, "Circuit-diagrams.py", arg=null, (err, results) => {
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
  RED.nodes.registerType("Circuit-diagrams", Circuits_diagramsNodes);
};