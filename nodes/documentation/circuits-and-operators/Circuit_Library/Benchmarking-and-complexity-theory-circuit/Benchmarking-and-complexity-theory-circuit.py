import io
import base64
import json

from qiskit.circuit.library import QuantumVolume
circuit_diagram=QuantumVolume(4).decompose().draw('mpl')
buffer=io.BytesIO()
circuit_diagram.savefig(buffer, format='png')   
buffer.seek(0)
circuit_diagarm_base64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()
result = { 
    "circuit_diagram": circuit_diagarm_base64,
}
print(json.dumps(result))
