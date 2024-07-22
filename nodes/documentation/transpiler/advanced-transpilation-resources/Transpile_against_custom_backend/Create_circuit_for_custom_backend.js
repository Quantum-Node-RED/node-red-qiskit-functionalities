const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function CreateCircuitForCustomBackendNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {

      const result = await new Promise((resolve,reject) => {

        runPythonScript(__dirname, "Create_circuit_for_custom_backend.py", arg = null, (err, results) => {
          if (err) {
            reject(err); 
            return;
          }
          resolve(results);
        });
      
      });

      const newMsg = {
        payload: result
      };


      node.send(newMsg);

    });
  }
  RED.nodes.registerType("create-circuit-for-custom-backend", CreateCircuitForCustomBackendNode);
}

