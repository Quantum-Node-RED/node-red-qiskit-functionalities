import base64
import json
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.primitives import Estimator
from matplotlib import pyplot as plt
import io

# Simple estimation experiment to create results
qc = QuantumCircuit(2)
qc.h(0)
qc.crx(1.5, 0, 1)
 
observables_labels = ["ZZ", "XX", "YZ", "ZY", "XY", "XZ", "ZX"]
observables = [SparsePauliOp(label) for label in observables_labels]
 
result = Estimator().run([qc]*7, observables).result()
 
# Plot using Matplotlib
plt.bar(observables_labels, result.values)
buffer = io.BytesIO()
plt.savefig(buffer, format='png') 
buffer.seek(0)
draw_str_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

result = {
    "plotted_estimator": draw_str_b64
}

print(json.dumps(result))
