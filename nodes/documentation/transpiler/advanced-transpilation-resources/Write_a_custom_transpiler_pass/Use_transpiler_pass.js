const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function UseTranspilerPassNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {

      const result = await new Promise((resolve,reject) => {

        runPythonScript(__dirname, "Use_transpiler_pass.py", arg = null, (err, results) => {
          if (err) {
            reject(err); 
            return;
          }
          resolve(results);
        });
      
      });

      const newMsg = {
        payload: result
      };


      node.send(newMsg);

    });
  }
  RED.nodes.registerType("use-the-transpiler-pass", UseTranspilerPassNode);
}

