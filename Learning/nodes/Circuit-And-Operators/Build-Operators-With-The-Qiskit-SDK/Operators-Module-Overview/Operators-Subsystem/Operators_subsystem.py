import numpy as np
from qiskit.quantum_info.operators import Operator
import json
import sys

def complex_encoder(obj):
    if isinstance(obj, complex):
        return [obj.real, obj.imag]
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

if __name__ == "__main__":
    op = Operator(np.random.rand(2**1, 2**2))

    result = {
        "input_dims": op.input_dims().__str__(),
        "output_dims": op.output_dims().__str__()
    }

    # Output the result in JSON format
    print(json.dumps(result, default=complex_encoder))
