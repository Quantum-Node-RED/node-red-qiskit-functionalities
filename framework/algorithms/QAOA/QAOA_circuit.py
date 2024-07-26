import sys
import json
import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler
from qiskit.result import QuasiDistribution
from qiskit.quantum_info import Pauli, SparsePauliOp
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit_algorithms.utils import algorithm_globals
from qiskit.circuit.library import PauliEvolutionGate
from utils.image_helper import visualize_graph, save_circuit_image, encode_image_to_base64, combine_images
from utils.JSON_helper import NumpyEncoder
# from qiskit.providers.aer import Aer
# from qiskit.utils import QuantumInstance  # Correct import for QuantumInstance

def objective_value(x, w):
    """Compute the value of a cut.
    Args:
        x: Binary string as numpy array.
        w: Adjacency matrix.
    Returns:
        Value of the cut.
    """
    X = np.outer(x, (1 - x))
    w_01 = np.where(w != 0, 1, 0)
    return np.sum(w_01 * X)

def bitfield(n, L):
    """Converts an integer into a bitfield."""
    result = np.binary_repr(n, L)
    return [int(digit) for digit in result]

def sample_most_likely(state_vector):
    """Compute the most likely binary string from state vector."""
    if isinstance(state_vector, QuasiDistribution):
        values = list(state_vector.values())
    else:
        values = state_vector
    n = int(np.log2(len(values)))
    k = np.argmax(np.abs(values))
    x = bitfield(k, n)
    x.reverse()
    return np.asarray(x)

def get_operator(weight_matrix):
    """Generate Hamiltonian for the graph partitioning
    Notes:
        Goals:
            1 Separate the vertices into two set of the same size.
            2 Make sure the number of edges between the two set is minimized.
        Hamiltonian:
            H = H_A + H_B
            H_A = sum\_{(i,j)\in E}{(1-ZiZj)/2}
            H_B = (sum_{i}{Zi})^2 = sum_{i}{Zi^2}+sum_{i!=j}{ZiZj}
            H_A is for achieving goal 2 and H_B is for achieving goal 1.
    Args:
        weight_matrix: Adjacency matrix.
    Returns:
        Operator for the Hamiltonian
        A constant shift for the obj function.
    """
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

# def construct_cost_hamiltonian(w):
#     """Construct the cost Hamiltonian for the graph partitioning problem."""
#     num_qubits = len(w)
#     paulis = []
#     coeffs = []

#     for i in range(num_qubits):
#         for j in range(i + 1, num_qubits):
#             if w[i, j] != 0:
#                 z_term = ['I'] * num_qubits
#                 z_term[i] = 'Z'
#                 z_term[j] = 'Z'
#                 paulis.append(''.join(z_term))
#                 coeffs.append(0.5 * w[i, j])

#     return SparsePauliOp(Pauli(paulis), coeffs)

def define_optimizer(optimizer_type):
    """Define the optimizer for the QAOA algorithm."""
    if optimizer_type == "SPSA":
        optimizer = SPSA()
    else:
        optimizer = COBYLA()
    return optimizer

def qaoa_circuit(num_qubits, params, hamiltonian, reps, save_images=False, image_dir='images'):
    """Construct the QAOA circuit."""
    gamma, beta = params[:reps], params[reps:]

    qc = QuantumCircuit(num_qubits)
    qc.h(range(num_qubits))

    mixer_hamiltonian = SparsePauliOp.from_list([('X' * num_qubits, -1)])

    step_images = []

    os.makedirs(image_dir, exist_ok=True)

    for i in range(reps):
        cost_op = PauliEvolutionGate(hamiltonian, time=gamma[i])
        qc.append(cost_op, range(num_qubits))
        if save_images:
            step_images.append(save_circuit_image(qc, os.path.join(image_dir, f"qaoa_circuit_step_cost_{i}.png")))

        mixer_op = PauliEvolutionGate(mixer_hamiltonian, time=beta[i])
        qc.append(mixer_op, range(num_qubits))
        if save_images:
            step_images.append(save_circuit_image(qc, os.path.join(image_dir, f"qaoa_circuit_step_mixer_{i}.png")))

    return qc, step_images

