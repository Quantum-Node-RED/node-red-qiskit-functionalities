import sys
import json
import pylab
import base64
import io

from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import TwoLocal
from qiskit.primitives import Estimator
from qiskit_algorithms import VQE
from qiskit_algorithms.optimizers import SLSQP, SPSA, COBYLA, L_BFGS_B

assert len(sys.argv) > 1, "No arguments found."
input = sys.argv[1]
parse_input = json.loads(input)

# parese input
num_qubits = parse_input["numQubits"]
rotation_blocks = parse_input["rotationLayers"]
entanglement_blocks = parse_input["entanglementLayers"]
# hamiltonian_data = parse_input["hamiltonianPauli"].strip('[]').split(',')
# hamiltonian_data = [item.strip('" ').strip() for item in hamiltonian_data]
pauli_list = parse_input["paulis"]
# hamiltonian_coeffs = [float(f) for f in parse_input["hamiltonianCoeffs"].strip('[]').split(',')]
chosen_optimizer = parse_input["optimizer"]
chosen_maxiter = int(parse_input["maxiter"])

# input error handling
# assert len(hamiltonian_data) == len(hamiltonian_coeffs), "The Pauli list of terms for the Hamiltonian should be as long as the complex coefficients."

hamiltonian_data = []
hamiltonian_coeffs = []
for pauli in pauli_list:
  hamiltonian_data.append(pauli["term"])
  hamiltonian_coeffs.append(pauli["coeff"])

operator = SparsePauliOp(hamiltonian_data, coeffs=hamiltonian_coeffs)

estimator = Estimator()

ansatz = TwoLocal(num_qubits=num_qubits, rotation_blocks=rotation_blocks, entanglement_blocks=entanglement_blocks)

optimizer = SLSQP(maxiter=chosen_maxiter)
if chosen_optimizer == "SPSA":
  optimizer = SPSA(maxiter=chosen_maxiter)
elif chosen_optimizer == "COBYLA":
  optimizer = COBYLA(maxiter=chosen_maxiter)
elif chosen_optimizer == "L_BFGS_B":
  optimizer = L_BFGS_B(maxiter=chosen_maxiter)


# storing intermediate energy value while optimizing
counts = []
values = []

def store_intermediate_result(eval_count, parameters, mean, std):
    counts.append(eval_count)
    values.append(mean)

vqe = VQE(estimator, ansatz, optimizer, callback=store_intermediate_result)

vqe_result = vqe.compute_minimum_eigenvalue(operator)

# Draw optimization convergence
pylab.rcParams["figure.figsize"] = (12, 8)
pylab.plot(counts, values, label=type(optimizer).__name__)
pylab.xlabel("Eval count")
pylab.ylabel("Energy")
pylab.title("Energy convergence")
pylab.legend(loc="upper right")

buffer = io.BytesIO()
pylab.savefig(buffer, format='png')
buffer.seek(0)
enegry_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

# Draw the optimal circuit
optimal_circuit_buffer = io.BytesIO()
vqe_result.optimal_circuit.decompose().draw('mpl').savefig(optimal_circuit_buffer, format='png')
optimal_circuit_buffer.seek(0)
optimal_circuit_str = base64.b64encode(optimal_circuit_buffer.read()).decode('utf-8')
optimal_circuit_buffer.close()


result = {
  "enegy_image": enegry_str, 
  "optimal_circuit_image": optimal_circuit_str,
  "optimal_value": vqe_result.optimal_value
}

print(json.dumps(result))
