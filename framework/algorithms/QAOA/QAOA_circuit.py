import sys
import json
import os
import numpy as np
from qiskit import QuantumCircuit
from qiskit.primitives import Sampler, Estimator
from qiskit.result import QuasiDistribution
from qiskit.quantum_info import Pauli, SparsePauliOp
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit_algorithms.utils import algorithm_globals
from qiskit.circuit.library import PauliEvolutionGate
from utils.image_helper import visualize_graph, save_circuit_image, encode_image_to_base64, combine_images
from utils.JSON_helper import NumpyEncoder
import matplotlib.pyplot as plt
from functools import partial

def objective_value(x, w):
    X = np.outer(x, (1 - x))
    w_01 = np.where(w != 0, 1, 0)
    return np.sum(w_01 * X)

def bitfield(n, L):
    result = np.binary_repr(n, L)
    return [int(digit) for digit in result]

def sample_most_likely(state_vector, num_qubits):
    # Ensure state_vector is a valid QuasiDistribution or array of probabilities
    if isinstance(state_vector, QuasiDistribution):
        values = list(state_vector.values())
    else:
        values = state_vector

    # Debug: Print the values to ensure they are correctly retrieved
    print(f"Values: {values}")
    
    # Find the index of the most likely state
    k = np.argmax(np.abs(values))
    
    # Generate the bitfield for the most likely state
    x = bitfield(k, num_qubits)
    
    # Debug: Check the bitfield generated
    print(f"Generated bitfield: {x}, Length: {len(x)}")
    
    # Reverse the bitfield (depends on endianness of your qubits)
    x.reverse()
    
    # Convert to numpy array and return
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

def define_optimizer(optimizer_type):
    if optimizer_type == "SPSA":
        optimizer = SPSA()
    else:
        optimizer = COBYLA()
    return optimizer

def qaoa_circuit(num_qubits, params, hamiltonian, reps, save_images=False, image_dir='images'):
    gamma, beta = params[:reps], params[reps:]

    qc = QuantumCircuit(num_qubits, num_qubits)  # Add classical registers equal to the number of qubits
    qc.h(range(num_qubits))  # Apply Hadamard gates to all qubits

    step_images = []
    os.makedirs(image_dir, exist_ok=True)

    for i in range(reps):
        # Apply the Cost Hamiltonian for any number of qubits involved
        for pauli_term, coeff in zip(hamiltonian.paulis, hamiltonian.coeffs):
            z_mask = pauli_term.z
            qubits = [idx for idx, z in enumerate(z_mask) if z]  # Identify qubits where Z is applied

            if len(qubits) == 1:  # Single-qubit Z term
                qc.rz(2 * gamma[i] * coeff.real, qubits[0])

            elif len(qubits) == 2:  # Two-qubit ZZ term (as before)
                j, k = qubits
                qc.cx(j, k)
                qc.rz(2 * gamma[i] * coeff.real, k)
                qc.cx(j, k)

            elif len(qubits) > 2:  # Multi-qubit interaction
                # Apply a sequence of CNOT gates and RZ for a multi-qubit term
                for j in range(len(qubits) - 1):
                    qc.cx(qubits[j], qubits[j + 1])
                qc.rz(2 * gamma[i] * coeff.real, qubits[-1])
                for j in range(len(qubits) - 2, -1, -1):
                    qc.cx(qubits[j], qubits[j + 1])

        if save_images:
            step_images.append(save_circuit_image(qc, os.path.join(image_dir, f"qaoa_circuit_step_cost_{i}.png")))
            plt.close()

        # Apply the Mixer Hamiltonian using RX rotations
        qc.rx(2 * beta[i], range(num_qubits))
        if save_images:
            step_images.append(save_circuit_image(qc, os.path.join(image_dir, f"qaoa_circuit_step_mixer_{i}.png")))
            plt.close()

    # Add measurement operations
    qc.measure(range(num_qubits), range(num_qubits))
    
    return qc, step_images


# def qaoa_circuit(num_qubits, params, hamiltonian, reps, save_images=False, image_dir='images'):
#     gamma, beta = params[:reps], params[reps:]

#     qc = QuantumCircuit(num_qubits, num_qubits)  # Add classical registers equal to the number of qubits
#     qc.h(range(num_qubits))  # Apply Hadamard gates to all qubits

#     step_images = []
#     os.makedirs(image_dir, exist_ok=True)

#     for i in range(reps):
#         print(f"--- Iteration {i+1} ---")
        
#         # Apply the Cost Hamiltonian for any number of qubits involved
#         for pauli_term, coeff in zip(hamiltonian.paulis, hamiltonian.coeffs):
#             z_mask = pauli_term.z
#             qubits = [idx for idx, z in enumerate(z_mask) if z]  # Identify qubits where Z is applied

