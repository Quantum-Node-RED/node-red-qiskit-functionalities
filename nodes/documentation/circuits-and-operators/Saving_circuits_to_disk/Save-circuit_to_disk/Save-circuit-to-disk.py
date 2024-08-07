from qiskit import QuantumCircuit
from qiskit import qpy
import json
import os
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0,1)
qc.measure_all()
with open('test.qpy', 'wb') as file:
    qpy.dump(qc, file)
absolute_path = os.path.abspath('test.qpy')
result={
    "result": "Circuit is saved to: " + absolute_path
}
print(json.dumps(result))