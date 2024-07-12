const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function AlignRightNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      const result = await new Promise((resolve,reject) => {

        
        runPythonScript(__dirname, "Align_context_right.py", arg = null, (err, results) => {
          if (err) throw err;
          return resolve(results);
        });
      
      });

      const newMsg = {
        payload: result
      }


      node.send(newMsg);
    });
  }
  RED.nodes.registerType("pulse-builder-align-right", AlignRightNode);
}

