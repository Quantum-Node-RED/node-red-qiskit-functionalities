module.exports = function (RED) {
  function QAOACircuit(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.option = config.option;

    node.on("input", function (msg) {
      // Ensure the payload is initialized
      if (!msg.payload) {
        msg.payload = {};
      }
      // Add optimizer data to the JSON object
      msg.payload.algorithm = "QAOA"; // Example: COBYLA, SPSA, etc.
      node.send(msg);
    });
  }
  RED.nodes.registerType("QAOA-Circuit", QAOA);
};
