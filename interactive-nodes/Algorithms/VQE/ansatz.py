import sys
import json
import base64
import io
from qiskit.circuit.library import TwoLocal

assert len(sys.argv) > 1, "No arguments found."
input = sys.argv[1]
parse_input = json.loads(input)

# parese input
num_qubits = parse_input["numQubits"]
rotation_blocks = parse_input["rotationLayers"]
entanglement_blocks = parse_input["entanglementLayers"]

ansatz = TwoLocal(num_qubits=num_qubits, rotation_blocks=rotation_blocks, entanglement_blocks=entanglement_blocks)

# Draw the circuit
ansatz_buffer = io.BytesIO()
ansatz.decompose().draw('mpl').savefig(ansatz_buffer, format='png')
ansatz_buffer.seek(0)
ansatz_str = base64.b64encode(ansatz_buffer.read()).decode('utf-8')
ansatz_buffer.close()


result = {
  "ansatz_image": ansatz_str,
}

print(json.dumps(result))
