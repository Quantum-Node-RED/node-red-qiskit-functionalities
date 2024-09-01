from qiskit import QuantumCircuit
import json
qc = QuantumCircuit(2)
qc.qubits[0]  # qubit "0"
result={
    "result": str(qc.qubits[0])
}
print(json.dumps(result))