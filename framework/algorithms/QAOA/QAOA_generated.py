import sys
import json
import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.primitives import Sampler, Estimator
from qiskit.result import QuasiDistribution
from qiskit.quantum_info import Pauli, SparsePauliOp
from scipy.optimize import minimize
from qiskit_algorithms.utils import algorithm_globals
from functools import partial
from utils.image_helper import visualize_graph, save_circuit_image, encode_image_to_base64, combine_images
from utils.JSON_helper import NumpyEncoder


def objective_value(x, w):
    X = np.outer(x, (1 - x))
    w_01 = np.where(w != 0, 1, 0)
    return np.sum(w_01 * X)

def bitfield(n, L):
    result = np.binary_repr(n, L)
    return [int(digit) for digit in result]

def sample_most_likely(state_vector, num_qubits):
    if isinstance(state_vector, QuasiDistribution):
        values = list(state_vector.values())
    else:
        values = state_vector

    k = np.argmax(np.abs(values))
    x = bitfield(k, num_qubits)
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

# def define_optimizer(optimizer_type):
#     if optimizer_type == "SPSA":
#         optimizer = SPSA()
#     else:
#         optimizer = COBYLA()
#     return optimizer

def create_qaoa_circuit(num_qubits, param_vector, hamiltonian, reps):
    qc = QuantumCircuit(num_qubits)

    qc.h(range(num_qubits))  # Apply Hadamard gates to all qubits

    for i in range(reps):
        gamma = param_vector[i]
        beta = param_vector[reps + i]

        # Cost Hamiltonian (using gamma)
        for pauli_term, coeff in zip(hamiltonian.paulis, hamiltonian.coeffs):
            z_mask = pauli_term.z
            qubits = [idx for idx, z in enumerate(z_mask) if z]

            if len(qubits) == 1:
                qc.rz(2 * gamma * coeff, qubits[0])

            elif len(qubits) == 2:
                j, k = qubits
                qc.cx(j, k)
                qc.rz(2 * gamma * coeff, k)
                qc.cx(j, k)

            elif len(qubits) > 2:
                for j in range(len(qubits) - 1):
                    qc.cx(qubits[j], qubits[j + 1])
                qc.rz(2 * gamma * coeff, qubits[-1])
                for j in range(len(qubits) - 2, -1, -1):
                    qc.cx(qubits[j], qubits[j + 1])

        # Mixer Hamiltonian (using beta)
        qc.rx(2 * beta, range(num_qubits))

    return qc

def objective_function(params, estimator, qc, param_vector, hamiltonian):
    # Assign parameters to the existing circuit
    assigned_qc = qc.assign_parameters({param_vector: params})
    energy = estimator.run(circuits=[assigned_qc], observables=[hamiltonian]).result().values[0]
    min_value.append(np.real(energy))
    return np.real(energy)

def run_general_qaoa(hamiltonian, num_qubits, reps=2, seed=10598, optimizer_type="COBYLA", save_images=False, image_dir='images'):
    algorithm_globals.random_seed = seed
    np.random.seed(seed)
    # optimizer = define_optimizer(optimizer_type)

    os.makedirs(image_dir, exist_ok=True)
    initial_point = np.random.rand(2 * reps)

    param_vector = ParameterVector('θ', length=2 * reps)
    qc = create_qaoa_circuit(num_qubits, param_vector, hamiltonian, reps)  # Create the circuit once

    estimator = Estimator()

    # Using scipy.optimize.minimize
    result = minimize(
        objective_function,
        initial_point,
        args=(estimator, qc, param_vector, hamiltonian),  # Pass the created circuit and parameter vector
        method="COBYLA",
        # options={"maxiter": max_evals}  # Set the maximum number of iterations
    )

    print(f"Optimization Result: {result}")

    sampler = Sampler()

    # Assign final parameters and measure
    final_qc = qc.assign_parameters({param_vector: result.x})
    final_qc.measure_all()

    job = sampler.run(circuits=[final_qc])
    final_result = job.result()

    print(f"Final min value: {len(min_value)}")

    # Get the most likely bitstring from the final result
    x = sample_most_likely(final_result.quasi_dists[0], num_qubits)
    print(f"Solution bitstring: {x}")

    final_cut_value = objective_value(x, weight_matrix)
    print(f"Final objective (cut) value: {final_cut_value}")

    if save_images:
        save_circuit_image(final_qc, os.path.join(image_dir, "optimized_qaoa_circuit.png"))
        plt.close()

    return x, final_qc, final_cut_value

if __name__ == "__main__":

    json_file_path = "./test.json"
    with open(json_file_path, 'r') as j:
        input_data = json.loads(j.read())

    reps = int(input_data.get("reps", 2))
    seed = int(input_data.get("seed", 10598))
    optimizer_type = input_data.get("optimizer", "COBYLA")

    image_dir = "qaoa_images"

    global iteration_num
    iteration_num = 0

    global min_value
    min_value = []

    if "graph" in input_data and "adjacency_matrix" in input_data["graph"]:
        adjacency_matrices = np.array(eval(input_data["graph"]["adjacency_matrix"]))
        visualize_graph(adjacency_matrices, image_dir, "graph.png")
        graph = encode_image_to_base64(os.path.join(image_dir, "graph.png"))
        qubit_op, offset = get_operator(adjacency_matrices)
        global weight_matrix
        weight_matrix = adjacency_matrices
    elif "hamiltonian" in input_data:
        hamiltonian = input_data["hamiltonian"]["terms"]
        pauli_list = [(term["pauli"], term["coeff"]) for term in hamiltonian]
        qubit_op = SparsePauliOp.from_list(pauli_list)
    else:
        raise ValueError("Missing graph or hamiltonian in input data")

    save_images = input_data.get("save_images", False)

    x, _, output = run_general_qaoa(qubit_op, len(qubit_op.paulis[0]), reps, seed, optimizer_type, save_images, image_dir)
    if save_images:
        initial_circuit_image = encode_image_to_base64(os.path.join(image_dir, "initial_qaoa_circuit.png"))
        optimized_circuit_image = encode_image_to_base64(os.path.join(image_dir, "optimized_qaoa_circuit.png"))
        combined_step_image_filename = combine_images(step_images, os.path.join(image_dir, "combined_qaoa_steps.png"))
        combined_step_image = encode_image_to_base64(combined_step_image_filename)
    
    result = {
        "solution": x.tolist(),
        "objective_value": str(output),
    }

    print(json.dumps(result, cls=NumpyEncoder))
