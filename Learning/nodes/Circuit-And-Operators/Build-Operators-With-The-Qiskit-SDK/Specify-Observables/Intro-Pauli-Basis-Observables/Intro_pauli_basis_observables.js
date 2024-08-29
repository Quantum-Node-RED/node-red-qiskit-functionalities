const runPythonScript = require("../../../../pythonShell");

module.exports = function (RED) {
  function IntroPauliBasisObserablesNode(config) {
    RED.nodes.createNode(this, config);
  
    var node = this;
  
    node.on('input',  async function (msg) {
      node.send(msg);
    });
  }
  RED.nodes.registerType("intro-pauli-basis-observables", IntroPauliBasisObserablesNode);
};
