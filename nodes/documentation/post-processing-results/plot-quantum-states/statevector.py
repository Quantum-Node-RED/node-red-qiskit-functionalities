import base64
import json
from math import pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import io

# Create a Bell state for demonstration
qc = QuantumCircuit(2)
qc.h(0)
qc.crx(pi/2, 0, 1)
psi = Statevector(qc)

# psi is a Statevector object
fold_draw = psi.draw(output="latex_source")

fold_draw_str = str(fold_draw)

result = {
    "circuit_text": fold_draw_str
}

print(json.dumps(result))
