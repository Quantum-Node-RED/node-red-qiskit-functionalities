from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import EfficientSU2, PauliTwoDesign, RealAmplitudes
from qiskit_algorithms.time_evolvers.variational import ImaginaryMcLachlanPrinciple
from qiskit_algorithms import TimeEvolutionProblem
from qiskit_algorithms import VarQITE
from qiskit.primitives import Estimator
from qiskit.quantum_info import Statevector
from qiskit_algorithms import SciPyImaginaryEvolver
from qiskit import QuantumCircuit
import numpy as np
import pylab
import base64
import io
import warnings

import json
import sys


input = sys.argv[1]
parsed_input = json.loads(input)



hamiltonian_data = parsed_input['hamiltonian_data'].strip('[]').split(',')
hamiltonian_data = [item.strip('" ').strip() for item in hamiltonian_data]
hamiltonian_coeffs = [float(f) for f in parsed_input['hamiltonian_coeffs'].strip('[]').split(',')]
ansatz_name = parsed_input['ansatz']
evolution_time = float(parsed_input['evolution_time'])
reps = int(parsed_input['reps'])

# hamiltonian_data = ["ZZ", "IX", "XI"]
# hamiltonian_coeffs = [-0.2, -1, -1]


# Define the Hamiltonian operator
hamiltonian = SparsePauliOp(hamiltonian_data, coeffs=hamiltonian_coeffs)

# Define the ansatz
if ansatz_name == "EfficientSU2":
    ansatz = EfficientSU2(hamiltonian.num_qubits, reps = reps)
elif ansatz_name == "RealAmplitudes":
    ansatz = RealAmplitudes(hamiltonian.num_qubits, reps = reps)
elif ansatz_name == "PauliTwoDesign":
    ansatz = PauliTwoDesign(hamiltonian.num_qubits, reps = reps)


init_param_values = {}
for i in range(len(ansatz.parameters)):
    init_param_values[ansatz.parameters[i]] = np.pi / 2


var_principle = ImaginaryMcLachlanPrinciple()


time = evolution_time
aux_ops = [hamiltonian]
evolution_problem = TimeEvolutionProblem(hamiltonian, time, aux_operators=aux_ops)

var_qite = VarQITE(ansatz, init_param_values, var_principle, Estimator())
# an Estimator instance is necessary, if we want to calculate the expectation value of auxiliary operators.
evolution_result = var_qite.evolve(evolution_problem)

h_exp_val = [ele[0][0] for ele in evolution_result.observables]

# Return the result as a JSON string
times = evolution_result.times
pylab.plot(times, h_exp_val, label="VarQITE")
pylab.xlabel("Time")
pylab.ylabel(r"$\langle H \rangle$ (energy)")
pylab.legend(loc="upper right")
pylab.annotate('Ground state energy', xy=(times[-1], h_exp_val[-1]), xytext=(-90, 25), 
               textcoords='offset points', arrowprops=dict(arrowstyle='->'))



# Save the plot to a buffer
buffer = io.BytesIO()
pylab.savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()


# Draw the ansatz circuit
ansatz_buffer = io.BytesIO()
ansatz.decompose().draw('mpl').savefig(ansatz_buffer, format='png')
ansatz_buffer.seek(0)

ansatz_b64_str = base64.b64encode(ansatz_buffer.read()).decode('utf-8')
ansatz_buffer.close()


result = {
    "ansatz_image": ansatz_b64_str,
    "result_image": b64_str,
    "ground_state_energy": h_exp_val[-1]
}

# Return the result as a JSON string
print(json.dumps(result))


