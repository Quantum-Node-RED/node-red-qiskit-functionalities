const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function AlignmentContextNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      // const result = await new Promise((resolve,reject) => {

        
      //   runPythonScript(__dirname, "Initial_ScheduleBlock.py", arg = null, (err, results) => {
      //     if (err) throw err;
      //     return resolve(results);
      //   });
      
      // });

      // const newMsg = {
      //   payload: result
      // }


      node.send(msg);
    });
  }
  RED.nodes.registerType("pulse-builder-alignment-context", AlignmentContextNode);
}

