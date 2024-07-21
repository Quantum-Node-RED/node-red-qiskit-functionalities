const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function DefineUseCustomInstructionNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      const result = await new Promise((resolve,reject) => {

        
        runPythonScript(__dirname, "Define_use_custom_classical_instructions.py", arg = null, (err, results) => {
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
  RED.nodes.registerType("define-use-custom-classical-instruction", DefineUseCustomInstructionNode);
}

