
from qiskit.circuit.library import HGate, MCXGate
import json
import io
import base64
from qiskit.circuit.library import TwoLocal
two_local = TwoLocal(3, 'rx', 'cz')
bound_circuit = two_local.assign_parameters({ p: 0 for p in two_local.parameters})
circuit_diagram=bound_circuit.decompose().draw('mpl')
buffer=io.BytesIO()
circuit_diagram.savefig(buffer, format='png')
buffer.seek(0)
circuit_diagarm_base64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()
result = { 
    "circuit_diagram": circuit_diagarm_base64,
}   

print(json.dumps(result))


