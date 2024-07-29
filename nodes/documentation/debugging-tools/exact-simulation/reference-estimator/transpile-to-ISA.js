const runPythonScript = require("../../../../pythonShell");

module.exports = function (RED) {
  function TranspileToISANode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      node.send(msg);
    });
  }
  RED.nodes.registerType("transpile-to-ISA", TranspileToISANode);
}