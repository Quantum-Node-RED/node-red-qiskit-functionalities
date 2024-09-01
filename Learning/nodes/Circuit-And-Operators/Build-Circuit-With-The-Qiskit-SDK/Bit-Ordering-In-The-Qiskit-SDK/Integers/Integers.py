from qiskit.primitives import Sampler
from qiskit import QuantumCircuit
import json
sampler = Sampler()  # Define the sampler
qc = QuantumCircuit(2)
qc.qubits[0]  # qubit "0"
qc.x(1)
qc.measure_all()
result_output = Sampler().run(qc).result().quasi_dists[0]

result={
    "result": result_output
}
print(json.dumps(result))
