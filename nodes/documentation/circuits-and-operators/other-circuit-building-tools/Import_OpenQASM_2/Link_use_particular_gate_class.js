const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function LinkByGateClassNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      const result = await new Promise((resolve,reject) => {

        
        runPythonScript(__dirname, "Link_use_particular_gate_class.py", arg = null, (err, results) => {
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
  RED.nodes.registerType("link-openQASM2-by-gate-class", LinkByGateClassNode);
}

