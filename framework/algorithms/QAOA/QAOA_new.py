import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.primitives import Sampler
from qiskit.quantum_info import Pauli, SparsePauliOp
from qiskit.result import QuasiDistribution
from scipy.optimize import minimize

# Function to calculate the objective value (e.g., for Max-Cut)
def objective_value(x, w):
    X = np.outer(x, (1 - x))
    w_01 = np.where(w != 0, 1, 0)
    return np.sum(w_01 * X)

# Function to generate the problem Hamiltonian operator
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

# Function to extract the most likely state from a state vector
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

# Function to execute the quantum circuit using the sampler
def execute_circuit_with_sampler(qc, sampler):
    job = sampler.run(qc)
    result = job.result()
    return result

# Function to create the QAOA circuit with parameterized gates
def create_qaoa_circuit(params):
    qc = QuantumCircuit(4)  # Adjust based on your circuit's qubit requirements

    # First layer of gates
    for qubit in range(4):
        qc.h(qubit)
        qc.rx(params[qubit], qubit)

    # Add a second layer with entangling gates
    qc.cx(0, 1)
    qc.rz(params[4], 1)
    qc.cx(1, 2)
    qc.rz(params[5], 2)
    qc.cx(2, 3)
    qc.rz(params[6], 3)

    # Add a third layer of single-qubit rotations
    for qubit in range(4):
        qc.rx(params[qubit + 7], qubit)
    
    qc.measure_all()
    return qc

# Cost function to be minimized
def qaoa_cost_func(param_values):
    qc = create_qaoa_circuit(param_values)
    sampler = Sampler()
    result = sampler.run(qc).result()
    x = extract_most_likely_state(result.quasi_dists[0], 4)
    return -objective_value(x, weight_matrix)  # Negate if using a minimizer

# Main execution block
import traceback
try:
    # Define the problem's weight matrix (e.g., for Max-Cut)
    weight_matrix = np.array([[0.0, 1.0, 1.0, 0.0], [1.0, 0.0, 1.0, 1.0], [1.0, 1.0, 0.0, 1.0], [0.0, 1.0, 1.0, 0.0]])
    
    # Generate the operator (Hamiltonian) from the weight matrix
    qubit_op, offset = get_operator(weight_matrix)
    
    # Define a parameter vector with a size based on your circuit's requirements
    num_params = 11  # Adjust the size based on the number of parameters you need
    params = ParameterVector('θ', num_params)
    
    # Initialize parameters randomly
    initial_params = 2 * np.pi * np.random.random(num_params)
    
    # To get a better result, run the optimization multiple times and take the best
    best_result = float('inf')
    for _ in range(10):  # Try 10 different initializations
        initial_params = 2 * np.pi * np.random.random(num_params)
        res = minimize(qaoa_cost_func, initial_params, method="COBYLA")
        if res.fun < best_result:
            best_result = res.fun
    
    print("Best optimized result after multiple runs: ", best_result)
    
except Exception as e:
    print(f'An error occurred: {e}')
    print(traceback.format_exc())
