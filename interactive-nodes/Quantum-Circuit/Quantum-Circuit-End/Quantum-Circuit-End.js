const component = require("../../component.js");
const constants = require('../../constants.js');
module.exports = function (RED) {
  function Quantum_Circuit_EndNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    // State object to track qubits
    const state = {
      expectedQubits: 0, // Set to 0 initially to indicate it should be retrieved dynamically
      receivedQubits: 0,
      structure:[]
    };

    node.on("input", function (msg) {
      // Retrieve the number of expected qubits from flow context if not already set
      if (state.expectedQubits === 0) {
        state.expectedQubits = node.context().flow.get("expectedQubits") || 1; // Default to 1 if not set
      }
      let circuit_name=node.context().flow.get(constants.CIRCUIT_NAME); //Get the name for the current (this) Circuit

      //Check if the qubit is the first qubit to reach the Quantum_Circuit_End
      if (state.receivedQubits === 0){
        //Extract all the components before the current (this) Quantum_Circuit_Begin 
        //Now traverse the structure of the current payload and get all the components before the current (this) Quantum_Circuit_End
        for (let component_ of msg.payload.structure){
          state.structure.push(component_);
          if (component_.name==="Quantum_Circuit_End" && component_.parameters.circuit_name === circuit_name){
            break;
          }
        }
        node.log("Payload: " + JSON.stringify(state.structure));
      }
      //For the last Qubit that reaches Quantum_Circuit_End take payload after Quantum_Circuit_Begin and add Quantum_Circuit_End
      else if (state.receivedQubits === state.expectedQubits-1){
        let collecting=false;
        for (let component_ of msg.payload.structure){
          if (component_.name==="Quantum_Circuit_Begin" && component_.parameters.circuit_name === circuit_name){
            collecting=true;
            continue;
          }
          if (collecting){
            state.structure.push(component_);
          }
        }
        //Add the Quantum_Circuit_End component
        const Quantum_Circuit_End_component = new component.Component(
          "Quantum_Circuit_End",
          {"circuit_name":circuit_name}
        );
        state.structure.push(Quantum_Circuit_End_component);
    
        //Now pass the structure to the Quantum_Circuit_End
        let new_payload={};
        new_payload.structure=state.structure;
        new_payload.currentNode=Quantum_Circuit_End_component;
        msg.payload=new_payload
        //Clear the states
        state.expectedQubits=0;
        state.receivedQubits=0;
        state.structure=[];
        node.log("Payload: " + JSON.stringify(msg.payload.structure));
        node.log("\n");

        node.send(msg);
      }
      //For the qubits that are not first and last take only the payload after the Quantum_Circuit_Begin and exclude the Quantum_Circuit_End
      else{
        let collecting=false;
        for (let component_ of msg.payload.structure){
          if (component_.name==="Quantum_Circuit_Begin" && component_.parameters.circuit_name === circuit_name){
            collecting=true;
            continue;
          }
          if (collecting){
            state.structure.push(component_);
          }
          if (component_.name==="Quantum_Circuit_End" && component_.parameters.circuit_name === circuit_name){
            break;
          }
        }
        node.log("Payload: " + JSON.stringify(state.structure));
      }
      state.receivedQubits += 1;
    }
   
    );
  }

  RED.nodes.registerType("Quantum_Circuit_End", Quantum_Circuit_EndNode);
};
