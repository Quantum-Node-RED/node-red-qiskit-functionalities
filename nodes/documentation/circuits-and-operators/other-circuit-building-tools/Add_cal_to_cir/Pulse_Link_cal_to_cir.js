const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function PulseLinkCalToCirNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      const result = await new Promise((resolve,reject) => {

        
        runPythonScript(__dirname, "Pulse_Link_cal_to_cir.py", arg = null, (err, results) => {
          if (err) throw err;
          return resolve(results);
        });
      
      });

      const newMsg = {
        payload: result,
        encoding: 'base64'
      }


      node.send(newMsg);
    });
  }
  RED.nodes.registerType("pulse-link-cal-to-cir", PulseLinkCalToCirNode);
}

