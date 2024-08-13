import sys
import json
from code_component import  snippets
from import_table import import_table
from params_schemas import schemas

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
    for  component in structure:
        component_name = component.get("name")
        if component_name == "root":
            if component.get("code"):
                calling_code += component.get("code")
        elif component_name == "Quantum_Circuit_Begin":
            calling_code += f"# Quantum Circuit Begin {component.get('parameters').get('circuit_name')}\n"
            has_circuit_begin = True
            calling_code = generate_qiskit_code(component, import_statements, functions, calling_code, defined_functions)
        elif component_name == "Quantum_Circuit_End":
            if not has_circuit_begin:
                calling_code += f"[Error] Circuit End mismatch\n"
                return calling_code
            calling_code += "# Quantum Circuit End\n"
            has_circuit_begin = False
        elif component_name == "qbit":
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
    full_code = f"{import_code}\n{function_code}\n{calling_code}"
    result = {
        "code": full_code,
    }
    print(json.dumps(result))

