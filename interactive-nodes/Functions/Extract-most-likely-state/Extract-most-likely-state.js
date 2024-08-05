const component = require("../../component.js");
module.exports = function (RED) {
  function extract_most_likely_stateNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      const extract_most_likely_state_component = new component.Component(
        "extract_most_likely_state",
        {}
      );
      extract_most_likely_state_component.parameters["state_vector"] = "TBD";
      extract_most_likely_state_component.parameters["var_result"] =
        "extracted_state";
      component.addComponent(msg, extract_most_likely_state_component);
      node.send(msg);
    });
  }
  RED.nodes.registerType(
    "extract_most_likely_state",
    extract_most_likely_stateNode
  );
};
