import sys
import json
import numpy as np
from qiskit import QuantumCircuit
from code_component_dependency import Code_Component_Dependency as Table
from code_component_v2 import Code_Component

def generate_qiskit_code(component):
    code = Code_Component.snippets.get(component.get("name"))
    if code is not None:
        try:
            code = code.format(**component.get("parameters", {}))
        except KeyError as e:
            return f"[Error] Missing parameter {e} for component: {component.get('name')}\n"
    else:
        return f"[Error] Code not found for component: {component.get('name')}\n"
    return code + "\n"

def traverse_structure(structure):
    code = ""
    stack = []
    circuit_name = None
    for index, component in enumerate(structure):
        if component.get("name") == "root":
            if component.get("code"):
                code += component.get("code")
        elif component.get("name") == "Quantum_Circuit_Begin":
            code += f"# Quantum Circuit Begin {component.get('parameters').get('circuit_name')}\n"
            circuit_name = component.get("parameters").get('circuit_name')
            stack.append(circuit_name)
            code += generate_qiskit_code(component)
        elif component.get("name") == "Quantum_Circuit_End":
            try:
                name=stack.pop()
            except:
                name=None 
            if not(name):
                code += f"[Error] Circuit End mismatch\n"
            code += "# Quantum Circuit End\n"
        elif component.get("name") == "qbit":
            for child in component.get("children"):
                code += generate_qiskit_code(child)
        else:
            code += generate_qiskit_code(component)
        print(f"Code: pass {index}\n"+code + "\n")
    return code



if __name__ == "__main__":
    json_file_path = "./test.json"
    with open(json_file_path, 'r') as j:
        data = json.loads(j.read())

    # input_json = sys.argv[1]
    # data = json.loads(input_json)

    generated_code = Code_Component.code_import(data)
    generated_code += traverse_structure(data['structure'])+""

    print(generated_code)
    