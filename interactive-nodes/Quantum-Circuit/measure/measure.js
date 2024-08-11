const component = require("../../component.js");
const constants = require('../../constants.js');

module.exports = function (RED) {
  function measureNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    const qbits = config.measure_qbit
    const cbits = config.cbit

    node.on("input", function (msg) {
      msg.payload = msg.payload || {};

      const measure_component = new component.Component(constants.MEASURE_COMPONENT_NAME, {});
      measure_component.parameters["qbit"] = msg.payload["qubit_id"];
      measure_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, measure_component);

      // Send the message onward
      node.send(msg);
    });
  }

  RED.nodes.registerType("measure", measureNode);
};
