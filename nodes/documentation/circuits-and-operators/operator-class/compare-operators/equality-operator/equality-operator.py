import numpy as np
from qiskit.quantum_info import Operator, Pauli
from qiskit.circuit.library import XGate
import json


def equality_operator():
    return Operator(Pauli("X")) == Operator(XGate())

def equality_operator_with_different_global_phase():
    return Operator(XGate()) == np.exp(1j * 0.5) * Operator(XGate())

if __name__ == "__main__":

    equality_operator = equality_operator()
    equality_operator_with_different_global_phase = equality_operator_with_different_global_phase()

    result = {
        "equality_operator": equality_operator,
        "equality_operator_with_different_global_phase": equality_operator_with_different_global_phase
    }

    print(json.dumps(result))
          