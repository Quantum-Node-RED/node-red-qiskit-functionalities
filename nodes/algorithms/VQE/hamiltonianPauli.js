module.exports = function (RED) {
  function hamiltonianPauliNode(config) {
    RED.nodes.createNode(this, config);

    this.paulis = config.paulis;

    var node = this;
    node.on('input', function (msg) {
      msg.payload = {
        numQubits: msg.payload.numQubits,
        paulis: node.paulis
      }
      node.send(msg);
    });
  }
  RED.nodes.registerType("hamiltonianPauli", hamiltonianPauliNode);
}