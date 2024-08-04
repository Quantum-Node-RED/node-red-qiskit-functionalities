const component=require('../../component.js');
module.exports = function (RED) {
  function local_simulatorNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const var_name = config.var_name
    const simulator = config.simulator
    const var_name_result = config.var_name_result
    const circuit_name = config.circuit_name
    const var_name_counts = config.var_name_counts
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const local_simulator_component = new component.Component("local_simulator",{});
      local_simulator_component.parameters["var_name"] = var_name;
      local_simulator_component.parameters["simulator"] = simulator;
      local_simulator_component.parameters["var_name_result"] = var_name_result;
      local_simulator_component.parameters["circuit_name"] = circuit_name;
      local_simulator_component.parameters["var_name_counts"] = var_name_counts;
      component.addComponent(msg, local_simulator_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("local_simulator", local_simulatorNode);
}