import sys
import json
import numpy as np
from qiskit import QuantumCircuit
from code_component_dependency import Code_Component_Dependency as Table
from code_component import Code_Component, snippets
from import_table import import_table

def generate_qiskit_code(component, import_statements, functions, calling_code, defined_functions):
    code_obj = snippets.get(component.get("name"))
    if code_obj is not None:
        try:
            # Format import statements and add them to the set if they exist
            if code_obj.import_statement:
                for import_key in code_obj.import_statement:
                    formatted_import = import_table[import_key].format(**component.get("parameters", {})).strip()
                    if formatted_import not in import_statements:
                        import_statements.add(formatted_import)

            # Format function definitions and add them to the set if they exist and haven't been added before
            if code_obj.function and code_obj.function not in defined_functions:
                formatted_function = code_obj.function.format(**component.get("parameters", {})).strip()
                functions.add(formatted_function)
                defined_functions.add(code_obj.function)  # Mark the function as defined

            # Generate the calling function code
            calling_code += code_obj.calling_function.format(**component.get("parameters", {})).strip() + "\n"

        except KeyError as e:
            return f"[Error] Missing parameter {e} for component: {component.get('name')}\n"
    else:
        return f"[Error] Code not found for component: {component.get('name')}\n"
    return calling_code

def traverse_structure(structure, import_statements, functions, calling_code, defined_functions):
    has_circuit_begin = False
    # circuit_name = None
    for index, component in enumerate(structure):
        compoment_name = component.get("name")
        if compoment_name == "root":
            if component.get("code"):
                calling_code += component.get("code")
        elif compoment_name == "Quantum_Circuit_Begin":
            calling_code += f"# Quantum Circuit Begin {component.get('parameters').get('circuit_name')}\n"
            # circuit_name = component.get("parameters").get('circuit_name')
            has_circuit_begin = True
            calling_code = generate_qiskit_code(component, import_statements, functions, calling_code, defined_functions)
        elif compoment_name == "Quantum_Circuit_End":
            if not has_circuit_begin:
                calling_code += f"[Error] Circuit End mismatch\n"
                return calling_code
            calling_code += "# Quantum Circuit End\n"
            has_circuit_begin = False
        elif compoment_name == "qbit":
            continue
        else:
            calling_code = generate_qiskit_code(component, import_statements, functions, calling_code, defined_functions)
        print(f"Code: pass {index}\n" + calling_code + "\n", file=sys.stderr)
    return calling_code

if __name__ == "__main__":
    input_json = sys.argv[1]
    data = json.loads(input_json)

    import_statements = set()
    functions = set()
    calling_code = ""
    defined_functions = set()  # Set to track already defined functions

    calling_code = traverse_structure(data['structure'], import_statements, functions, calling_code, defined_functions)

    # Join the import statements, functions, and calling code into a single code string
    import_code = "\n".join(import_statements)
    function_code = "\n\n".join(functions)
    full_code = f"{import_code}\n\n{function_code}\n\n{calling_code}"

    result = {
        "code": full_code,
    }

    print(json.dumps(result))
