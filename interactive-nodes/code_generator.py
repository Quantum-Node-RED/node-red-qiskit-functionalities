import sys
import json
import numpy as np
from qiskit import QuantumCircuit
from code_component_dependency import Code_Component_Dependency as Table
from code_component import Code_Component 

def generate_qiskit_code(data, num_qubits, on_qbit, circuit_name):
    name = data['name']
    param = data.get('parameters', {})
    code = ""

    # Circuits
    if name == "Quantum_Circuit_Begin":
        code += Code_Component.Quantum_Circuit_Begin.format(circuit_name=circuit_name, num_qubits=num_qubits)
    elif name == "measure":
        code += Code_Component.measure.format(circuit_name=circuit_name, qbit=on_qbit)
    # TODO: multiple qubit gate
    elif name == "swap":
        code += Code_Component.swap.format(circuit_name=circuit_name, qbit1=on_qbit-1, qbit2=on_qbit)
    elif name == "reset":
        code += Code_Component.reset.format(circuit_name=circuit_name, qbit=on_qbit)
    elif name == "Quantum_Circuit_End":
        code += "# Quantum Circuit End"
    # TODO: classical_register, quantum_register

    # Maths
    elif name == "matrix":
        code += Code_Component.matrix.format(var_name=param['parameters'], matrix=param['matrix'])
    # Gates
     # TODO: multiple qubit gate
    elif name == "CX_gate":
        code += Code_Component.CX_gate.format(circuit_name=circuit_name, qbit1=on_qbit-1, qbit2=on_qbit)
    elif name == "CZ_gate":
        code += Code_Component.CZ_gate.format(circuit_name=circuit_name, qbit1=on_qbit-1, qbit2=on_qbit)
    elif name == "CU_gate":
        code += Code_Component.CU_gate.format(circuit_name=circuit_name, theta=param['theta'], phi=param['phi'], lam=param['lambda'], qbit1=on_qbit-1, qbit2=on_qbit)
    elif name == "H_gate":
        code += Code_Component.H_gate.format(circuit_name=circuit_name, qbit=on_qbit)
    elif name == "RX_gate":
        code += Code_Component.RX_gate.format(circuit_name=circuit_name, theta=param['theta'], qbit=on_qbit)
    elif name == "RZ_gate":
        code += Code_Component.RZ_gate.format(circuit_name=circuit_name, theta=param['theta'], qbit=on_qbit)
    elif name == "RY_gate":
        code += Code_Component.RY_gate.format(circuit_name=circuit_name, theta=param['theta'], qbit=on_qbit)
    elif name == "SX_gate":
        code += Code_Component.SX_gate.format(circuit_name=circuit_name, qbit=on_qbit)
    elif name == "X_gate":
        code += Code_Component.X_gate.format(circuit_name=circuit_name, qbit=on_qbit)
    elif name == "barrier":
        code += Code_Component.barrier.format(circuit_name=circuit_name, qbit=on_qbit)
    elif name == "phase":
        code += Code_Component.phase.format(circuit_name=circuit_name, theta=param['theta'], qbit=on_qbit)
    elif name == "I_gate":
        code += Code_Component.I_gate.format(circuit_name=circuit_name, qbit=on_qbit)
    elif name == "U_gate":
        code += Code_Component.U_gate.format(circuit_name=circuit_name, theta=param['theta'], phi=param['phi'], lam=param['lambda'], qbit=on_qbit)
    elif name == "Toffoli_gate":
        code += Code_Component.Toffoli_gate.format(circuit_name=circuit_name, qbit1=on_qbit-2, qbit2=on_qbit-1, qbit3=on_qbit)
    elif name == "CCX_gate":
        code += Code_Component.CCX_gate.format(circuit_name=circuit_name, qbit1=on_qbit-2, qbit2=on_qbit-1, qbit3=on_qbit)
    # Tools
    elif name == "local_simulator":
        code += Code_Component.local_simulator.format(var_name=param['var_name'], simulator=param['simulator'], var_name_result=param['var_name_result'], 
                                                      circuit_name=param['circuit_name'], var_name_counts=param['var_name_counts'])
    elif name == "draw":
        code += Code_Component.draw.format(circuit_name=circuit_name, output_type=param['output_type'])
    elif name == "encode_image":
        code += Code_Component.encode_image
    elif name == "histogram":
        code += Code_Component.histogram
    
    return code


def traverse_structure(structure, num_qubits):
    code_lines = []
    for node in structure:
        circuit_name = ""
        if node['parameters'] and 'circuit_name' in node['parameters']:
            circuit_name = node['parameters']['circuit_name']
        code_lines.append(generate_qiskit_code(node, num_qubits, -1, circuit_name))
        if 'children' in node and node['children']:
            on_qbit = node['parameters']['id']
            for child in node['children']:
                code_lines.append(generate_qiskit_code(child, num_qubits, on_qbit, circuit_name))
    return "\n".join(code_lines)

if __name__ == "__main__":
    json_file_path = "./test.json"
    with open(json_file_path, 'r') as j:
        data = json.loads(j.read())

    # input_json = sys.argv[1]
    # data = json.loads(input_json)

    num_qubits = max(node['parameters']['id'] for node in data['structure'] if node['name'] == 'qbit') + 1
    generated_code = Code_Component.code_import(data)
    generated_code += traverse_structure(data['structure'], num_qubits)

    print(generated_code)
    