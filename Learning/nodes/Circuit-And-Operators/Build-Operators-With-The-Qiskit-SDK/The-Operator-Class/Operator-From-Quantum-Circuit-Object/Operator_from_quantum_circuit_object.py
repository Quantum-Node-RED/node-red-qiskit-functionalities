from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info import Operator
import json

def create_operator_from_quantum_circuit_object():
    # Create an operator from a QuantumCircuit object
    circ = QuantumCircuit(10)
    circ.h(0)
    for j in range(1, 10):
        circ.cx(j - 1, j)
    
    # Convert circuit to an operator by implicit unitary simulation
    return Operator(circ)

if __name__ == "__main__":
    operator = create_operator_from_quantum_circuit_object()   

    result = {  
        "operator": operator.data.__str__(),
        "dim": operator.dim.__str__(),
        "input_dims": operator.input_dims().__str__(),
        "output_dims": operator.output_dims().__str__()
    }   

    print(json.dumps(result))  
