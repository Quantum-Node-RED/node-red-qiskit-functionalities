import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sys
import json
import base64
import io
from qiskit.quantum_info import Pauli, SparsePauliOp
from qiskit.primitives import Sampler
from qiskit.result import QuasiDistribution
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit_algorithms.utils import algorithm_globals
import warnings

# Helper functions
def objective_value(x, w):
    """Compute the value of a cut for Max-Cut problem."""
    X = np.outer(x, (1 - x))
    w_01 = np.where(w != 0, 1, 0)
    return np.sum(w_01 * X)

def bitfield(n, L):
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

def get_maxcut_operator(weight_matrix):
    """Generate Hamiltonian for Max-Cut problem."""
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

def get_tsp_operator(dist_matrix):
    num_cities = len(dist_matrix)
    pauli_list = []
    coeffs = []

    # Cost Hamiltonian: Minimize the total distance traveled
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                z_p = np.zeros(num_cities ** 2, dtype=bool)
                z_p[i * num_cities + j] = True
                pauli_list.append(Pauli((z_p, np.zeros(num_cities ** 2, dtype=bool))))
                coeffs.append(dist_matrix[i][j])

    # Constraint Hamiltonian: Each city needs to be visited exactly once
    for k in range(num_cities):
        for i in range(num_cities):
            z_p = np.zeros(num_cities ** 2, dtype=bool)
            z_p[i * num_cities + k] = True  # Visit from city i to k
            z_p[k * num_cities + i] = True  # Visit from city k to i
            pauli_list.append(Pauli((z_p, np.zeros(num_cities ** 2, dtype=bool))))
            coeffs.append(2)  # Penalty coefficient
        identity = np.zeros(num_cities ** 2, dtype=bool)
        pauli_list.append(Pauli((identity, np.zeros(num_cities ** 2, dtype=bool))))  # Identity for balancing the quadratic terms
        coeffs.append(-2 * num_cities)

    return SparsePauliOp(pauli_list, coeffs=coeffs)

def run_general_qaoa(hamiltonian, reps=2, seed=10598):
    algorithm_globals.random_seed = seed
    optimizer = COBYLA()
    sampler = Sampler()
    qaoa = QAOA(sampler, optimizer, reps=reps)
    result = qaoa.compute_minimum_eigenvalue(hamiltonian)
    x = sample_most_likely(result.eigenstate)
    return x, qaoa.ansatz

# QAOA execution function for Max-Cut
def run_qaoa_maxcut(weight_matrix, reps=2, seed=10598):
    qubit_op, offset = get_maxcut_operator(weight_matrix)
    algorithm_globals.random_seed = seed
    optimizer = COBYLA()
    sampler = Sampler()
    qaoa = QAOA(sampler, optimizer, reps=reps)
    result = qaoa.compute_minimum_eigenvalue(qubit_op)
    x = sample_most_likely(result.eigenstate)
    return x, objective_value(x, weight_matrix), qaoa.ansatz

# QAOA execution function for TSP
def run_qaoa_tsp(dist_matrix, reps=1, seed=10598):
    qubit_op = get_tsp_operator(dist_matrix)
    algorithm_globals.random_seed = seed
    optimizer = SPSA(maxiter=100)  # Change optimizer to SPSA with max iterations
    sampler = Sampler()
    qaoa = QAOA(sampler, optimizer, reps=reps, initial_point=[0.1] * 2 * reps)
    result = qaoa.compute_minimum_eigenvalue(qubit_op)
    x = sample_most_likely(result.eigenstate)
    return x, qaoa.ansatz

def visualise_graph(matrix):
        
    # Suppress specific warnings
    warnings.filterwarnings('ignore', category=UserWarning)
        
    # Create graph from numpy matrix
    G = nx.from_numpy_array(matrix)
    layout = nx.random_layout(G, seed=10)
        
    # Generate node colors
    num_nodes = len(G.nodes)
    colors = plt.cm.rainbow(np.linspace(0, 1, num_nodes))
        
    # Draw graph
    nx.draw(G, layout, node_color=colors)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
        
    # Save graph to a buffer instead of a file
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
        
    # Encode buffer contents to base64
    buffer.seek(0)
    b64_str = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
        
    return b64_str

def encode_image_to_base64(filename):
    with open(filename, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def draw_ansatz(ansatz):
    # Draw the ansatz circuit
    ansatz_buffer = io.BytesIO()
    ansatz.decompose().draw('mpl').savefig(ansatz_buffer, format='png')
    ansatz_buffer.seek(0)
    ansatz_b64_str = base64.b64encode(ansatz_buffer.read()).decode('utf-8')
    ansatz_buffer.close()

    return ansatz_b64_str

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)


if __name__ == "__main__":
    input_json = sys.argv[1]
    input_data = json.loads(input_json)

    # # Extract parameters
    adjacent_matrices = np.array(eval(input_data["adjacent_matrices"]))
    reps = int(input_data.get("reps", 2))
    seed = int(input_data.get("seed", 10598))
    QAOA_problems = input_data.get("QAOA_problems", "max_cut")

    image_filename = "graph.png"
    graph_image = visualise_graph(adjacent_matrices)

    if QAOA_problems == "max_cut":
        x, obj_value, ansatz = run_qaoa_maxcut(adjacent_matrices, reps, seed)
        circuit_image = draw_ansatz(ansatz) # Draw the ansatz circuit   
        result = {
            "problem": "max_cut",
            "solution": x.tolist(),  # Convert numpy array to list for JSON compatibility
            "objective_value": obj_value,
            "graph": graph_image,
            "circuit_image": circuit_image  # Add the circuit image to the result
        }
    elif QAOA_problems == "tsp":
        x, ansatz = run_qaoa_tsp(adjacent_matrices, reps, seed)
        circuit_image = draw_ansatz(ansatz) # Draw the ansatz circuit   
        result = {
            "problem": "tsp", 
            "solution": x.tolist(),  # Convert numpy array to list for JSON compatibility
            "graph": graph_image,
            "circuit_image": circuit_image  # Add the circuit image to the result
        }
    elif QAOA_problems == "general":
        hamiltonian = json.loads(input_data["hamiltonian"])
        pauli_list = [(term, coeff) for term, coeff in hamiltonian]
        qubit_op = SparsePauliOp.from_list(pauli_list)
        x, ansatz = run_general_qaoa(qubit_op, reps, seed)
        circuit_image = draw_ansatz(ansatz)
        result = {
            "problem": "general",
            "solution": x.tolist(),
            "circuit_image": circuit_image
        }
    else:
        result = {
            "error": f"Unknown option {input_data.get('QAOA_problems')}"
        }
    # Output the result in JSON format
    print(json.dumps(result,  cls=NumpyEncoder))