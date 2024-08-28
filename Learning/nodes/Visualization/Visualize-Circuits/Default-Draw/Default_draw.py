import base64
import json
from qiskit import QuantumCircuit

# Build a quantum circuit
circuit = QuantumCircuit(3, 3)
circuit.x(1)
circuit.h(range(3))
circuit.cx(0, 1)
circuit.measure(range(3), range(3));

# Draw the circuit
default_draw = circuit.draw()
default_draw_str = str(default_draw)

result = {
    "circuit_text": default_draw_str
}

print(json.dumps(result))
