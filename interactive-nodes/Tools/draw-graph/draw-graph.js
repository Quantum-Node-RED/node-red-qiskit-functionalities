const component = require("../../component.js");

module.exports = function (RED) {
  function drawGraphNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      msg.payload = msg.payload || {};

      // Add the graph construction component
      const draw_graph_component = new component.Component("draw_graph", {});
      draw_graph_component.parameters["variable"] = config.variable;
      draw_graph_component.parameters["matrix"] = config.matrix;
      component.addComponent(msg, draw_graph_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("draw-graph", drawGraphNode);
};
