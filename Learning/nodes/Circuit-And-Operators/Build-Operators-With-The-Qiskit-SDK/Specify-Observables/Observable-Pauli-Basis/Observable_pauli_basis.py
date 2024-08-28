import numpy as np
from qiskit.quantum_info import SparsePauliOp
import json


def create_hamiltonian(n, interaction_coeff=1, field_coeff=-1):
    """
    Creates a Hamiltonian for an n-qubit system.
    
    Parameters:
    n (int): Number of qubits.
    interaction_coeff (float): Coefficient for the ZZ interaction terms.
    field_coeff (float): Coefficient for the X field terms.
    
    Returns:
    SparsePauliOp: The Hamiltonian as a SparsePauliOp object.
    """
    # Define the single Pauli terms as ("Paulis", [indices], coefficient)
    interactions = [("ZZ", [i, i + 1], interaction_coeff) for i in range(n - 1)]
    field = [("X", [i], field_coeff) for i in range(n)]
    
    # Build the operator
    hamiltonian = SparsePauliOp.from_sparse_list(interactions + field, num_qubits=n)
    return hamiltonian

def measure_magnetization(n):
    """
    Measures the average magnetization in the Z-direction for an n-qubit system.
    
    Parameters:
    n (int): Number of qubits.
    
    Returns:
    SparsePauliOp: The magnetization observable as a SparsePauliOp object.
    """
    magnetization_terms = [("Z", [i], 1/n) for i in range(n)]
    
    # Build the magnetization observable
    magnetization = SparsePauliOp.from_sparse_list(magnetization_terms, num_qubits=n)
    return magnetization

def decompose_matrix(matrix):
    """
    Decomposes a given matrix into Pauli terms.
    
    Parameters:
    matrix (numpy.ndarray): The matrix to decompose.
    
    Returns:
    SparsePauliOp: The observable as a SparsePauliOp object.
    """
    observable = SparsePauliOp.from_operator(matrix)
    return observable

# Example usage
if __name__ == "__main__":
    # Define the number of qubits
    n = 12
    
    # Create Hamiltonian
    hamiltonian = create_hamiltonian(n)
    # print("Hamiltonian:")
    # print(hamiltonian)
    # print()

    # Measure magnetization
    magnetization = measure_magnetization(n)
    # print("Magnetization:")
    # print(magnetization)
    # print()
    
    # Decompose a given matrix into Pauli terms
    matrix = np.array([[-1, 0, 0.5, -1],
                       [0, 1, 1, 0.5],
                       [0.5, 1, -1, 0],
                       [-1, 0.5, 0, 1]])
    
    observable = decompose_matrix(matrix)
    # print("Observable from Matrix:")
    # print(observable)

    result = {
        "observable": str(observable)
    }

    print(json.dumps(result))

