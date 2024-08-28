import json
from qiskit.quantum_info.operators import Pauli
import json
import sys

def demonstrate_pauli_operations(operator):
    return operator.dim, operator.phase, operator.to_matrix()

def complex_encoder(obj):
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

# Create main function  
if __name__ == "__main__":
    input_json = sys.argv[1]
    input_data = json.loads(input_json)

    operator = input_data["operator"]

    dimension, phase, matrix = demonstrate_pauli_operations(Pauli(operator))    
    
    result = {
        "dimension": dimension.__str__(),
        "phase": int(phase),
        "matrix": matrix.__str__()
    }

    # Output the result in JSON format
    print(json.dumps(result, default=complex_encoder))
    