def run_general_qaoa(hamiltonian, num_qubits, reps=2, seed=10598, optimizer_type="COBYLA", save_images=False, image_dir='images'):
    """Run the QAOA algorithm for a general problem."""
    algorithm_globals.random_seed = seed
    optimizer = define_optimizer(optimizer_type)

    # Create the directory if it doesn't exist
    os.makedirs(image_dir, exist_ok=True)

    # Initialize parameter values
    initial_point = np.random.rand(2 * reps)
    
    # Create a QAOA ansatz circuit
    def ansatz(params):
        return qaoa_circuit(num_qubits, params, hamiltonian, reps, save_images, image_dir)
    
    # Save the initial QAOA circuit
    initial_qc, step_images = ansatz(initial_point)
    if save_images:
        save_circuit_image(initial_qc, os.path.join(image_dir, "initial_qaoa_circuit.png"))

    # Execute the QAOA circuit using the quantum instance
    sampler = Sampler()
    qaoa = QAOA(sampler, optimizer=optimizer, reps=reps, initial_point=initial_point)
    qaoa.ansatz = ansatz  # Assign the custom ansatz function to QAOA
    
    result = qaoa.compute_minimum_eigenvalue(hamiltonian)
    x = sample_most_likely(result.eigenstate)

    # Save the optimized QAOA circuit
    optimized_params = result.optimal_point
    optimized_qc, _ = ansatz(optimized_params)
    if save_images:
        save_circuit_image(optimized_qc, os.path.join(image_dir, "optimized_qaoa_circuit.png"))

    return x, optimized_qc, step_images

if __name__ == "__main__":
    input_json = sys.argv[1]
    input_data = json.loads(input_json)

    reps = int(input_data.get("reps", 2))
    seed = int(input_data.get("seed", 10598))
    optimizer_type = input_data.get("optimizer", "COBYLA")

    image_dir = "qaoa_images"

    graph = None

    if "graph" in input_data and "adjacency_matrix" in input_data["graph"]:
        adjacency_matrices = np.array(eval(input_data["graph"]["adjacency_matrix"]))
        visualize_graph(adjacency_matrices, image_dir, "graph.png")
        graph = encode_image_to_base64(os.path.join(image_dir, "graph.png"))
        qubit_op, _ = get_operator(adjacency_matrices)
    elif "hamiltonian" in input_data:
        hamiltonian = input_data["hamiltonian"]["terms"]
        pauli_list = [(term["pauli"], term["coeff"]) for term in hamiltonian]
        qubit_op = SparsePauliOp.from_list(pauli_list)
    else:
        raise ValueError("Missing graph or hamiltonian in input data")

    save_images = input_data.get("save_images", True)

    x, ansatz, step_images = run_general_qaoa(qubit_op, len(qubit_op.paulis[0]), reps, seed, optimizer_type, save_images, image_dir)
    initial_circuit_image = encode_image_to_base64(os.path.join(image_dir, "initial_qaoa_circuit.png"))
    optimized_circuit_image = encode_image_to_base64(os.path.join(image_dir, "optimized_qaoa_circuit.png"))
    combined_step_image_filename = combine_images(step_images, os.path.join(image_dir, "combined_qaoa_steps.png"))
    combined_step_image = encode_image_to_base64(combined_step_image_filename)
    
    result = {
        "problem": "general",
        "solution": x.tolist(),
        "initial_circuit_image": initial_circuit_image,
        "optimized_circuit_image": optimized_circuit_image,
        "combined_step_image": combined_step_image,
        "graph": graph
    }

    # Output the result in JSON format
    print(json.dumps(result, cls=NumpyEncoder))
