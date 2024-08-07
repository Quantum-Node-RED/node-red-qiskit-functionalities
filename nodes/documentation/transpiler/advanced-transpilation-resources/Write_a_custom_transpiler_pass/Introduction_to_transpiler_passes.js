const runPythonScript = require("../../../../pythonShell.js");


module.exports = function (RED) {
  function IntroToTranspilerPassNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {


      node.send(msg);

    });
  }
  RED.nodes.registerType("intro-to-transpiler-pass", IntroToTranspilerPassNode);
}

