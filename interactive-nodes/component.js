const constants = require("./constants.js");

class Component {
  constructor(name, parameters = {}) {
    this.name = name;
    this.parameters = parameters;
    this.children = [];
  }

  addChild(child) {
    this.children.push(child);
  }

  toJSON() {
    return {
      name: this.name,
      parameters: this.parameters,
      children: this.children.map((child) => child.toJSON())
    };
  }
}

function addComponentasChild(msg, newNode) {
  if (!msg.payload.structure) {
    // If no structure exists, create a new root
    root = new Component("root", {});
    msg.payload.structure = [];
    msg.payload.structure.push(root);
    msg.payload.structure.push(newNode);
    msg.payload.currentNode = newNode;
    msg.payload.parentofCurrentNode = root;
    msg.payload.no_of_components = msg.payload.no_of_components + 1;
  }

  if (msg.payload.currentNode) {
    // Add the new node as a child of the current node
    msg.payload.currentNode.addChild(newNode);
    // Update the current node to the newly added node
    msg.parentofCurrentNode = msg.payload.currentNode;
    // Update the parent of the current node
    msg.payload.currentNode = newNode;
    // Increment the number of components
    msg.payload.no_of_components = msg.payload.no_of_components + 1;
  } else {
    // If there's no current node, add to the list of structure
    msg.payload.structure.push(newNode);
    // Update the current node to the newly added node
    msg.payload.currentNode = newNode;
    // Update the parent of the current node
    msg.payload.parentofCurrentNode = null; //is this fine?
    // Increment the number of components
    msg.payload.no_of_components = msg.payload.no_of_components + 1;
  }
}

function addComponent(msg, newNode) {
  if (!msg.payload.structure) {
    // If no structure exists, create a new root
    root = new Component("root", {});
    msg.payload.structure = [];
    msg.payload.structure.push(root);
    msg.payload.structure.push(newNode);
    msg.payload.currentNode = newNode;
    msg.payload.parentofCurrentNode = root;
    msg.payload.no_of_components = msg.payload.no_of_components + 1;
  }

  if (msg.payload.currentNode) {
    //Add to the list of structure
    msg.payload.structure.push(newNode);
    // Update the current node to the newly added node
    msg.payload.parentofCurrentNode = msg.payload.currentNode;
    // Update the parent of the current node
    msg.payload.currentNode = newNode;
    // Increment the number of components
    msg.payload.no_of_components = msg.payload.no_of_components + 1;
  } else {
    // If there's no current node, add to the list of structure
    msg.payload.structure.push(newNode);
    // Update the current node to the newly added node
    msg.payload.currentNode = newNode;
    // Update the parent of the current node
    msg.payload.parentofCurrentNode = null; //is this fine?
    // Increment the number of components
    msg.payload.no_of_components = msg.payload.no_of_components + 1;
  }
}

function addGateComponentasChild(msg, newNode) {
  if (!msg.payload.structure) {
    // If no structure exists, create a new root
    // If we are to add this newNode to the root can cause a weird structure, like gate component being child of root
    root = new Component("root", {});
    msg.payload.structure = [root];
    msg.payload.currentNode = root;
    msg.payload.parentofCurrentNode = root;
    msg.payload.no_of_components = 0;
  }

  if (msg.payload.currentNode) {
    let targetNode = msg.payload.currentNode;
    // Check if the current node is a gate
    if (msg.payload.currentNode.name.endsWith("_gate")) {
      // If it's a gate, set the target to the parent of the current node
      targetNode = msg.payload.parentofCurrentNode || msg.payload.structure[0]; // Default to root if no parent
    }

    // Add the new node as a child of the target node
    targetNode.addChild(newNode);

    // Update the current node to the newly added node
    msg.payload.parentofCurrentNode = targetNode;
    msg.payload.currentNode = newNode;

    // Increment the number of components
    msg.payload.no_of_components = msg.payload.no_of_components + 1;
  } else {
    // If there's no current node, add to the root of the structure
    msg.payload.structure[0].addChild(newNode);
    msg.payload.currentNode = newNode;
    msg.payload.parentofCurrentNode = msg.payload.structure[0];
    msg.payload.no_of_components = msg.payload.no_of_components + 1;
  }
}

