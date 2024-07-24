import base64
import json
from math import pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.quantum_info import DensityMatrix
import io

# Create a Bell state for demonstration
qc = QuantumCircuit(2)
qc.h(0)
qc.crx(pi/2, 0, 1)
psi = Statevector(qc)

# convert to a DensityMatrix and draw
fold_draw = DensityMatrix(psi).draw(output="latex_source")

fold_draw_str = str(fold_draw)

result = {
    "circuit_text": fold_draw_str
}

print(json.dumps(result))
