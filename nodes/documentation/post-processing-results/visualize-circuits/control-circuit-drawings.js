// const runPythonScript = require("../../../../pythonShell");

module.exports = function (RED) {
  function ControlCircuitDrawingsNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;
    node.info = config.info;

    
    
    node.on("input", async function (msg) {

      node.send(msg);
    });

    
  }
  RED.nodes.registerType("control-circuit-drawings", ControlCircuitDrawingsNode);
};