const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function PulseTryTranspileOnCus(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      const result = await new Promise((resolve,reject) => {

        
        runPythonScript(__dirname, "Pulse_Try_transpile_on_custom_gate.py", arg = null, (err, results) => {
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
  RED.nodes.registerType("pulse-try-transpile-on-custom", PulseTryTranspileOnCus);
}

