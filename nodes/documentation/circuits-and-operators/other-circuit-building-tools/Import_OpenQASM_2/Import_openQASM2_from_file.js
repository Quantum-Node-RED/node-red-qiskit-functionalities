const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function ImportOpenQASM2FromFileNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      const result = await new Promise((resolve,reject) => {

        
        runPythonScript(__dirname, "Import_openQASM2_from_file.py", arg = null, (err, results) => {
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
  RED.nodes.registerType("import-OpenQASM2-program-from-file", ImportOpenQASM2FromFileNode);
}

