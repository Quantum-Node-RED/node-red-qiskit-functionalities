const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function drawNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      let current_node_name=msg.payload.currentNode;
      if (current_node_name.name==constants.QUANTUM_CIRCUIT_END_COMPONENT_NAME){
        current_node_name=current_node_name.parameters[constants.CIRCUIT_NAME];
      }
      else{
        current_node_name="";
      }
      msg.payload = msg.payload || {};
      const draw_component = new component.Component("draw",{});
      draw_component.parameters["output_type"] = config.output_type?config.output_type:"mpl";
      draw_component.parameters[constants.CIRCUIT_NAME] = config.circuit_name?config.circuit_name:current_node_name?current_node_name:"";
      component.addComponent(msg, draw_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("draw", drawNode);
}