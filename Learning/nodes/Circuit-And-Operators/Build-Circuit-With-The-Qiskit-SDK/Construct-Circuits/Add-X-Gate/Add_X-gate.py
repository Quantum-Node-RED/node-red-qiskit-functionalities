from qiskit import QuantumCircuit
import json
import io
import base64
qc = QuantumCircuit(2)
qc.qubits
qc.x(0)  # Add X-gate to qubit 0
circuit_diagram=qc.draw("mpl")
buffer=io.BytesIO()
circuit_diagram.savefig(buffer, format="png")
buffer.seek(0)
circuit_diagram_base64=base64.b64encode(buffer.read()).decode("utf-8")
buffer.close()

result={
    "result": str(qc.data),
    "circuit_diagram": circuit_diagram_base64
}
print(json.dumps(result))