from qiskit.quantum_info import Statevector
import json
sv = Statevector.from_label("0+")
result={
    "result": str(sv.probabilities_dict())
}
print(json.dumps(result))