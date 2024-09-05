const component=require('../../component.js');
const constants=require('../../constants.js');
module.exports = function (RED) {
  function local_simulatorNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const local_simulator_component = new component.Component("local_simulator",{});
      local_simulator_component.parameters["circuit_name"] = config.circuit_name;
      local_simulator_component.parameters["shots"] = config.shots;
      component.addComponent(msg, local_simulator_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("local_simulator", local_simulatorNode);
}