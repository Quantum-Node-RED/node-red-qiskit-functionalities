const runPythonScript = require("../../../pythonShell");

module.exports = function(RED) {
  function BarriersMplDrawNode(config) {
    RED.nodes.createNode(this,config);
    var node = this;
    node.on('input', async function(msg) {
      const result = await new Promise((resolve, reject) => {
        const option = {

        };
        runPythonScript(__dirname, "barriers-mpl-draw.py", option, (err, results) => {
          if (err) throw err;
          return resolve(results);
        });
      });
        
      const newMsg = {
        payload: result
      };
      node.send(newMsg);
    });
  }
  RED.nodes.registerType("barriers-mpl-draw", BarriersMplDrawNode);
}