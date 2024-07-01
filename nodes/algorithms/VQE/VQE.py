import sys
import json
import numpy as np

from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import TwoLocal
from qiskit.primitives import Estimator
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP, SPSA
# import matplotlib.pyplot as plt 

# def convert_to_serializable(data):
#     serializable_data = {}
#     for key in data.__dict__:
#         value = getattr(data, key)
#         if isinstance(value, (np.ndarray, list)):
#             serializable_data[key] = value.tolist() if isinstance(value, np.ndarray) else value
#         elif isinstance(value, dict):
#             serializable_data[key] = {str(k): v for k, v in value.items()}
#         else:
#             serializable_data[key] = str(value) if not isinstance(value, (int, float, type(None))) else value
#     return serializable_data

input = sys.argv[1]
parse_input = json.loads(input)

num_qubits = parse_input["numQubits"]
rotation_blocks = parse_input["rotationLayers"]
entanglement_blocks = parse_input["entanglementLayers"]
hamiltonian_data = parse_input["hamiltonianPauli"]

hamiltonian_data = parse_input['hamiltonianPauli'].strip('[]').split(',')
hamiltonian_data = [item.strip('" ').strip() for item in hamiltonian_data]
hamiltonian_coeffs = [float(f) for f in parse_input['hamiltonianCoeffs'].strip('[]').split(',')]
print(hamiltonian_coeffs)

H2_op = SparsePauliOp(hamiltonian_data, coeffs=hamiltonian_coeffs)

estimator = Estimator()

ansatz = TwoLocal(num_qubits, rotation_blocks, entanglement_blocks)

optimizer = SLSQP(maxiter=1000)  # TODO: convert to input or attributes
# optimizer = SPSA(maxiter=100) 

# ansatz.decompose().draw("mpl")
# plt.show()

vqe = VQE(estimator, ansatz, optimizer)


result = vqe.compute_minimum_eigenvalue(H2_op)
# serializable_result = convert_to_serializable(result)

print(json.dumps({"optimal_value": result.optimal_value}))
