module.exports = function (RED) {
  function optimizerNode(config) {
    RED.nodes.createNode(this, config);

    this.optimizer = config.optimizer;

    var node = this;
    node.on('input', function (msg) {
      msg.payload = {
        numQubits: msg.payload.numQubits,
        paulis: msg.payload.paulis,
        rotationLayers: msg.payload.rotationLayers,
        entanglementLayers: msg.payload.entanglementLayers,
        optimizer: node.optimizer
      }
      node.send(msg);
    });
  }
  RED.nodes.registerType("optimizer", optimizerNode);
}