<<<<<<< HEAD
import io
import json
from qiskit import QuantumCircuit
import base64
import matplotlib.pyplot as plt
import base64
import io



# Quantum Circuit Begin test
test = QuantumCircuit(2)
test.cx(1, 0)
test.h(0)
test.cz(0, 1)
test.rx(0.5, 1)
# Quantum Circuit End
buffer = io.BytesIO()
test.draw(output='mpl').savefig(buffer, format='png')
buffer.seek(0)
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()
print(json.dumps(b64_str))
=======
from qiskit.primitives import Sampler
from qiskit.quantum_info import Pauli
from qiskit.result import QuasiDistribution
from qiskit import QuantumCircuit
import numpy as np
from qiskit.quantum_info import SparsePauliOp

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

def execute_circuit_with_sampler(qc, sampler):
        job = sampler.run(qc)
        result = job.result()
        return result

def objective_value(x, w):
    X = np.outer(x, (1 - x))
    w_01 = np.where(w != 0, 1, 0)
    return np.sum(w_01 * X)

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

import traceback
try:
    weight_matrix = np.array(eval("[[0.0, 1.0, 1.0, 0.0], [1.0, 0.0, 1.0, 1.0], [1.0, 1.0, 0.0, 1.0], [0.0, 1.0, 1.0, 0.0]]"))
    qubit_op, offset = get_operator(weight_matrix)
    sampler = Sampler()
    # Quantum Circuit Begin qc
    qc = QuantumCircuit(4, 4)
    qc.h(0)
    qc.rx(0.647, 0)
    qc.h(1)
    qc.cx(0, 1)
    qc.rz(-1.12, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.rz(2.25, 1)
    qc.cx(0, 1)
    qc.cx(0, 1)
    qc.rz(2.25, 1)
    qc.cx(0, 1)
    qc.rx(0.647, 1)
    qc.h(2)
    qc.cx(0, 2)
    qc.rz(-1.12, 2)
    qc.cx(0, 2)
    qc.cx(1, 2)
    qc.rz(-1.12, 2)
    qc.cx(1, 2)
    qc.cx(0, 2)
    qc.rz(2.25, 2)
    qc.cx(0, 2)
    qc.cx(1, 2)
    qc.rz(2.25, 2)
    qc.cx(1, 2)
    qc.cx(0, 2)
    qc.rz(2.25, 2)
    qc.cx(0, 2)
    qc.cx(1, 2)
    qc.rz(2.25, 2)
    qc.cx(1, 2)
    qc.rx(0.647, 2)
    qc.h(3)
    qc.cx(1, 3)
    qc.rz(-1.12, 3)
    qc.cx(1, 3)
    qc.cx(2, 3)
    qc.rz(-1.12, 3)
    qc.cx(2, 3)
    qc.cx(0, 3)
    qc.rz(2.25, 3)
    qc.cx(0, 3)
    qc.cx(1, 3)
    qc.rz(2.25, 3)
    qc.cx(1, 3)
    qc.cx(2, 3)
    qc.rz(2.25, 3)
    qc.cx(2, 3)
    qc.cx(0, 3)
    qc.rz(2.25, 3)
    qc.cx(0, 3)
    qc.cx(1, 3)
    qc.rz(2.25, 3)
    qc.cx(1, 3)
    qc.cx(2, 3)
    qc.rz(2.25, 3)
    qc.cx(2, 3)
    qc.rx(0.647, 3)
    # Quantum Circuit End
    qc.measure(range(4), range(4))
    optimised_result = execute_circuit_with_sampler(qc, sampler)
    x = extract_most_likely_state(optimised_result.quasi_dists[0], 4)
    objective_value = objective_value(x, weight_matrix)
    print("result: ", objective_value)
    
except Exception as e:
    print(f'An error occurred: {e}')
    print(traceback.format_exc())
