import sys
import json
import numpy as np
from qiskit import QuantumCircuit
from code_component_dependency import Code_Component_Dependency as Table
from code_component import Code_Component 

def generate_qiskit_code(data, num_qubits, on_qbit):
    name = data['name']
    parameters = data.get('parameters', {})
    code = ""
    # TODO: accept many circuits
    circuit_name = "qc_0"

    if name == "Quantum_Circuit_Begin":
        code += Code_Component.Quantum_Circuit_Begin.format(circuit_name=circuit_name, num_qubits=num_qubits)
    # TODO: decide which is target bit
    elif name == "CX_gate":
        code += Code_Component.CX_gate.format(circuit_name=circuit_name, qbit1=on_qbit-1, qbit2=on_qbit)
    elif name == "CZ_gate":
        code += Code_Component.CZ_gate.format(circuit_name=circuit_name, qbit1=on_qbit-1, qbit2=on_qbit)
    # TODO: decide theta and phi
    elif name == "CU_gate":
        code += Code_Component.CU_gate.format(circuit_name=circuit_name, theta=1/2, phi=1/2, lam=1/2, qbit1=on_qbit-1, qbit2=on_qbit)
    elif name == "H_gate":
        code += Code_Component.H_gate.format(circuit_name=circuit_name, qbit=on_qbit)
    elif name == "RX_gate":
        code += Code_Component.RX_gate.format(circuit_name=circuit_name, theta=1/2, qbit=on_qbit)
    elif name == "RZ_gate":
        code += Code_Component.RZ_gate.format(circuit_name=circuit_name, theta=1/2, qbit=on_qbit)
    elif name == "RY_gate":
        code += Code_Component.RY_gate.format(circuit_name=circuit_name, theta=1/2, qbit=on_qbit)
    elif name == "SX_gate":
        code += Code_Component.SX_gate.format(circuit_name=circuit_name, qbit=on_qbit)
    elif name == "X_gate":
        code += Code_Component.X_gate.format(circuit_name=circuit_name, qbit=on_qbit)
    # Add other gates similarly
    elif name == "Quantum_Circuit_End":
        code += "# Quantum Circuit End"
    
    return code


def traverse_structure(structure, num_qubits):
    code_lines = []
    for node in structure:
        code_lines.append(generate_qiskit_code(node, num_qubits, -1))
        if 'children' in node and node['children']:
            on_qbit = node['parameters']['id']
            for child in node['children']:
                code_lines.append(generate_qiskit_code(child, num_qubits, on_qbit))
    return "\n".join(code_lines)

if __name__ == "__main__":
    json_file_path = "./interactive-nodes/test.json"
    with open(json_file_path, 'r') as j:
        data = json.loads(j.read())

    # input_json = sys.argv[1]
    # data = json.loads(input_json)

    num_qubits = max(node['parameters']['id'] for node in data['structure'] if node['name'] == 'qbit') + 1
    generated_code = Code_Component.code_import(data)
    generated_code += traverse_structure(data['structure'], num_qubits)

    print(generated_code)
    