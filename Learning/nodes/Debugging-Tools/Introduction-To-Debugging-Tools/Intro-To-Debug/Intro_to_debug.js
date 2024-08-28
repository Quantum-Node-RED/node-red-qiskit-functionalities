
module.exports = function (RED) {
  function IntroToDebugNode(config) {
    RED.nodes.createNode(this, config);

    var node = this;

    node.on('input',  async function (msg) {
      node.send(msg);
    });
  }
  RED.nodes.registerType("intro-to-debug", IntroToDebugNode);
}