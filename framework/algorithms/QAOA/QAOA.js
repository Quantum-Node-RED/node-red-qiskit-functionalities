module.exports = function (RED) {
  function QAOA(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.option = config.option;
    node.reps = config.reps;

    node.on("input", function (msg) {
      // Ensure the payload is initialized
      if (!msg.payload) {
        msg.payload = {};
      }

      // Add optimizer data to the JSON object
      msg.payload.algorithm = "QAOA";
      msg.payload.reps = node.reps;
      node.send(msg);
    });
  }
  RED.nodes.registerType("QAOA", QAOA);
};
