const component = require("../../component.js");
const constants = require("../../constants.js");
module.exports = function (RED) {
  function Circuit_Loop_Begin_Node(config) {
    RED.nodes.createNode(this, config);
    var node = this;
    node.on('input', function (msg) {
      msg.payload = msg.payload || {};
      node.context().flow.get("loop_expected_qubit", 0);
      currentNode=msg.payload.currentNode;
      const circuit_name = node.context().flow.get(constants.CIRCUIT_NAME);
      const connectedPaths = node._wireCount || 0;
      const expectedQubits = node.context().flow.get("expectedQubits");
      const iterations=parseInt(config.iterations || 0);


      //If the current node is a qubit or a gate,you need to aggreate the paths (Case 2,Case 4,Case 6,Case 7)
      if (currentNode.name==constants.QUBITS_COMPONENT_NAME || /_gate$/.test(currentNode.name)){
        component.aggregatePaths(type=constants.TYPE_CIRCUIT_LOOP_BEFORE_BEGIN,expectedQubits,circuit_name,connectedPaths,node,msg,iterations);
        node.context().flow.set("has_circuit_loop",true);
      }
      
      // If the current node is Quantum Circuit Begin, there are no paths to aggregate (Case 1,Case 3,Case 5)
      else if (currentNode.name==constants.QUANTUM_CIRCUIT_BEGIN_COMPONENT_NAME){
        node.context().flow.set(constants.EXPECTED_QUBITS, 0);
        if (msg.payload && msg.payload.structure) {
          for (let i = 0; i < msg.payload.structure.length; i++) {
            if (msg.payload.structure[i].name === constants.QUANTUM_CIRCUIT_BEGIN_COMPONENT_NAME) {
              msg.payload.structure[i].parameters.num_qbits = connectedPaths; 
              msg.payload.structure[i].parameters.num_cbits = connectedPaths;
              break;
            }
          }
        }
        const Circuit_Loop_Begin_component = new component.Component(
          constants.CIRCUIT_LOOP_BEGIN_COMPONENT_NAME,
          { circuit_name: circuit_name,
            num_qbits: connectedPaths,
            iterations:iterations
          }
        );
        component.addComponent(msg, Circuit_Loop_Begin_component);
        node.context().flow.set("has_circuit_loop",true);
        node.send(msg);
      }

    });
  }
    
  RED.nodes.registerType("Circuit_Loop_Begin", Circuit_Loop_Begin_Node);
};
