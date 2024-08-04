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
      // qubit: qubit(s) to measure.
      // cbit: classical bit(s) to place the measurement result(s) in.
      measure_component.parameters["qbit"] = [qbits, cbits];
      measure_component.parameters[constants.CIRCUIT_NAME] = node.context().flow.get(constants.CIRCUIT_NAME);
      component.addComponent(msg, measure_component);

      // Send the message onward
      node.send(msg);
    });
  }

  RED.nodes.registerType("measure_component", measureNode);
};
