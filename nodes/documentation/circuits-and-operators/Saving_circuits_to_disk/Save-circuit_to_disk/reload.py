from qiskit import qpy
import json, io, base64
with open('test.qpy', 'rb') as handle:
    qc = qpy.load(handle)
buffer=io.BytesIO()
qc[0].draw('mpl').savefig(buffer, format="png")
buffer.seek(0)
circuit_diagram_base64=base64.b64encode(buffer.read()).decode("utf-8")
buffer.close()
result={
    "circuit_diagram": circuit_diagram_base64
}
print(json.dumps(result))