#             if len(qubits) == 1:  # Single-qubit Z term
#                 print(f"RZ gate on qubit {qubits[0]} with angle {2 * gamma[i] * coeff.real}")
#                 qc.rz(2 * gamma[i] * coeff.real, qubits[0])

#             elif len(qubits) == 2:  # Two-qubit ZZ term (as before)
#                 j, k = qubits
#                 print(f"CX gate with control {j} and target {k}")
#                 qc.cx(j, k)
#                 print(f"RZ gate on qubit {k} with angle {2 * gamma[i] * coeff.real}")
#                 qc.rz(2 * gamma[i] * coeff.real, k)
#                 print(f"CX gate with control {j} and target {k}")
#                 qc.cx(j, k)

#             elif len(qubits) > 2:  # Multi-qubit interaction
#                 # Apply a sequence of CNOT gates and RZ for a multi-qubit term
#                 for j in range(len(qubits) - 1):
#                     print(f"CX gate with control {qubits[j]} and target {qubits[j+1]}")
#                     qc.cx(qubits[j], qubits[j + 1])
#                 print(f"RZ gate on qubit {qubits[-1]} with angle {2 * gamma[i] * coeff.real}")
#                 qc.rz(2 * gamma[i] * coeff.real, qubits[-1])
#                 for j in range(len(qubits) - 2, -1, -1):
#                     print(f"CX gate with control {qubits[j]} and target {qubits[j+1]}")
#                     qc.cx(qubits[j], qubits[j + 1])

#         # Apply the Mixer Hamiltonian using RX rotations
#         print(f"RX gates on all qubits with angle {2 * beta[i]}")
#         qc.rx(2 * beta[i], range(num_qubits))

#         print("---------------------")

#     # Add measurement operations
#     qc.measure(range(num_qubits), range(num_qubits))
    
#     return qc, step_images

# def qaoa_circuit(num_qubits, params, hamiltonian, reps, save_images=False, image_dir='images'):
#     gamma, beta = params[:reps], params[reps:]

#     qc = QuantumCircuit(num_qubits, num_qubits)  # Add classical registers equal to the number of qubits
#     qc.h(range(num_qubits))

#     mixer_hamiltonian = SparsePauliOp.from_list([('X' * num_qubits, -1)])

#     step_images = []

#     os.makedirs(image_dir, exist_ok=True)

#     for i in range(reps):
#         cost_op = PauliEvolutionGate(hamiltonian, time=gamma[i])
#         qc.append(cost_op, range(num_qubits))
#         if save_images:
#             step_images.append(save_circuit_image(qc, os.path.join(image_dir, f"qaoa_circuit_step_cost_{i}.png")))
#             plt.close()

#         mixer_op = PauliEvolutionGate(mixer_hamiltonian, time=beta[i])
#         qc.append(mixer_op, range(num_qubits))
#         if save_images:
#             step_images.append(save_circuit_image(qc, os.path.join(image_dir, f"qaoa_circuit_step_mixer_{i}.png")))
#             plt.close()

#     # Add measurement operations
#     qc.measure(range(num_qubits), range(num_qubits))
    
#     return qc, step_images

def calculate_expectation_value(counts, hamiltonian):
    energy = 0
    total_counts = sum(counts.values())

    for bitstring, count in counts.items():
        probability = count / total_counts
        state = np.array([int(bit) for bit in bitstring])
        value = 0

        for pauli_term, coeff in zip(hamiltonian.paulis, hamiltonian.coeffs):
            parity = 1
            for i, z in enumerate(pauli_term.z):
                if z and state[i] == 1:
                    parity *= -1
            value += coeff * parity

        energy += probability * value
        
    return energy

def objective_function(params, sampler, ansatz, hamiltonian, num_qubits, reps):
    # iteration_num += 1
    # print(f"Iteration {iteration_num}")
    qc, _ = ansatz(params, num_qubits, hamiltonian, reps)
    job = sampler.run(qc)
    result = job.result()
    counts = result.quasi_dists[0].binary_probabilities()
    energy = calculate_expectation_value(counts, hamiltonian)
    min_value.append(np.real(energy))
    return np.real(energy)

def ansatz(params, num_qubits, hamiltonian, reps, save_images=False, image_dir='images'):
    return qaoa_circuit(num_qubits, params, hamiltonian, reps, save_images, image_dir)

