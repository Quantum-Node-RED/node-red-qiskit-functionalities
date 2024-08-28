import numpy as np
from qiskit.circuit.library import RXGate
from qiskit.quantum_info import Operator
import json

def create_operator_for_parametrized_gate_object():
    return Operator(RXGate(np.pi / 2))

if __name__ == "__main__":

    operator = create_operator_for_parametrized_gate_object()
    
    result = {  
        "operator": operator.data.__str__(),
        "dim": operator.dim.__str__(),
        "input_dims": operator.input_dims().__str__(),
        "output_dims": operator.output_dims().__str__()
    }

    print(json.dumps(result))
