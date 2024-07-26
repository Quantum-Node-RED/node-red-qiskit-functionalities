import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import sys
import json
import base64
import io
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import Sampler
from qiskit.result import QuasiDistribution
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit_algorithms.utils import algorithm_globals

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

def define_optimizer(optimizer_type):
    if optimizer_type == "SPSA":
        optimizer = SPSA()
    else:
        optimizer = COBYLA()

    return optimizer

def run_general_qaoa(hamiltonian, reps=2, seed=10598, optimizer_type="COBYLA"):
    algorithm_globals.random_seed = seed
    optimizer = define_optimizer(optimizer_type)
    sampler = Sampler()
    qaoa = QAOA(sampler, optimizer, reps=reps)
    result = qaoa.compute_minimum_eigenvalue(hamiltonian)
    x = sample_most_likely(result.eigenstate)
    return x, qaoa.ansatz

def visualize_graph(w, filename="graph.png"):
    G = nx.from_numpy_array(w)
    layout = nx.random_layout(G, seed=10)
    colors = ["r", "g", "b", "y"]
    nx.draw(G, layout, node_color=colors)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
    # Save the plot as an image
    plt.savefig(filename)
    plt.close()

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

    if "graph" in input_data and "adjacency_matrix" in input_data["graph"]:
        adjacency_matrices = np.array(eval(input_data["graph"]["adjacency_matrix"]))

    reps = int(input_data.get("reps", 2))
    seed = int(input_data.get("seed", 10598))

    optimizer_type = input_data.get("optimizer", "COBYLA")

    if "hamiltonian" in input_data:
        hamiltonian = input_data["hamiltonian"]["terms"]
        pauli_list = [(term["pauli"], term["coeff"]) for term in hamiltonian]
        qubit_op = SparsePauliOp.from_list(pauli_list)
    else:
        raise ValueError("Missing hamiltonian in input data")

    x, ansatz = run_general_qaoa(qubit_op, reps, seed, optimizer_type)
    circuit_image = draw_ansatz(ansatz)
    result = {
        "problem": "general",
        "solution": x.tolist(),
        "circuit_image": circuit_image,
    }

    # Output the result in JSON format
    print(json.dumps(result, cls=NumpyEncoder))
