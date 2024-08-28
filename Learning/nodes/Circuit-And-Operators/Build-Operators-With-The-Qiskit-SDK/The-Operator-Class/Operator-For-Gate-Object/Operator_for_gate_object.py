from qiskit.circuit.library import CXGate
from qiskit.quantum_info import Operator
import json

def create_operator_for_gate_object():
    return Operator(CXGate())

def complex_encoder(obj):
    if isinstance(obj, complex):
        return [obj.real, obj.imag]
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

if __name__ == "__main__":

    operator = create_operator_for_gate_object()
    
    result = {  
        "operator": operator.data.__str__(),
        "dim": operator.dim.__str__(),
        "input_dims": operator.input_dims().__str__(),
        "output_dims": operator.output_dims().__str__()
    }

    print(json.dumps(result, default=complex_encoder))