function aggregatePaths(type, expectedQubits, circuit_name, connectedPaths, node, msg, iterations = null) {
  if (expectedQubits === null || expectedQubits === undefined) {
    node.error(
      "expectedQubits not initialized. Ensure Quantum_Circuit_Begin/Circuit_Begin node is setting this correctly."
    );
    return;
  }

  let state = node.context().flow.get("executionState") || {
    receivedQubits: 0,
    structure: [],
    sequenceComponents: [],
    sortedComponents: []
  };

  if (state.receivedQubits === 0) {
    state.structure = [];
  }

  const has_circuit_loop = node.context().flow.get("has_circuit_loop");
  let collecting = false;

  // First Qubit is also the Last Qubit
  if (state.receivedQubits === 0 && state.receivedQubits === expectedQubits - 1) {
    let endComponent = null;
    if (type === constants.TYPE_CIRCUIT_LOOP_BEFORE_BEGIN) {
      endComponent = new Component(
        constants.CIRCUIT_LOOP_BEGIN_COMPONENT_NAME,
        { circuit_name: circuit_name, num_qbits: connectedPaths, iterations: iterations }
      );
    } else if (type === constants.TYPE_CIRCUIT_LOOP) {
      endComponent = new Component(
        constants.CIRCUIT_LOOP_END_COMPONENT_NAME,
        { circuit_name: circuit_name, num_qbits: connectedPaths }
      );
    } else if (type === constants.TYPE_QUANTUM_CIRCUIT) {
      endComponent = new Component(
        constants.QUANTUM_CIRCUIT_END_COMPONENT_NAME,
        { circuit_name: circuit_name }
      );
    }
    msg.payload.structure.push(endComponent);
    node.send(msg);
  }

  // First Qubit Logic
  else if (state.receivedQubits === 0) {
    for (let component_ of msg.payload.structure) {     
      if (type === constants.TYPE_CIRCUIT_LOOP_BEFORE_BEGIN) {
        if (component_.name === constants.CIRCUIT_LOOP_BEGIN_COMPONENT_NAME &&
            component_.parameters.circuit_name === circuit_name) {
          break;
        }
      } else if (type === constants.TYPE_CIRCUIT_LOOP) {
        if (component_.name === constants.CIRCUIT_LOOP_END_COMPONENT_NAME &&
            component_.parameters.circuit_name === circuit_name) {
          break;
        }
      } else if (type === constants.TYPE_QUANTUM_CIRCUIT) {
        if (component_.name === constants.QUANTUM_CIRCUIT_END_COMPONENT_NAME &&
            component_.parameters.circuit_name === circuit_name) {
          break;
        }
      }
      if (component_.parameters.hasOwnProperty("sequence_no")) {
        state.sequenceComponents.push(component_);
      }
      else{
        state.sortedComponents.push(component_);
      }
    }
  }

  // Last Qubit Logic
  else if (state.receivedQubits === expectedQubits - 1) {
    for (let component_ of msg.payload.structure) {
      if (type === constants.TYPE_CIRCUIT_LOOP_BEFORE_BEGIN) {
        if (component_.name === constants.QUANTUM_CIRCUIT_BEGIN_COMPONENT_NAME &&
            component_.parameters.circuit_name === circuit_name) {
          collecting = true;
          continue;
        }
      } else if (type === constants.TYPE_CIRCUIT_LOOP) {
        if (component_.name === constants.CIRCUIT_LOOP_BEGIN_COMPONENT_NAME &&
            component_.parameters.circuit_name === circuit_name) {
          collecting = true;
          continue;
        }
      } else if (type === constants.TYPE_QUANTUM_CIRCUIT) {
        if ((!has_circuit_loop && component_.name === constants.QUANTUM_CIRCUIT_BEGIN_COMPONENT_NAME &&
             component_.parameters.circuit_name === circuit_name) ||
            (has_circuit_loop && component_.name === constants.CIRCUIT_LOOP_END_COMPONENT_NAME &&
             component_.parameters.circuit_name === circuit_name)) {
          collecting = true;
          continue;
        }
      }

      if (collecting) {
        if (component_.parameters.hasOwnProperty("sequence_no")) {
          state.sequenceComponents.push(component_);
        }
        else{
          state.sortedComponents.push(component_);
        }
      }
    }

    has_no_defined_sequence=[];
    final_sequence=[];
    for (let component_ of state.sequenceComponents) {
      if (component_.parameters["sequence_no"] === null || component_.parameters["sequence_no"] === undefined || component_.parameters["sequence_no"] === ""){
        has_no_defined_sequence.push(component_);
      }
      else{
        final_sequence.push(component_);
      }
    }
    // Sort the components with a sequence number
    final_sequence.sort((a, b) => a.parameters.sequence_no - b.parameters.sequence_no);
    state.structure = [...state.sortedComponents, ...has_no_defined_sequence, ...final_sequence];

    let endComponent = null;

    if (type === constants.TYPE_CIRCUIT_LOOP_BEFORE_BEGIN) {
      endComponent = new Component(
        constants.CIRCUIT_LOOP_BEGIN_COMPONENT_NAME,
        { circuit_name: circuit_name, num_qbits: connectedPaths, iterations: iterations }
      );
    } else if (type === constants.TYPE_CIRCUIT_LOOP) {
      endComponent = new Component(
        constants.CIRCUIT_LOOP_END_COMPONENT_NAME,
        { circuit_name: circuit_name, num_qbits: connectedPaths }
      );
    } else if (type === constants.TYPE_QUANTUM_CIRCUIT) {
      endComponent = new Component(
        constants.QUANTUM_CIRCUIT_END_COMPONENT_NAME,
        { circuit_name: circuit_name }
      );
    }

    state.structure.push(endComponent);


    let new_payload = {};
    new_payload.structure = state.structure;
    new_payload.currentNode = endComponent;
    msg.payload = new_payload;

    // Reset flow context after completing the execution
    node.context().flow.set("expectedQubits", type === "quantumCircuit" ? null : 0);
    node.context().flow.set(constants.CIRCUIT_NAME, type === "quantumCircuit" ? null : node.context().flow.get(constants.CIRCUIT_NAME));
    node.context().flow.set("executionState", null);
    if (type === "quantumCircuit") {
      node.context().flow.set("has_circuit_loop", null);
    }

    node.send(msg);
    return; // Exit after sending the last qubit
  }

  // Middle Qubit Logic
  else {
    for (let component_ of msg.payload.structure) {
      if (type === constants.TYPE_CIRCUIT_LOOP_BEFORE_BEGIN) {
        if (component_.name === constants.QUANTUM_CIRCUIT_BEGIN_COMPONENT_NAME &&
            component_.parameters.circuit_name === circuit_name) {
          collecting = true;
          continue;
        }
      } else if (type === constants.TYPE_CIRCUIT_LOOP) {
        if (component_.name === "Circuit_Loop_Begin" &&
            component_.parameters.circuit_name === circuit_name) {
          collecting = true;
          continue;
        }
      } else if (type === constants.TYPE_QUANTUM_CIRCUIT) {
        if ((!has_circuit_loop && component_.name === constants.QUANTUM_CIRCUIT_BEGIN_COMPONENT_NAME &&
             component_.parameters.circuit_name === circuit_name) ||
            (has_circuit_loop && component_.name === constants.CIRCUIT_LOOP_END_COMPONENT_NAME &&
             component_.parameters.circuit_name === circuit_name)) {
          collecting = true;
          continue;
        }
      }
      if (type === constants.TYPE_CIRCUIT_LOOP_BEFORE_BEGIN &&
          component_.name === constants.CIRCUIT_LOOP_BEGIN_COMPONENT_NAME &&
          component_.parameters.circuit_name === circuit_name) {
        break;
      } else if (type === constants.TYPE_CIRCUIT_LOOP &&
                 component_.name === constants.CIRCUIT_LOOP_END_COMPONENT_NAME &&
                 component_.parameters.circuit_name === circuit_name) {
        break;
      } else if (type === constants.TYPE_QUANTUM_CIRCUIT &&
                 component_.name === constants.QUANTUM_CIRCUIT_END_COMPONENT_NAME &&
                 component_.parameters.circuit_name === circuit_name) {
        break;
      }
      if (collecting) {
        if (component_.parameters.hasOwnProperty("sequence_no")) {
          state.sequenceComponents.push(component_);
        }
        else{
          state.sortedComponents.push(component_);
        }
      }
    }
  }

  // Increment the received qubits counter and save the state
  state.receivedQubits += 1;
  node.context().flow.set("executionState", state);
}


module.exports = {
  Component,
  addComponentasChild,
  addComponent,
  addGateComponentasChild,
  aggregatePaths
};
