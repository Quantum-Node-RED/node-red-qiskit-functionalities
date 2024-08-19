import json, io, base64
from qiskit import QuantumCircuit
qc = QuantumCircuit(2)
qc.qubits[0]  # qubit "0"
qc.x(1)
circuit_diagram_qc = qc.draw("mpl")
buffer = io.BytesIO()
circuit_diagram_qc.savefig(buffer, format="png")
buffer.seek(0)
circuit_diagram_base64 = base64.b64encode(buffer.read()).decode("utf-8")
buffer.close()
result = {
    "circuit_diagram": circuit_diagram_base64
}
print(json.dumps(result))