import json
from qiskit.quantum_info import Statevector
sv = Statevector.from_label("0+")
result={
    "result": [str(sv[1]), str(sv[2])]
}
print(json.dumps(result))