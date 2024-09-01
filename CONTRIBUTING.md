# Contributing

## Qiskit Demonstration Flows

The Qiskit Documentation Flow is encapsulated from the [Qiskit official documentation](https://docs.quantum.ibm.com/). To contribute to this section, please follow these steps:

1. Each flow represents a module, or chapter, from the Qiskit official documentation, while each node corresponds to a step required to complete that module. You can decide the range of the step length in the original text according to your own understanding. These nodes should be placed in the `Learning/nodes/` directory, and paths should be created for them based on the hierarchical structure of the original article. For example, in the original text, the step "Change order in Qiskit" from the ["Bit-Ordering in the Qiskit SDK"](https://docs.quantum.ibm.com/guides/bit-ordering) section is placed in `Learning/nodes/Circuit-And-Operators/Build-Circuit-With-The-Qiskit-SDK/Bit-Ordering-In-The-Qiskit-SDK/Change-Ordering-In-Qiskit/Change_ordering_in_qiskit.js`

2. When building a node, please refer to [the official Node-RED documentation](https://nodered.org/docs/creating-nodes/first-node). The description in the node should include a textual introduction for the corresponding steps, the required code snippet, an explanation of the code, and the node's input and output. This information should be placed in the node's Information sidebar.

3. Since Node-RED cannot directly run Python code snippets, you will need to create an additional `.py` file and call PythonShell in the node's JavaScript to execute this `.py` file. The output from the .py file should be added to `msg.payload.result`. If the output is an image, connect an image output node after the node; if the output is text, connect a debug node.

4. If a node does not contain a code snippet, it should be treated as an information node. An information node serves only as a textual description and does not execute any code independently. The color of the information node should be set to "dddddd" and use a white info icon as its symbol.

5. Once you have completed all the nodes, connect them sequentially to form a flow. The nodes in this flow should have the same category name and consistent names. At the beginning of the flow, use Node-RED's built-in inject node to inject a message and trigger the flow. Between each node, add a "Next" node, which can be found in the 'Learning Functional Nodes' category, to control the flow, allowing it to execute step-by-step and generate the output accordingly.

6. When your flow is complete, it should be exported in JSON format and named after the corresponding chapter in orignal text. The flow should be placed in the `Learning/flows` directory.

## Interactive Node Framework

To contribute in this Interactive Node Frameowork part, you need to understand certain files under the interactive-nodes directory, as follows:

### component.py:

This file contributes a `Component` class and several utility functions to manage hierarchical structures, particularly useful for representing and constructing quantum circuits or similar workflows.

The **Component** class is a foundational building block that represents a node in a hierarchical structure. It includes:

- **`name`**: The name of the component.
- **`parameters`**: A dictionary of parameters associated with the component.
- **`children`**: An array to hold child components, allowing for nested structures.

The class also provides a **`toJSON`** method to serialize the component and its children into a JSON-compatible format.

Several utility functions are provided to facilitate the dynamic construction and manipulation of hierarchical structures:

- **`addComponent`**: Adds a new component to the structure, setting it as the current node.
- **`addComponentAsChild`**: Adds a new component as a child of the current node and updates the structure accordingly.
- **`addGateComponentAsChild`**: Similar to `addComponentAsChild`, but tailored for adding gate components under specific conditions.
- **`aggregatePaths`**: Aggregates and organizes components based on certain criteria, handling quantum circuit paths and sequences.

These functions ensure that the structure is built and managed dynamically, adhering to the logical requirements of the application, such as managing quantum circuits or other sequential processes.

To contribute and extend the functionality:

1. **Add New Component Types**: Extend the `Component` class or create new types by inheriting from it.
2. **Enhance Utility Functions**: Modify or add new utility functions to handle additional scenarios or complex logic.
3. **Improve Serialization**: Enhance the `toJSON` method or add new methods to support different export formats or data handling requirements.

All contributions should maintain consistency with the existing structure and naming conventions to ensure compatibility and readability.

### code_component.py

The file introduces a **Code_Component class** and a comprehensive set of predefined code snippets to facilitate the construction and manipulation of quantum circuits, as well as performing mathematical operations relevant to quantum computing workflows.

**The `Code_Component` class** is designed to encapsulate a quantum circuit component or operation. It includes the following attributes:

- **`import_statement`**: Specifies necessary imports for the component.
- **`function`**: (Optional) Contains the function definition for more complex operations.
- **`calling_function`**: Represents the specific code snippet or method call to execute the component's functionality.

Each code snippets mostly has a single responsibilty. Contributors can extend this system by adding new Code_Component instances to the snippets dictionary, adhering to the existing structure to maintain compatibility and coherence within the codebase.

### code_generator.py

This file dynamically generates Qiskit code based on a structured input, validates parameters, and handles code execution, error management, and visualization.

Key Functions:

- **`validate_parameters(component_name, parameters)`**: Validates the parameters for a given component against predefined schemas to ensure correct types and presence of required parameters.
- **`generate_qiskit_code(component, import_statements, functions, calling_code, defined_functions)`**: Generates Qiskit code for a specified component, including import statements, function definitions, and method calls, formatted with the provided parameters.
- **`traverse_structure(structure, import_statements, functions, calling_code, defined_functions)`**: Iterates through a hierarchical structure of components to generate the full Qiskit code, handling different component types, loops, and conditions within quantum circuits.
- **`generate_import_statements(import_statements)`**: Generates a properly formatted string of Python import statements required for the Qiskit code, managing both single imports and imports with aliases.
- **`process_component_with_condition(component, conditions, parameters, reps, iteration_index, calling_code)`**: Processes a component with specific conditions, dynamically modifying parameters based on loops or other iterative structures.

To contribute and enhance the functionality:

- **Add New Component Handlers**: Extend the `generate_qiskit_code` and `traverse_structure` functions to handle additional quantum components or custom logic.
- **Improve Error Handling**: Enhance error detection and reporting mechanisms for more robust feedback.
- **Optimize Code Generation**: Refactor and optimize the code generation process for better performance and readability.
- **Expand Validation**: Introduce more comprehensive validation schemas to cover additional use cases or parameter types.

### code_component_dependency.py

This file contributes a **Component_Dependency class** that facilitates optimized import management by defining specific module imports required for various quantum computing components. The goal is to avoid wildcard imports and instead import only the necessary modules, enhancing both performance and readability.

The Component_Dependency class provides a structured mapping of component names to their respective modules and optional aliases. Each entry in the class specifies:

- **Component Name**: The name of the component, corresponding to a specific function or element in quantum computing.
- **Modules and Aliases**: A list defining the exact module path required for the component and an optional alias to simplify usage in the code.

You can contribute by adding more new import or update import accordingly when adding or updating a component.

### params_schemas.py

This file defines a **schemas** dictionary that outlines the expected parameters and their types for various quantum circuit components. These schemas are crucial for validating the input parameters during quantum circuit code generation, ensuring that each component is configured correctly before execution.

The **schemas** dictionary maps each quantum component or operation to a set of expected parameters along with their data types. Each entry in the dictionary ensures that the corresponding component receives the correct inputs, preventing runtime errors and improving the robustness of the quantum circuit generation process.

You can contribute by adding

### Other folders:

There are many folders within the interactive-nodes that separate each category as a directory of the nodes. This includes:

- **Algorithms**: Contains all the quantum algorithms node such as QAOA.
- **Flow**: Contains node that represent flow programming such as Start and End node.
- **Functions**: Contains the quantum operation and transformation in Qiskit such as Sparse Pauli Operator.
- **Gates**: Contains the quantum gates within the quantum circuit such as Hadamard Gate.
- **Maths**: Contains mathematic operations.
- **Programming**: Contains flexible programming node such as a node to add a snipper of Python code as part of the flow.
- **Quantum-Circuit**: Contains all the necessary node to build a quantum circuit.
- **Tools**: Contains all the necessary utility to support the flow such as drawing circuit.

If you want to add a new node or component, you can add it to these categories.

## Adding new node or component to the Interactive Node Framework

To add new node or component, you can follow these steps:

1. Choose a category or directory of the node you think your node will be in. You can add new category if desired.
2. Create a directory of that node with the node name under the category directory and subsequently create HTML and JavaScript file under the created node name directory.
3. Add the code snippet of that component in code_component.py
4. Add new import statement if an import statement for the code snippet added is not already exist in code_component_dependency.py.
5. Add a new node as a path in package.json. Ensure that all the spelling reflect the name of the node you registered within HTML and JavaScript file.
6. Run `node-red` command and your node should be your Node-RED workspace editor inside the node palette.
