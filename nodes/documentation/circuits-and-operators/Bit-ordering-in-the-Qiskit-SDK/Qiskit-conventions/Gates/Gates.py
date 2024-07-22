from qiskit import QuantumCircuit
import json, io, base64
qc = QuantumCircuit(2)
qc.cx(0, 1)
buffer=io.BytesIO()
qc.draw(output='mpl').savefig(buffer, format="png")
buffer.seek(0)
circuit_diagram_base64=base64.b64encode(buffer.read()).decode("utf-8")
buffer.close()
result={
    "circuit_diagram": circuit_diagram_base64
}
print(json.dumps(result))