def run_general_qaoa(hamiltonian, num_qubits, reps=2, seed=10598, optimizer_type="COBYLA", save_images=False, image_dir='images'):
    algorithm_globals.random_seed = seed
    np.random.seed(seed)
    optimizer = define_optimizer(optimizer_type)

    os.makedirs(image_dir, exist_ok=True)
    initial_point = np.random.rand(2 * reps)
    
    # initial_qc, step_images = ansatz(initial_point, num_qubits, hamiltonian, reps)
    # if save_images:
    #     save_circuit_image(initial_qc, os.path.join(image_dir, "initial_qaoa_circuit.png"))
    #     plt.close()

    sampler = Sampler()
    
    # def objective_function(params):
    #     qc, _ = ansatz(params)
    #     job = sampler.run(qc)
    #     result = job.result()
    #     counts = result.quasi_dists[0].binary_probabilities()

    #     # Calculate the cut value based on the measurement outcomes
    #     max_cut_value = 0
    #     for bitstring, probability in counts.items():
    #         x = np.array([int(bit) for bit in bitstring])
    #         cut_value = objective_value(x, weight_matrix)
    #         max_cut_value += probability * cut_value
        
    #     # Since we're maximizing the cut value, return -max_cut_value for the optimizer to minimize
    #     return -max_cut_value

    # def objective_function(params):
    #     # Generate the quantum circuit based on the current parameters
    #     qc, _ = ansatz(params)
        
    #     # Use the Estimator to calculate the expectation value of the Hamiltonian
    #     estimator = Estimator()
    #     job = estimator.run([qc], [hamiltonian])
    #     energy = job.result().values[0]
        
    #     # Return the real part of the energy to avoid issues with complex numbers
    #     return np.real(energy)

    objective_function_with_fixed_arg = partial(objective_function, sampler=sampler, ansatz=ansatz, hamiltonian=hamiltonian, num_qubits=num_qubits, reps=reps)
    
    result = optimizer.minimize(objective_function_with_fixed_arg, x0=initial_point)
    print(f"Optimization Result: {result}")

    # Generate the final quantum circuit with the optimized parameters
    qc, _ = ansatz(result.x, num_qubits, hamiltonian, reps)
    job = sampler.run(qc)
    final_result = job.result()

    print(f"Final min value: {len(min_value)}")

    # Get the most likely bitstring from the final result
    x = sample_most_likely(final_result.quasi_dists[0], num_qubits)
    print(f"Solution bitstring: {x}")

    # Calculate the final objective value for the most likely bitstring
    final_cut_value = objective_value(x, weight_matrix)
    print(f"Final objective (cut) value: {final_cut_value}")

    # optimized_params = result.x
    # optimized_qc, _ = ansatz(optimized_params)
    save_images = True
    if save_images:
        save_circuit_image(qc, os.path.join(image_dir, "optimized_qaoa_circuit.png"))
        plt.close()

    return x, qc, final_cut_value

if __name__ == "__main__":

    json_file_path = "./test.json"
    with open(json_file_path, 'r') as j:
        input_data = json.loads(j.read())

    # input_json = sys.argv[1]
    # input_data = json.loads(input_json)

    reps = int(input_data.get("reps", 2))
    seed = int(input_data.get("seed", 10598))
    optimizer_type = input_data.get("optimizer", "COBYLA")

    image_dir = "qaoa_images"

    global iteration_num
    iteration_num = 0

    global min_value
    min_value = []

    # graph = None

    if "graph" in input_data and "adjacency_matrix" in input_data["graph"]:
        adjacency_matrices = np.array(eval(input_data["graph"]["adjacency_matrix"]))
        visualize_graph(adjacency_matrices, image_dir, "graph.png")
        graph = encode_image_to_base64(os.path.join(image_dir, "graph.png"))
        qubit_op, offset = get_operator(adjacency_matrices)
        global weight_matrix  # Define weight_matrix globally for the objective function
        weight_matrix = adjacency_matrices
    elif "hamiltonian" in input_data:
        hamiltonian = input_data["hamiltonian"]["terms"]
        pauli_list = [(term["pauli"], term["coeff"]) for term in hamiltonian]
        qubit_op = SparsePauliOp.from_list(pauli_list)
    else:
        raise ValueError("Missing graph or hamiltonian in input data")

    save_images = input_data.get("save_images", False)

    x, ansatz, output = run_general_qaoa(qubit_op, len(qubit_op.paulis[0]), reps, seed, optimizer_type, save_images, image_dir)
    if(save_images):
        initial_circuit_image = encode_image_to_base64(os.path.join(image_dir, "initial_qaoa_circuit.png"))
        optimized_circuit_image = encode_image_to_base64(os.path.join(image_dir, "optimized_qaoa_circuit.png"))
        combined_step_image_filename = combine_images(step_images, os.path.join(image_dir, "combined_qaoa_steps.png"))
        combined_step_image = encode_image_to_base64(combined_step_image_filename)
    
    result = {
        "solution": x.tolist(),
        "objective_value": str(output),  
        # "initial_circuit_image": initial_circuit_image,
        # "optimized_circuit_image": optimized_circuit_image,
        # "combined_step_image": combined_step_image,
        # "graph": graph,

    }

    print(json.dumps(result, cls=NumpyEncoder))
