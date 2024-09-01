import base64
import json
from math import pi
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_city
import io

# Create a Bell state for demonstration
qc = QuantumCircuit(2)
qc.h(0)
qc.crx(pi/2, 0, 1)
psi = Statevector(qc)

draw_str = plot_state_city(psi)
buffer = io.BytesIO()
draw_str.savefig(buffer, format='png') 
buffer.seek(0)
draw_str_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

result = {
    "circuit_diagram": draw_str_b64
}

print(json.dumps(result))
