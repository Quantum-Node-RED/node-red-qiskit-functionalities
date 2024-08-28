import base64
import json
from qiskit import QuantumCircuit

circuit = QuantumCircuit(1)
for _ in range(10):
    circuit.h(0)
# limit line length to 40 characters
fold_draw = circuit.draw(output="text", fold=40)

fold_draw_str = str(fold_draw)

result = {
    "circuit_text": fold_draw_str
}

print(json.dumps(result))
