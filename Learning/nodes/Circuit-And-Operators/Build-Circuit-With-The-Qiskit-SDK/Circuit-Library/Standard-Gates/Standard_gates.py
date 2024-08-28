from qiskit import QuantumCircuit
from qiskit.circuit.library import HGate, MCXGate

import json
import io
import base64

mcx_gate = MCXGate(3)
hadamard_gate = HGate()
qc = QuantumCircuit(4)
qc.append(hadamard_gate, [0])
qc.append(mcx_gate, [0,1,2,3])

circuit_diagram = qc.draw(output='mpl')
buffer=io.BytesIO()
circuit_diagram.savefig(buffer, format='png')
buffer.seek(0)
circuit_diagarm_base64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

result = { 
    "circuit_diagram": circuit_diagarm_base64
}   

print(json.dumps(result))


