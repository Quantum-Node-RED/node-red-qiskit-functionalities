from qiskit import QuantumCircuit
import json, io, base64
qc = QuantumCircuit(2)
qc.x(0)
buffer=io.BytesIO()
qc.draw(reverse_bits=True, output="mpl").savefig(buffer, format="png")
buffer.seek(0)
circuit_diagram_base64=base64.b64encode(buffer.read()).decode("utf-8")
buffer.close()
buffer=io.BytesIO()
qc.reverse_bits().draw(output="mpl").savefig(buffer, format="png")
buffer.seek(0)
circuit_diagram_base64_reversed=base64.b64encode(buffer.read()).decode("utf-8")
buffer.close()

result={
    "circuit_diagram": circuit_diagram_base64,
    "circuit_diagram_reversed": circuit_diagram_base64_reversed
}
print(json.dumps(result))
