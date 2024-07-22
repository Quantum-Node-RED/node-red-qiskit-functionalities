module.exports = function (RED) {
  function hamiltonianPauliNode(config) {
    RED.nodes.createNode(this, config);

    this.hamiltonianPauli = config.hamiltonianPauli;
    this.hamiltonianCoeffs = config.hamiltonianCoeffs;

    var node = this;
    node.on('input', function (msg) {
      msg.payload = {
        hamiltonianPauli: node.hamiltonianPauli,
        hamiltonianCoeffs: node.hamiltonianCoeffs
      }
      node.send(msg);
    });
  }
  RED.nodes.registerType("hamiltonianPauli", hamiltonianPauliNode);
}