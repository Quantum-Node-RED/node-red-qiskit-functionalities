import io
import base64
import json
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import random_unitary
 
 
UU = random_unitary(4, seed=12345)
rand_U = UnitaryGate(UU)

qc = QuantumCircuit(2)
qc.append(rand_U, range(2))
qc.swap(0, 1)

# View the circuit
qc_buffer = io.BytesIO()
qc.draw("mpl", style="iqp").savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

result = {
  "qc_image": qc_str
}

print(json.dumps(result))
