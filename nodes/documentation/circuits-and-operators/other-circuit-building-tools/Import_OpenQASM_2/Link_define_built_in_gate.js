const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function LinkDefineBuiltInGateNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      const result = await new Promise((resolve,reject) => {

        
        runPythonScript(__dirname, "Link_define_built_in_gate.py", arg = null, (err, results) => {
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
  RED.nodes.registerType("link-define-new-built-in-gate", LinkDefineBuiltInGateNode);
}

