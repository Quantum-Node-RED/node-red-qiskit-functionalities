import numpy as np
from qiskit import QuantumCircuit
import json, io, base64

U = 0.5 * np.array([
    [1, 1, 1, 1],
    [-1, 1, -1, 1],
    [-1, -1, 1, 1],
    [-1, 1, 1, -1]
])
 
circuit = QuantumCircuit(2)
circuit.unitary(U, circuit.qubits)

circuit_diagram=circuit.draw("mpl")
buffer=io.BytesIO()
circuit_diagram.savefig(buffer, format="png")
buffer.seek(0)
circuit_diagram_base64=base64.b64encode(buffer.read()).decode("utf-8")
buffer.close()
result={
    "circuit_diagram": circuit_diagram_base64
}
print(json.dumps(result))