const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function ScheduleBlockShiftFrequencyNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      const result = await new Promise((resolve,reject) => {

        
        runPythonScript(__dirname, "ScheduleBlock_shift_freq.py", arg = null, (err, results) => {
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
  RED.nodes.registerType("pulse-shift-freq", ScheduleBlockShiftFrequencyNode);
}

