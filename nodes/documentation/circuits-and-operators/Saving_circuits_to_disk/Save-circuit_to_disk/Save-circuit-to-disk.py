from qiskit import QuantumCircuit
from qiskit import qpy
import json
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0,1)
qc.measure_all()
with open('test.qpy', 'wb') as file:
    qpy.dump(qc, file)
result={
    "result": "Circuit saved to disk"
}
print(json.dumps(result))