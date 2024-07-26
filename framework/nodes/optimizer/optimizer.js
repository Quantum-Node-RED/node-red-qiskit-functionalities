module.exports = function (RED) {
  function OptimizerNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.option = config.option;

    node.on("input", function (msg) {
      // Ensure the payload is initialized
      if (!msg.payload) {
        msg.payload = {};
      }
      // Add optimizer data to the JSON object
      msg.payload.optimizer = node.option; // Example: COBYLA, SPSA, etc.
      node.send(msg);
    });
  }
  RED.nodes.registerType("Optimizer", OptimizerNode);
};
