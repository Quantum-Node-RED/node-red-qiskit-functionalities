const component = require("../../component.js");

module.exports = function (RED) {
  function Quantum_Circuit_EndNode(config) {
    RED.nodes.createNode(this, config);
    var node = this;

    // State object to track qubits
    const state = {
      qubits: [],
      expectedQubits: 0, // Set to 0 initially to indicate it should be retrieved dynamically
      receivedQubits: 0,
    };

    node.on("input", function (msg) {
      // Retrieve the number of expected qubits from flow context if not already set
      if (state.expectedQubits === 0) {
        state.expectedQubits = node.context().flow.get("expectedQubits") || 1; // Default to 1 if not set
        node.log(`Expected Qubits retrieved: ${state.expectedQubits}`);
      }

      // Extract the qubit and its gates from the message
      const currentStructure = msg.payload.structure;
      const qubitNode = currentStructure.find(
        (node) => node.name === "Quantum_Circuit_Begin"
      ).children[0];

      // Create a qubit object
      const qubit = {
        name: qubitNode.name,
        gates: qubitNode.children.map((gateNode) => ({
          name: gateNode.name,
          parameters: gateNode.parameters,
        })),
      };

      // Add the qubit to the temporary state
      state.qubits.push(qubit);
      state.receivedQubits++;

      // Log the received qubits for debugging
      node.log(
        `Received Qubits: ${state.receivedQubits}/${state.expectedQubits}`
      );

      // Check if all expected qubits have been received
      if (state.receivedQubits === state.expectedQubits) {
        // Create the aggregated quantum circuit
        msg.payload.quantumCircuit = {
          qubits: state.qubits,
        };

        // Add the Quantum_Circuit_End component
        const Quantum_Circuit_End_component = new component.Component(
          "Quantum_Circuit_End",
          {}
        );
        component.addComponent(msg, Quantum_Circuit_End_component);

        // Send the aggregated message
        node.send(msg);

        // Reset state for next aggregation
        state.qubits = [];
        state.receivedQubits = 0;
        state.expectedQubits = 0; // Reset to force re-fetch next time
      }
    });
  }

  RED.nodes.registerType("Quantum_Circuit_End", Quantum_Circuit_EndNode);
};

// Norbu stuff

// const component =require("../../component.js");
// module.exports = function (RED) {
//     function Quantum_Circuit_EndNode(config) {
//       RED.nodes.createNode(this, config);
//       var node = this;
//       node.on('input', function (msg) {
//         msg.payload = msg.payload || {};
//         const Quantum_Circuit_End_component = new component.Component("Quantum_Circuit_End",{});
//         component.addComponent(msg,Quantum_Circuit_End_component)
//         node.send(msg);
//       });
//     }
//     RED.nodes.registerType("Quantum_Circuit_End", Quantum_Circuit_EndNode);
//   }

// const component = require("../../component.js");

// module.exports = function (RED) {
//     function Quantum_Circuit_EndNode(config) {
//         RED.nodes.createNode(this, config);
//         var node = this;

//         // Store incoming messages
//         let messages = [];
//         let expectedMessages = 3; // Number of qubits/paths

//         node.on('input', function (msg) {
//             if (msg.payload && typeof msg.payload === 'object' && Array.isArray(msg.payload.structure)) {
//                 messages.push(msg.payload);
//             } else {
//                 node.error("Received invalid payload structure", msg);
//                 return;
//             }

//             if (messages.length === expectedMessages) {
//                 try {
//                     // All messages received, merge them
//                     let mergedPayload = mergePayloads(messages);

//                     // Create new Quantum_Circuit_End component
//                     const Quantum_Circuit_End_component = new component.Component("Quantum_Circuit_End", {});

//                     // Add the Quantum_Circuit_End component to the merged structure
//                     mergedPayload.structure.push(Quantum_Circuit_End_component);
//                     mergedPayload.currentNode = Quantum_Circuit_End_component;
//                     mergedPayload.no_of_components++;

//                     // Send merged message
//                     node.send({ payload: mergedPayload });
//                 } catch (error) {
//                     node.error("Error processing messages: " + error.message, messages);
//                 } finally {
//                     // Reset messages array for next set
//                     messages = [];
//                 }
//             }
//         });
//     }

//     RED.nodes.registerType("Quantum_Circuit_End", Quantum_Circuit_EndNode);
// }

// function mergePayloads(payloads) {
//     let mergedStructure = [];
//     let seenComponents = new Set();
//     let totalComponents = 0;

//     payloads.forEach(payload => {
//         payload.structure.forEach(comp => {
//             if (!seenComponents.has(comp.name)) {
//                 seenComponents.add(comp.name);
//                 mergedStructure.push(comp);
//             } else {
//                 // If component exists, merge its children
//                 let existingComp = mergedStructure.find(c => c.name === comp.name);
//                 existingComp.children = mergeChildren(existingComp.children || [], comp.children || []);
//             }
//         });
//         totalComponents += payload.no_of_components;
//     });

//     return {
//         structure: mergedStructure,
//         currentNode: null, // This will be set to the Quantum_Circuit_End component
//         parentofCurrentNode: mergedStructure[mergedStructure.length - 1] || null,
//         no_of_components: totalComponents
//     };
// }

// function mergeChildren(existing, newChildren) {
//     newChildren.forEach(child => {
//         if (!existing.some(e => e.name === child.name)) {
//             existing.push(child);
//         } else {
//             let existingChild = existing.find(e => e.name === child.name);
//             existingChild.children = mergeChildren(existingChild.children || [], child.children || []);
//         }
//     });
//     return existing;
// }
