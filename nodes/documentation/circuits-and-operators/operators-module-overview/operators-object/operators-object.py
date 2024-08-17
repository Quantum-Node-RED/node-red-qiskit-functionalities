import numpy as np
from qiskit.quantum_info.operators import Operator
import json
import sys

def demonstrate_operator_operations(matrix):
    return matrix, matrix.data, matrix.dim, matrix.input_dims(), matrix.output_dims()

def complex_encoder(obj):
    if isinstance(obj, complex):
        return [obj.real, obj.imag]
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

if __name__ == "__main__":
    input_json = sys.argv[1]
    input_data = json.loads(input_json)

    matrix = Operator(np.array(eval(input_data["matrix"])))

    matrix, data, dim, input_dims, output_dims = demonstrate_operator_operations(matrix)

    result = {
        "matrix": data.__str__(),  # Convert NumPy array to list
        "dim": dim.__str__(),  # Ensure dim is a standard int
        "input_dims": list(input_dims),  # Convert to list
        "output_dims": list(output_dims)  # Convert to list
    }

    # Output the result in JSON format
    print(json.dumps(result, default=complex_encoder))
