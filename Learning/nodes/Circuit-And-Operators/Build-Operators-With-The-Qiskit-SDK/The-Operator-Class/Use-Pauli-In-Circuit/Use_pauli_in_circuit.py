import base64
import io
import json
import sys
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info import Operator, Pauli
from qiskit.visualization import circuit_drawer

def save_circuit_image(circuit, filename):
    """Save the circuit image to a file and return the base64 string."""
    buffer = io.BytesIO()
    circuit_drawer(circuit, output='mpl').savefig(buffer, format='png')
    buffer.seek(0)
    with open(filename, 'wb') as f:
        f.write(buffer.read())
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    return img_base64

def use_unitary_operator_in_circuit(pauli="XX"):
    
    circ = QuantumCircuit(2, 2)
    circ.append(Pauli(pauli), [0, 1])
    circ.measure([0, 1], [0, 1])
    
    # Save and return circuit image as base64
    image_filename = "circuit.png"
    circuit_image_base64 = save_circuit_image(circ, image_filename)
    
    return circuit_image_base64

if __name__ == "__main__":
    input_arg = sys.argv[1]
    input_data = json.loads(input_arg)

    pauli = input_data["pauli"]

    circuit_image_base64 = use_unitary_operator_in_circuit(pauli)
    
    result = {
        "circuit_image": circuit_image_base64
    }

    print(json.dumps(result))
