module.exports = function (RED) {
  function ParameterSettingNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      // Implement parameter setting logic
      msg.parameters = config.parameters; // Example: { reps: 2, seed: 10598 }
      node.send(msg);
    });
  }
  RED.nodes.registerType("parameter-setting", ParameterSettingNode);
};
