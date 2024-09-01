import numpy as np
from qiskit.quantum_info.operators import SparsePauliOp
import json
import sys

def demonstrate_sparse_pauli_op_operations(op1, op2):
    # Perform addition
    addition_result = op1 + op2
    
    # Perform scalar multiplication
    scalar_multiplication_result = 2 * op1
    
    # Perform operator multiplication
    operator_multiplication_result = op1 @ op2
    
    # Perform tensor product
    tensor_product_result = op1.tensor(op2)

    return addition_result, scalar_multiplication_result, operator_multiplication_result, tensor_product_result

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

    # Create the second SparsePauliOp object
    op2 = SparsePauliOp.from_sparse_list(
        eval(input_data["op2"]["sparse_list"]), num_qubits=input_data["op2"]["num_qubits"]
    )

    addition_result, scalar_multiplication_result, operator_multiplication_result, tensor_product_result = demonstrate_sparse_pauli_op_operations(op1, op2)
    
    result = {
        "addition_result": addition_result.to_list(),
        "scalar_multiplication_result": scalar_multiplication_result.to_list(),
        "operator_multiplication_result": operator_multiplication_result.to_list(),
        "tensor_product_result": tensor_product_result.to_list()
    }

    # Output the result in JSON format
    print(json.dumps(result, default=complex_encoder))
