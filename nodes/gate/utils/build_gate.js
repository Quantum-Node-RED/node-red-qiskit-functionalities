module.exports = function (RED) {
  function BuildGateNode(config) {
    RED.nodes.createNode(this, config);
    this.gates = config.gates;
    var node = this;
    node.on("input", async function (msg) {

      const newMsg = {
        payload: {
          gates: node.gates 
        }
      };
      node.send(newMsg);
    });
  }
  RED.nodes.registerType("Build-Gate", BuildGateNode);
};
