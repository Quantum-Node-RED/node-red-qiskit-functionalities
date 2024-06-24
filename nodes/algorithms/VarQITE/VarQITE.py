from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import EfficientSU2
from qiskit_algorithms.time_evolvers.variational import ImaginaryMcLachlanPrinciple
from qiskit_algorithms import TimeEvolutionProblem
from qiskit_algorithms import VarQITE
from qiskit.primitives import Estimator
from qiskit.quantum_info import Statevector
from qiskit_algorithms import SciPyImaginaryEvolver
import numpy as np

import json
import sys

input = sys.argv[1]
parsed_input = json.loads(input)



hamiltonian_data = parsed_input['hamiltonian_data'].strip('[]').split(',')
hamiltonian_data = [item.strip('" ').strip() for item in hamiltonian_data]
hamiltonian_coeffs = [float(f) for f in parsed_input['hamiltonian_coeffs'].strip('[]').split(',')]
magnetization_data = parsed_input['magnetization_data'].strip('[]').split(',')
magnetization_data = [item.strip('" ').strip() for item in magnetization_data]
magnetization_coeffs = [float(f) for f in parsed_input['magnetization_coeffs'].strip('[]').split(',')]


# Define the Hamiltonian and the magnetization operator
hamiltonian = SparsePauliOp(["ZZ", "IX", "XI"], coeffs=[-0.2, -1, -1])
magnetization = SparsePauliOp(["IZ", "ZI"], coeffs=[1, 1])

ansatz = EfficientSU2(hamiltonian.num_qubits, reps=1)

init_param_values = {}
for i in range(len(ansatz.parameters)):
    init_param_values[ansatz.parameters[i]] = np.pi / 2


var_principle = ImaginaryMcLachlanPrinciple()


time = 5.0
aux_ops = [hamiltonian]
evolution_problem = TimeEvolutionProblem(hamiltonian, time, aux_operators=aux_ops)

var_qite = VarQITE(ansatz, init_param_values, var_principle, Estimator())
# an Estimator instance is necessary, if we want to calculate the expectation value of auxiliary operators.
evolution_result = var_qite.evolve(evolution_problem)

h_exp_val = [ele[0][0] for ele in evolution_result.observables]

result = {'result': h_exp_val}

print(json.dumps(result))
