const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function ScheduleBlockSetPhaseNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      const result = await new Promise((resolve,reject) => {

        
        runPythonScript(__dirname, "ScheduleBlock_set_phase.py", arg = null, (err, results) => {
          if (err) throw err;
          return resolve(results);
        });
      
      });

      const newMsg = {
        payload: result,
        encoding: "base64"
      }


      node.send(newMsg);
    });
  }
  RED.nodes.registerType("pulse-set-phase", ScheduleBlockSetPhaseNode);
}

