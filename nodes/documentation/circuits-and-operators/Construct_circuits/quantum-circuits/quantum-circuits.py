from qiskit import QuantumCircuit
import json
qc = QuantumCircuit(2)
result={
    "result": str(qc.qubits)
}
print(json.dumps(result))