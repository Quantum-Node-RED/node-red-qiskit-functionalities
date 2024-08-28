import numpy as np
from qiskit.quantum_info.operators import Operator
import json
import sys


def complex_encoder(obj):
    if isinstance(obj, complex):
        return [obj.real, obj.imag]
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

if __name__ == "__main__":
    input_json = sys.argv[1]
    input_data = json.loads(input_json)

    matrix = Operator(np.array(eval(input_data["matrix"])))

    

    result = {
        "matrix": str(matrix)
    }

    # Output the result in JSON format
    print(json.dumps(result, default=complex_encoder))
