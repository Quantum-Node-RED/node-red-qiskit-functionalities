// const runPythonScript = require("../../../../pythonShell");

module.exports = function (RED) {
  function IntroToTranspileStageNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.name = config.name;
    node.info = config.info;

    node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });
    
    node.on("input", async function (msg) {
      node.status({ fill: "green", shape: "dot", text: "You have  learned this node." });
      node.send(msg);
    });

    node.on('close', function () {
      node.status({ fill: "red", shape: "dot", text: "You haven't learned this node yet." });
    });
  }
  RED.nodes.registerType("intro-to-transpile-stage", IntroToTranspileStageNode);
};