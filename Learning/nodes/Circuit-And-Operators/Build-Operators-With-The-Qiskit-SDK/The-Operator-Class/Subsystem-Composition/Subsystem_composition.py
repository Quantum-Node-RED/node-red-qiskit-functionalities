import numpy as np
from qiskit.quantum_info import Operator, Pauli
import json


def subsystem_composition():
    # Compose XZ with a 3-qubit identity operator
    op = Operator(np.eye(2**3))
    XZ = Operator(Pauli("XZ"))
    return op.compose(XZ, qargs=[0, 2])

if __name__ == "__main__":
    subsystem_composition = subsystem_composition()

    result = {
        "subsystem_composition": subsystem_composition.data.__str__(),
        "dim": subsystem_composition.dim.__str__(),
        "input_dims": subsystem_composition.input_dims().__str__(),
        "output_dims": subsystem_composition.output_dims().__str__()
    }

    print(json.dumps(result))  
    