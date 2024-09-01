const component = require("../../component.js");

module.exports = function (RED) {
  function define_parameterNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    // Parse the parameters JSON
    let parameters = JSON.parse(config.parameters);
    node.on("input", function (msg) {
      msg.payload = msg.payload || {};

      // Flatten the parameters JSON into a single list (initial_point format)
      let initial_param = [];
      let numberOfParameter = 0;
      if (config.mode == "customize") {
        for (let key in parameters) {
          if (parameters.hasOwnProperty(key)) {
            numberOfParameter += 1;
            initial_param = initial_param.concat(parameters[key]);
          }
        }
      } else {
        numberOfParameter = config.numberOfParams;
      }

      const define_parameter_component = new component.Component(
        "define_parameter",
        {}
      );

      define_parameter_component.parameters["variable"] = config.variable;
      define_parameter_component.parameters["parameters"] =
        JSON.stringify(parameters);
      define_parameter_component.parameters["number_of_parameter"] =
        numberOfParameter;
      define_parameter_component.parameters["number_of_reps"] =
        config.numberOfRepetitions;
      define_parameter_component.parameters["initial_param"] = initial_param;
      define_parameter_component.parameters["mode"] = config.mode;

      component.addComponent(msg, define_parameter_component);
      node.send(msg);
    });
  }

  RED.nodes.registerType("define_parameter", define_parameterNode);
};
