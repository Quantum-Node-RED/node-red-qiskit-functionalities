from qiskit import QuantumCircuit
import io
import base64
import json
qc = QuantumCircuit(2)
qc.x(0)  # Add X-gate to qubit 0
# Draw definition circuit of 0th instruction in `qc`
circuit_diagram=qc.data[0].operation.definition.draw("mpl")
buffer=io.BytesIO()
circuit_diagram.savefig(buffer, format='png')
buffer.seek(0)
circuit_diagram=base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

results = {"circuit_diagram": circuit_diagram}
print(json.dumps(results))