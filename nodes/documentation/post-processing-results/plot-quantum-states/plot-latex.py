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

# psi is a Statevector object
statevector_draw = psi.draw(output="latex_source")
density_matrix_draw = psi.draw(output="latex_source")

statevector_draw_str = str(statevector_draw)
density_matrix_str = str(density_matrix_draw)

result = {
    "statevector": statevector_draw,
    "density_matrix": density_matrix_str
}

print(json.dumps(result))
