const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function forBeginNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const times = config.times;
    const var1 = config.var1;
    const var2 = config.var2;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      const for_begin_component = new component.Component("for_begin",{});
      if (times) {
        for_begin_component.parameters["times"] = times;
      }
      if (var1 && var1 !== "" && var2 && var2 !== "") {
        for_begin_component.parameters["var1"] = var1;
        for_begin_component.parameters["var2"] = var2;
      }
      for_begin_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, for_begin_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("for_begin", forBeginNode);
}