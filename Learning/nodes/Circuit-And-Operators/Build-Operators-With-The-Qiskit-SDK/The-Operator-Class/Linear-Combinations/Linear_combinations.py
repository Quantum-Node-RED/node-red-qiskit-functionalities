import numpy as np
from qiskit.quantum_info import Operator, Pauli
import json


def linear_combinations():
    XX = Operator(Pauli("XX"))
    YY = Operator(Pauli("YY"))
    ZZ = Operator(Pauli("ZZ"))
    
    op = 0.5 * (XX + YY - 3 * ZZ)

    return op

if __name__ == "__main__":
    linear_combinations = linear_combinations()

    result = {
        "linear_combinations": linear_combinations.data.__str__(),
        "dim": linear_combinations.dim.__str__(),
        "input_dims": linear_combinations.input_dims().__str__(),
        "output_dims": linear_combinations.output_dims().__str__()
    }

    print(json.dumps(result))