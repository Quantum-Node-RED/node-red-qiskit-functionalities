const component = require("../../component.js");

module.exports = function (RED) {
  function DrawGraphNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      // Parse the adjacency matrix from the config
      let matrix = config.matrix ? config.matrix : [];

      // // Add graph data to the payload
      // msg.payload.graph = {
      //   adjacency_matrix: matrix,
      // };

      msg.payload = msg.payload || {};

      // Add the graph construction component
      const draw_graph_component = new component.Component("draw_graph", {});
      component.addComponent(msg, draw_graph_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("draw-graph", DrawGraphNode);
};
