import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.primitives import Estimator, Sampler
from qiskit.quantum_info import Pauli, SparsePauliOp
from qiskit.result import QuasiDistribution
from scipy.optimize import minimize

def extract_most_likely_state(state_vector, num_qubits):
    if isinstance(state_vector, QuasiDistribution):
        values = list(state_vector.values())
    else:
        values = state_vector
    k = np.argmax(np.abs(values))
    result = np.binary_repr(k, num_qubits)
    x = [int(digit) for digit in result]
    x.reverse()
    return np.asarray(x)

def get_operator(weight_matrix):
    num_nodes = len(weight_matrix)
    pauli_list = []
    coeffs = []
    shift = 0

    for i in range(num_nodes):
        for j in range(i):
            if weight_matrix[i, j] != 0:
                x_p = np.zeros(num_nodes, dtype=bool)
                z_p = np.zeros(num_nodes, dtype=bool)
                z_p[i] = True
                z_p[j] = True
                pauli_list.append(Pauli((z_p, x_p)))
                coeffs.append(-0.5)
                shift += 0.5

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                x_p = np.zeros(num_nodes, dtype=bool)
                z_p = np.zeros(num_nodes, dtype=bool)
                z_p[i] = True
                z_p[j] = True
                pauli_list.append(Pauli((z_p, x_p)))
                coeffs.append(1.0)
            else:
                shift += 1

    return SparsePauliOp(pauli_list, coeffs=coeffs), shift

def objective_function(params, qc, param_vector, hamiltonian, estimator):
    assigned_qc = qc.assign_parameters({param_vector: params})
    energy = estimator.run(circuits=[assigned_qc], observables=[hamiltonian]).result().values[0]
    return np.real(energy)

def execute_circuit_with_sampler(qc, sampler):
        job = sampler.run(qc)
        result = job.result()
        return result

def objective_value(x, w):
    X = np.outer(x, (1 - x))
    w_01 = np.where(w != 0, 1, 0)
    return np.sum(w_01 * X)

import traceback
try:
    weight_matrix = np.array(eval("[[0.0, 1.0, 1.0, 0.0], [1.0, 0.0, 1.0, 1.0], [1.0, 1.0, 0.0, 1.0], [0.0, 1.0, 1.0, 0.0]]"))
    operator, offset = get_operator(weight_matrix)
    sampler = Sampler()
    initial_params = [0.1, 0.2, 0.3, 0.4]
    param_vector = ParameterVector('θ', length=2 * 2)
    # Quantum Circuit Begin qc
    qc = QuantumCircuit(4, 4)
    # Circuit Loop: Iterations 2
    # Circuit Loop Iteration 1
    [Error] Failed to apply condition for RX_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RX_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RX_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RX_gate: 0
    # Circuit Loop Iteration 2
    [Error] Failed to apply condition for RX_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RX_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RX_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RZ_gate: 0
    [Error] Failed to apply condition for RX_gate: 0
    # Circuit Loop End
    # Quantum Circuit End
    estimator = Estimator()
    
    result= minimize(objective_function, initial_params, args=(qc, param_vector, operator, estimator), method="COBYLA")
    qc.measure(range(4), range(4))
    optimised_result = execute_circuit_with_sampler(qc, sampler)
    x = extract_most_likely_state(optimised_result.quasi_dists[0], 4)
    objective_value = objective_value(x, weight_matrix)
    print("result: ", objective_value)
    
except Exception as e:
    print(f'An error occurred: {e}')
    print(traceback.format_exc())
