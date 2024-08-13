import sys
import json
import os
import subprocess
import numpy as np
from qiskit import QuantumCircuit
from code_component_dependency import Code_Component_Dependency as Table
from code_component import Code_Component, snippets
from import_table import import_table
import matplotlib.pyplot as plt
import base64
from io import BytesIO

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

def save_code_as_image_base64(code_str):
    """
    Save a given Python code string as an image and return it as a Base64-encoded string.

    Parameters:
    - code_str (str): The Python code to render as an image.

    Returns:
    - str: Base64-encoded string of the image.
    """
    # Set up the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Add the code as text to the plot
    ax.text(0.05, 0.95, code_str, fontsize=12, fontfamily='monospace', ha='left', va='top')
    
    # Remove axes
    ax.axis('off')
    
    # Save the figure to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
    
    # Close the plot to free memory
    plt.close(fig)
    
    # Encode the image in Base64
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    
    return image_base64

if __name__ == "__main__":
    input_json = sys.argv[1]
    data = json.loads(input_json)

    import_statements = set()
    functions = set()
    calling_code = ""
    defined_functions = set()

    calling_code = traverse_structure(data['structure'], import_statements, functions, calling_code, defined_functions)

    import_code = "\n".join(import_statements)
    function_code = "\n\n".join(functions)

    # Properly format the wrapped code without f-string issues
    indented_calling_code = calling_code.replace('\n', '\n    ')
    # Properly format the wrapped code with indentation
    indented_calling_code = calling_code.replace('\n', '\n    ')
    wrapped_calling_code = (
        "import traceback\n"
        "try:\n"
        f"    {indented_calling_code}\n"  # Indent the entire block by four spaces
        "except Exception as e:\n"
        "    print(f'An error occurred: {e}')\n"
        "    print(traceback.format_exc())\n"  # Add traceback information
    )
    full_code = f"{import_code}\n\n{function_code}\n\n{wrapped_calling_code}"

    # Dump the full code into a Python file
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_name = "generated_code.py"
    file_path = os.path.join(script_directory, file_name)
    try:
        with open(file_path, "w") as code_file:
            code_file.write(full_code)
    except Exception as e:
        result = {
            "error": f"Failed to create file {file_name}: {e}"
        }
        print(json.dumps(result))
        sys.exit(1)

    # Save the generated code as an image
    code_snapshot = save_code_as_image_base64(full_code)

    # Execute the Python file and capture the output
    try:
        process = subprocess.run([sys.executable, file_path], capture_output=True, text=True)
        execution_result = process.stdout + process.stderr
    except Exception as e:
        execution_result = str(e)

    result = {
        "code": full_code,
        "code_snapshot": code_snapshot,
        "result": execution_result,
    }

    # Cleanup the generated Python file
    # os.remove(file_path)

    # Cleanup the generated Python file
    # os.remove(file_name)

    print(json.dumps(result))