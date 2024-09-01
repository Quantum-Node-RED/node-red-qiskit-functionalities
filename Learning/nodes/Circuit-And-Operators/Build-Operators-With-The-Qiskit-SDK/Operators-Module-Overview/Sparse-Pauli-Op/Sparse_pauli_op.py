import numpy as np
from qiskit.quantum_info.operators import SparsePauliOp
import json
import sys


def complex_encoder(obj):
    if isinstance(obj, complex):
        return [obj.real, obj.imag]
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

if __name__ == "__main__":
    input_json = sys.argv[1]
    input_data = json.loads(input_json)

    # Create the first SparsePauliOp object
    op1 = SparsePauliOp.from_sparse_list(
        eval(input_data["op1"]["sparse_list"]), num_qubits=input_data["op1"]["num_qubits"]
    )

    result = {
        "SparsePauliOp_list": op1.to_list()
    }

    # Output the result in JSON format
    print(json.dumps(result, default=complex_encoder))
