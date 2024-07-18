from qiskit.circuit.library import HGate
from qiskit import QuantumCircuit
import json
import base64
import io
qc = QuantumCircuit(1)
qc.append(
    HGate(),  # New HGate instruction
    [0]       # Apply to qubit 0
)
circuit_digram=qc.draw("mpl")
buffer=io.BytesIO()
circuit_digram.savefig(buffer, format="png")
buffer.seek(0)
circuit_digram_base64=base64.b64encode(buffer.read()).decode("utf-8")
buffer.close()
result={
    "circuit_diagram": circuit_digram_base64
}

print(json.dumps(result))