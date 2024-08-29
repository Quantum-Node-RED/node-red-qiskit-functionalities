const component = require("../../component.js");
const constants = require("../../constants.js");

module.exports = function (RED) {
  function Quantum_Circuit_EndNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    node.on("input", function (msg) {
      msg.payload = msg.payload || {};
      let expectedQubits = node.context().flow.get("expectedQubits");
      let circuit_name = node.context().flow.get(constants.CIRCUIT_NAME);


      if (expectedQubits === null || expectedQubits === undefined) {
        node.error(
          "expectedQubits not initialized. Ensure Quantum_Circuit_Begin node/Circuit_Loop_End node is setting this correctly."
        );
        return;
      }

      let currentNode = msg.payload.currentNode;
      if (currentNode.name==constants.CIRCUIT_LOOP_END_COMPONENT_NAME){
        // No need to aggregate paths at  Quantum_Circuit_End as only one path is expected 
        node.context().flow.set("expectedQubits", null);
        node.context().flow.set(constants.CIRCUIT_NAME, null);
        node.context().flow.set("executionState", null); 
        node.context().flow.set("has_circuit_loop", null);

        const Quantum_Circuit_End_component = new component.Component(
          constants.QUANTUM_CIRCUIT_END_COMPONENT_NAME,
          { circuit_name: circuit_name }
        );
        component.addComponent(msg, Quantum_Circuit_End_component);
        node.send(msg);
      }

      else{
        component.aggregatePaths(type=constants.TYPE_QUANTUM_CIRCUIT,expectedQubits,circuit_name,null,node,msg);
      }
    });
  }

  RED.nodes.registerType("Quantum_Circuit_End", Quantum_Circuit_EndNode);
};

