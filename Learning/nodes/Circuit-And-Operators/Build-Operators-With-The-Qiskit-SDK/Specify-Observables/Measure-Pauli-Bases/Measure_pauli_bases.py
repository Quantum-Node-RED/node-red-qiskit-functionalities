import base64
import io
import json
from qiskit.circuit import QuantumCircuit
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

def demonstrate_measure_in_pauli_bases():
    # Create a circuit, where we would like to measure
    # q0 in the X basis, q1 in the Y basis and q2 in the Z basis
    circuit = QuantumCircuit(3)
    circuit.ry(0.8, 0)
    circuit.cx(0, 1)
    circuit.cx(1, 2)
    circuit.barrier()
    
    # Diagonalize X with the Hadamard gate 
    circuit.h(0)
    
    # Diagonalize Y with Hadamard as S^\dagger
    circuit.h(1)
    circuit.sdg(1)
    
    # The Z basis is the default, no action required here
    
    # Measure all qubits
    circuit.measure_all()
    
    return circuit

if __name__ == "__main__":
    circuit = demonstrate_measure_in_pauli_bases()
    image_filename = "circuit.png"
    circuit_image_base64 = save_circuit_image(circuit, image_filename)

    result = {
        "circuit_image": circuit_image_base64
    }

    print(json.dumps(result))
