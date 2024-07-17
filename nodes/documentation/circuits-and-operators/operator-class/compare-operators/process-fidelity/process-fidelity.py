import numpy as np
from qiskit.quantum_info import Operator
from qiskit.circuit.library import XGate
from qiskit.quantum_info import process_fidelity
import json


def demonstrate_process_fidelity():
    # Two operators which differ only by phase
    op_a = Operator(XGate())
    op_b = np.exp(1j * 0.5) * Operator(XGate())
 
    # Compute process fidelity
    F = process_fidelity(op_a, op_b)
    return F


if __name__ == "__main__":

    process_fidelity = demonstrate_process_fidelity()

    result = {
        "process_fidelity": process_fidelity,
    }

    print(json.dumps(result))
          