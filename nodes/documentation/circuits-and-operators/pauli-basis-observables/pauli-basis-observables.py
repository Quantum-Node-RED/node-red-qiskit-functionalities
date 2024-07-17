from qiskit.quantum_info import SparsePauliOp

def decompose_observable_pauli_basis():
    # define the number of qubits
    n = 12
    
    # define the single Pauli terms as ("Paulis", [indices], coefficient)
    interactions = [("ZZ", [i, i + 1], 1) for i in range(n - 1)]  # we assume spins on a 1D line
    field = [("X", [i], -1) for i in range(n)]
    
    # build the operator
    hamiltonian = SparsePauliOp.from_sparse_list(interactions + field, num_qubits=n)

    import numpy as np
    from qiskit.quantum_info import SparsePauliOp
    
    matrix = np.array([[-1, 0, 0.5, -1],
            [0, 1, 1, 0.5],
            [0.5, 1, -1, 0],
            [-1, 0.5, 0, 1]])
    
    observable = SparsePauliOp.from_operator(matrix)
    print(observable)  


from qiskit.circuit import QuantumCircuit

def demonstrate_measure_in_pauli_bases():
    # create a circuit, where we would like to measure
    # q0 in the X basis, q1 in the Y basis and q2 in the Z basis
    circuit = QuantumCircuit(3)
    circuit.ry(0.8, 0)
    circuit.cx(0, 1)
    circuit.cx(1, 2)
    circuit.barrier()
    
    # diagonalize X with the Hadamard gate 
    circuit.h(0)
    
    # diagonalize Y with Hadamard as S^\dagger
    circuit.h(1)
    circuit.sdg(1)
    
    # the Z basis is the default, no action required here
    
    # measure all qubits
    circuit.measure_all()
    circuit.draw("mpl")
