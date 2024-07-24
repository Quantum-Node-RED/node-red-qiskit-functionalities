const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function LinkByLegacyExporterNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      const result = await new Promise((resolve,reject) => {

        
        runPythonScript(__dirname, "Link_by_qiskit_legacy_exporter.py", arg = null, (err, results) => {
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
  RED.nodes.registerType("link-openQASM2-by-qiskit-legacy-exporter", LinkByLegacyExporterNode);
}

