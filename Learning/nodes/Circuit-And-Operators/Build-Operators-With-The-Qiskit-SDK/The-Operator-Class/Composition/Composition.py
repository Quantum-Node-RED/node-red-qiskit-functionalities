from qiskit.quantum_info import Operator, Pauli
import json
import sys


def composition(pauli_1 = "X", pauli_2 = "Z" ):
    A = Operator(Pauli(pauli_1))
    B = Operator(Pauli(pauli_2))
    return A.compose(B, front=True)

if __name__ == "__main__":

    input_arg = sys.argv[1]
    input_data = json.loads(input_arg)

    pauli_1 = input_data["pauli_1"] 
    pauli_2 = input_data["pauli_2"] 
    
    composition = composition(pauli_1, pauli_2)

    result = {
        "composition": composition.data.__str__(),
        "dim": composition.dim.__str__(),
        "input_dims": composition.input_dims().__str__(),
        "output_dims": composition.output_dims().__str__()
    }

    print(json.dumps(result))     