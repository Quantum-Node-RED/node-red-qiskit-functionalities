module.exports = function (RED) {
  function optimizerNode(config) {
    RED.nodes.createNode(this, config);

    this.optimizer = config.optimizer;
    this.maxiter = config.maxiter;

    var node = this;
    node.on('input', function (msg) {
      msg.payload = {
        optimizer: node.optimizer,
        maxiter: node.maxiter
      }
      node.send(msg);
    });
  }
  RED.nodes.registerType("optimizer", optimizerNode);
}