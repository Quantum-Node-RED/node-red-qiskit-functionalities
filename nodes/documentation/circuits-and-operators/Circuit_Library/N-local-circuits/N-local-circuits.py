
from qiskit.circuit.library import HGate, MCXGate
import json
import io
import base64
from qiskit.circuit.library import TwoLocal
two_local = TwoLocal(3, 'rx', 'cz')
circuit_diagram = two_local.decompose().draw('mpl')
buffer=io.BytesIO()
circuit_diagram.savefig(buffer, format='png')
buffer.seek(0)
circuit_diagarm_base64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()
two_local_params=two_local.parameters
result = { 
    "circuit_diagram": circuit_diagarm_base64,
    "two_local_params": str(two_local_params),
}   

print(json.dumps(result))


