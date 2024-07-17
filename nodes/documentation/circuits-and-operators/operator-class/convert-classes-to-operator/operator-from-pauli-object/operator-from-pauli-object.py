from qiskit.quantum_info import Operator, Pauli
import json
import sys

def create_operator_from_pauli_object(pauli = "XX"):
    # Create an Operator from a Pauli object
    _pauli = Pauli(pauli)
    operator = Operator(_pauli)
    return operator

def complex_encoder(obj):
    if isinstance(obj, complex):
        return [obj.real, obj.imag]
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

if __name__ == "__main__":

    input_arg = sys.argv[1]
    input_data = json.loads(input_arg)

    pauli = input_data["pauli"]

    operator = create_operator_from_pauli_object(pauli)
    
    result = {  
        "operator": operator.data.__str__(),
        "dim": operator.dim.__str__(),
        "input_dims": operator.input_dims().__str__(),
        "output_dims": operator.output_dims().__str__()
    }

    print(json.dumps(result, default=complex_encoder))
