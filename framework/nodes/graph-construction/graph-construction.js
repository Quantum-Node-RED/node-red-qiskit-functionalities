module.exports = function (RED) {
  function GraphConstructionNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      // Parse the adjacency matrix from the config
      let matrix = config.matrix ? config.matrix : [];

      // Ensure the payload is initialized
      if (!msg.payload) {
        msg.payload = {};
      }

      // Add graph data to the payload
      msg.payload.graph = {
        adjacency_matrix: matrix,
      };
      node.send(msg);
    });
  }
  RED.nodes.registerType("graph-construction", GraphConstructionNode);
};
