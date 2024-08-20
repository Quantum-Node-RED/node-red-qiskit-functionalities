const runPythonScript = require("../../../../pythonShell");

module.exports = function (RED) {
  function InitializeSamplerNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      node.send(msg);
    });
  }
  RED.nodes.registerType("initialize-sampler", InitializeSamplerNode);
}