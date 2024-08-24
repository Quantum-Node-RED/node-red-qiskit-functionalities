const component = require("../../component.js");
module.exports = function (RED) {
  function measure_allNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const measure_all_component = new component.Component("measure_all", {});
      measure_all_component.parameters["circuit_name"] = config.circuit_name;
      measure_all_component.parameters["num_qbits"] = config.num_qbits;
      measure_all_component.parameters["num_cbits"] = config.num_cbits;
      component.addComponent(msg, measure_all_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("measure_all", measure_allNode);
};
