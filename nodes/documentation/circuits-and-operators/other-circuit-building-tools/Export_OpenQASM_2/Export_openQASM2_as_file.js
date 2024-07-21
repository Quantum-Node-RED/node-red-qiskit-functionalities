const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function ExportQiskitAsOpenQASM2FileNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      const result = await new Promise((resolve,reject) => {

        
        runPythonScript(__dirname, "Export_openQASM2_as_file.py", arg = null, (err, results) => {
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
  RED.nodes.registerType("export-Qiskit-as-OpenQASM2-file", ExportQiskitAsOpenQASM2FileNode);
}

