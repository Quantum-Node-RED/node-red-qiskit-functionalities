from qiskit.quantum_info import Operator, Pauli
import json
import sys


def tensor_expansion(pauli_1 = "X", pauli_2 = "Z" ):
    A = Operator(Pauli(pauli_1))
    B = Operator(Pauli(pauli_2))
    return A.expand(B)

if __name__ == "__main__":

    input_arg = sys.argv[1]
    input_data = json.loads(input_arg)

    pauli_1 = input_data["pauli_1"] 
    pauli_2 = input_data["pauli_2"] 
    
    tensor_expansion = tensor_expansion(pauli_1, pauli_2)

    result = {
        "tensor_expansion": tensor_expansion.data.__str__(),
        "dim": tensor_expansion.dim.__str__(),
        "input_dims": tensor_expansion.input_dims().__str__(),
        "output_dims": tensor_expansion.output_dims().__str__()
    }

    print(json.dumps(result))   
      