from qiskit import QuantumCircuit
import json
qc = QuantumCircuit(2)
qc.qubits
qc.x(0)  # Add X-gate to qubit 0
result={
    "result": str(qc.data)
}
print(json.dumps(result))