const component = require("../../component.js");
const constants = require("../../constants.js");
module.exports = function (RED) {
  function Circuit_Loop_End_Node(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      let expectedQubits = node.context().flow.get(constants.EXPECTED_QUBITS);
      let connectedPaths = node._wireCount || 0;
      let currentNode=msg.payload.currentNode;
      let circuit_name = node.context().flow.get(constants.CIRCUIT_NAME);

      if (expectedQubits === null || expectedQubits === undefined) {
        node.error(
          "expectedQubits not initialized. Ensure Circuit_Loop_Begin node is setting this correctly."
        );
        return;
      }


      if (currentNode.name==constants.CIRCUIT_LOOP_BEGIN_COMPONENT_NAME)
      {
        const Circuit_Loop_End_component = new component.Component(
          constants.CIRCUIT_LOOP_END_COMPONENT_NAME,
          { circuit_name: circuit_name,
            num_qbits: connectedPaths
          }
        );
        component.addComponent(msg, Circuit_Loop_End_component);
        node.send(msg);
      }
      else{
        component.aggregatePaths(type=constants.TYPE_CIRCUIT_LOOP,expectedQubits,circuit_name,connectedPaths,node,msg);
      }
      
    });
  }
    
  RED.nodes.registerType("Circuit_Loop_End", Circuit_Loop_End_Node);
};
