const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function CreateCustomBackendNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      node.send(msg);
    });
  }
  RED.nodes.registerType("create-custom-backend", CreateCustomBackendNode);
}

