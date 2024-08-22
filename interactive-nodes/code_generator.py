import sys
import json
import os
import subprocess
from code_component import  snippets
from params_schemas import schemas
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def validate_parameters(component_name, parameters):
    if component_name in schemas:
        for param_key, param_type in schemas[component_name].items():
            if param_key not in parameters:
                return f"Missing parameter key: {param_key}"
            elif not isinstance(parameters[param_key], param_type):
                return f"Incorrect type for parameter key: {param_key}. Expected {param_type.__name__}, \
                got {type(parameters[param_key]).__name__}"
            return None

def generate_qiskit_code(component, import_statements, functions, calling_code, defined_functions):
    component_name = component.get('name')
    code_obj = snippets.get(component_name)
    if code_obj is not None:
        errors = validate_parameters(component_name, component['parameters'])
        if errors is not None:
            return f"[Error] Parameters of component {component_name} are invalid: {errors}\n"
        try:
            # Format import statements and add them to the set if they exist
            if code_obj.import_statement:
                for import_key in code_obj.import_statement:
                    formatted_import = tuple(item.format(**component.get("parameters", {})).strip() for item in import_key)
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
            return f"[Error] Missing parameter {e} for component: {component_name}\n"
    else:
        return f"[Error] Code not found for component: {component_name}\n"
    return calling_code


def traverse_structure(structure, import_statements, functions, calling_code, defined_functions):
    has_circuit_begin = False
    in_circuit_loop= False
    stack=[]
    iterations = 0
    theta_count = 0
    circuit_parameters =None
    circuit_loop_conditions=None
    for  component in structure:
        component_name = component.get("name")
        if component_name == "root":
            if component.get("code"):
                calling_code += component.get("code")
        elif component_name == "Quantum_Circuit_Begin":
            if has_circuit_begin:
                calling_code += f"[Error] Circuit Begin exist.\n"
            calling_code += f"# Quantum Circuit Begin {component.get('parameters').get('circuit_name')}\n"
            has_circuit_begin = True
            calling_code = generate_qiskit_code(component, import_statements, functions, calling_code, defined_functions)
        elif component_name == "Quantum_Circuit_End":
            if not has_circuit_begin:
                calling_code += f"[Error] Circuit End mismatch\n"
                return calling_code
            calling_code += "# Quantum Circuit End\n"
            has_circuit_begin = False
        elif has_circuit_begin and component_name=="Circuit_Loop_Begin":
                iterations=component.get("parameters").get("iterations")
                calling_code += f"# Circuit Loop: Iterations {iterations}\n"
                in_circuit_loop=True
        elif has_circuit_begin and component_name=="Circuit_Loop_End":
                for i in range(iterations):
                    calling_code+=f"# Circuit Loop Iteration {i+1}\n"
                    for component__ in stack:
                        if circuit_loop_conditions and circuit_parameters:
                            calling_code = process_component_with_condition(component__, circuit_loop_conditions, circuit_parameters, circuit_repetition, i, calling_code)
                        else:
                            calling_code = generate_qiskit_code(component__, import_statements, functions, calling_code, defined_functions)
                in_circuit_loop=False
                calling_code += f"# Circuit Loop End\n"
        elif has_circuit_begin and in_circuit_loop and component_name!="qubit" and  component_name!="condition" and component_name!="define_parameter":
            stack.append(component)
        elif component_name == "RX_gate" or component_name == "RY_gate" or component_name == "RZ_gate":
            if (component['parameters']['mode'] == "parameters"):
                component['parameters']['theta'] = f"theta[{theta_count}]"
                theta_count += 1
            calling_code = generate_qiskit_code(component, import_statements, functions, calling_code, defined_functions)
        elif component_name == "condition":
            try:
                circuit_loop_conditions=json.loads(component['parameters']['condition'])
            except Exception as e:
                calling_code+=f"[Error] Failed to parse condition {e}\n"
        elif component_name == "define_parameter":
            try:
                circuit_parameters= json.loads(component['parameters']['parameters'])
                circuit_repetition = component['parameters']['number_of_reps']
                calling_code = generate_qiskit_code(component, import_statements, functions, calling_code, defined_functions)
            except Exception as e:
                calling_code+=f"[Error] Failed to parse parameter: {e}\n"
        elif component_name == "qubit":
            continue
        else:
            calling_code = generate_qiskit_code(component, import_statements, functions, calling_code, defined_functions)
    return calling_code

def generate_import_statements(import_statements):
    from collections import defaultdict
    module_imports = defaultdict(set)
    single_imports = set()
    aliased_imports = {}

    for item in import_statements:
        if isinstance(item, tuple):
            if len(item) == 2:
                module, alias = item
            else:
                module, alias = item[0], None
        else:
            module, alias = item, None

        parts = module.split('.')
        if len(parts) == 1:
            if alias:
                aliased_imports[module] = alias
            else:
                single_imports.add(module)
        else:
            base_module = '.'.join(parts[:-1])
            class_name = parts[-1]
            if alias:
                module_imports[base_module].add(f"{class_name} as {alias}")
            else:
                module_imports[base_module].add(class_name)
    result = []
    
    # Handle single imports
    for module in sorted(single_imports):
        result.append(f"import {module}")

    # Handle aliased imports
    for module, alias in sorted(aliased_imports.items()):
        result.append(f"import {module} as {alias}")

    # Handle module imports
    for module, items in sorted(module_imports.items()):
        if items:
            result.append(f"from {module} import {', '.join(sorted(items))}")

    return "\n".join(result)

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

def process_component_with_condition(component, conditions, parameters, reps, iteration_index, calling_code):
    component_name = component.get("name")

    # Check if the component is in the condition
    if component_name in conditions:
        try:
            # For a particular component, there can be many conditions, ie component have many parameters thus many conditions
            for param_condition in conditions[component_name]:
                parameter_name = param_condition["parameter"] 
                value_expression = param_condition["value"]  
                # Check for that paticular parameter in the parameters
                param_index = 0
                for param_name in parameters:
                    if param_name in value_expression:
                        if len(parameters[param_name]) > iteration_index:
                            value_expression = value_expression.replace(param_name, f"{param_index * int(reps) + iteration_index}")
                            param_index += 1
                        else:
                            raise ValueError(f"Index {iteration_index} out of range for parameter '{param_name}'")
                component['parameters'][parameter_name] = value_expression
                calling_code = generate_qiskit_code(component, import_statements, functions, calling_code, defined_functions)
                return calling_code

        except Exception as e:
            calling_code += f"[Error] Failed to apply condition for {component_name}: {e}\n"
    
    return calling_code

if __name__ == "__main__":
    input_json = sys.argv[1]
    data = json.loads(input_json)
    import_statements = set()
    functions = set()
    calling_code = ""
    defined_functions = set()

    calling_code = traverse_structure(data['structure'], import_statements, functions, calling_code, defined_functions)

    # Consolidate and print the imports
    import_code = generate_import_statements(import_statements)
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
        execution_result = execution_result.strip('"')
    except Exception as e:
        execution_result = str(e)

    result = {
        "code": full_code,
        "code_snapshot": code_snapshot,
        "result": execution_result,
    }

    # Cleanup the generated Python file
    # os.remove(file_path)

    print(json.dumps(result))
