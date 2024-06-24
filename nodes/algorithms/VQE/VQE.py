from qiskit_algorithms.optimizers import SLSQP
from qiskit_algorithms.optimizers import SPSA
from qiskit.circuit.library import TwoLocal
from qiskit.primitives import Estimator
from qiskit_algorithms import VQE
from qiskit.quantum_info import SparsePauliOp
# import matplotlib.pyplot as plt 
import sys
import json
import numpy as np

def convert_to_serializable(data):
    serializable_data = {}
    for key in data.__dict__:
        value = getattr(data, key)
        if isinstance(value, (np.ndarray, list)):
            serializable_data[key] = value.tolist() if isinstance(value, np.ndarray) else value
        elif isinstance(value, dict):
            serializable_data[key] = {str(k): v for k, v in value.items()}
        else:
            serializable_data[key] = str(value) if not isinstance(value, (int, float, type(None))) else value
    return serializable_data

input = sys.argv[1]
parse_input = json.loads(input)

num_qubits = parse_input["numQubits"]

rotation_blocks = "rx"           # TODO: convert to input or attributes
entanglement_blocks = "crx"      # TODO: convert to input or attributes
ansatz = TwoLocal(num_qubits, rotation_blocks, entanglement_blocks)
optimizer = SLSQP(maxiter=1000)  # TODO: convert to input or attributes
# optimizer = SPSA(maxiter=100) 

# ansatz.decompose().draw("mpl")
# plt.show()

estimator = Estimator()

vqe = VQE(estimator, ansatz, optimizer)

H2_op = SparsePauliOp.from_list(  # TODO: convert to input or attributes
    [
        ("II", -1.052373245772859),
        ("IZ", 0.39793742484318045),
        ("ZI", -0.39793742484318045),
        ("ZZ", -0.01128010425623538),
        ("XX", 0.18093119978423156),
    ]
)

result = vqe.compute_minimum_eigenvalue(H2_op)
serializable_result = convert_to_serializable(result)
print(json.dumps(serializable_result))
