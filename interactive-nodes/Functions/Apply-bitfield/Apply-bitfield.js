const component = require("../../component.js");
module.exports = function (RED) {
  function apply_bitfieldNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const apply_bitfield_component = new component.Component(
        "apply_bitfield",
        {}
      );
      apply_bitfield_component.parameters["binary_vector"] = "bitfield";
      apply_bitfield_component.parameters["integer_value"] = 1;
      apply_bitfield_component.parameters["bit_length"] = 100;
      apply_bitfield_component.parameters["var_result"] = "bitfield";
      component.addComponent(msg, apply_bitfield_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType("apply_bitfield", apply_bitfieldNode);
};
