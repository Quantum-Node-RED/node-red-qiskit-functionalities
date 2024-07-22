module.exports = function (RED) {
  function ansatzNode(config) {
    RED.nodes.createNode(this, config);

    this.rotationLayers = config.rotationLayers;
    this.entanglementLayers = config.entanglementLayers;

    var node = this;
    node.on('input', async function (msg) {
      msg.payload = {
        numQubits: msg.payload.numQubits,
        rotationLayers: node.rotationLayers,
        entanglementLayers: node.entanglementLayers
      }
      node.send(msg);
    });
  }
  RED.nodes.registerType("ansatz", ansatzNode);
}