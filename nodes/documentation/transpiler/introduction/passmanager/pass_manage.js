const runPythonScript = require("../../../../pythonShell");

module.exports = function (RED) {
  function PassmanageNode(config) {
    RED.nodes.createNode(this, config);
    this.token = config.token;

    var node = this;
    node.on('input', async function (msg) {
      const result = await new Promise((resolve, reject) => {
        const options = {
          token: node.token
        };
        runPythonScript(__dirname, "pass_manage.py", options, (err, results) => {
          if (err) {
            node.error("Error running Python script: " + err);
            return reject(err);
          }
          return resolve(results);
        });
      });

      const newMsg = {
        payload: result
      };
      node.send(newMsg);
    });
  }
  RED.nodes.registerType("pass_manage", PassmanageNode);
}