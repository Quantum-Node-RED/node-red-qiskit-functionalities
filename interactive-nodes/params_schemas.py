# schemas.py

schemas = {
    "Quantum_Circuit_Begin": {
        "circuit_name": str,
        "num_qbits": int
    },
    "measure": {
        "circuit_name": str,
        "qbit": int
    },
    "swap": {
        "circuit_name": str,
        "qbit1": int,
        "qbit2": int
    },
    "classical_register": {
        "var_name": str,
        "num_qbits": int
    },
    "quantum_register": {
        "var_name": str,
        "num_qbits": int
    },
    "reset": {
        "circuit_name": str,
        "qbit": int
    },
    "barrier": {
        "circuit_name": str,
        "qbit": int
    },
    "matrix": {
        "var_name": str,
        "matrix": str
    },
    "CX_gate": {
        "circuit_name": str,
        "control_qubit": int,
        "target_qubit": int
    },
    "CZ_gate": {
        "circuit_name": str,
        "control_qubit": int,
        "target_qubit": int
    },
    "CU_gate": {
        "circuit_name": str,
        "theta": float,
        "phi": float,
        "lam": float,
        "control_qubit": int,
        "target_qubit": int
    },
    "H_gate": {
        "circuit_name": str,
        "qbit": int
    },
    "RX_gate": {
        "circuit_name": str,
        "theta": float,
        "qbit": int
    },
    "RZ_gate": {
        "circuit_name": str,
        "theta": float,
        "qbit": int
    },
    "RY_gate": {
        "circuit_name": str,
        "theta": float,
        "qbit": int
    },
    "SX_gate": {
        "circuit_name": str,
        "qbit": int
    },
    "X_gate": {
        "circuit_name": str,
        "qbit": int
    },
    "barrier": {
        "circuit_name": str,
        "qbit": int
    },
    "phase": {
        "circuit_name": str,
        "theta": float,
        "qbit": int
    },
    "I_gate": {
        "circuit_name": str,
        "qbit": int
    },
    "U_gate": {
        "circuit_name": str,
        "theta": float,
        "phi": float,
        "lam": float,
        "qbit": int
    },
    "Toffoli_gate": {
        "circuit_name": str,
        "control_qubit1": int,
        "control_qubit2": int,
        "target_qubit": int
    },
    "CCX_gate": {
        "circuit_name": str,
        "control_qubit1": int,
        "control_qubit2": int,
        "target_qubit": int
    },
    "multi_controlled_U_gate": {
        "circuit_name": str,
        "num_of_control_qubits": int,
        "list_of_control_qubits": int,
        "target_qubit": int
    },
    "local_simulator": {
        "var_name": str,
        "circuit_name": str,
        "simulator": str,
        "var_name_result": str,
        "var_name_counts": str
    },
    "draw": {
        "circuit_name": str,
        "output_type": str
    },
    "encode_image": {},
    "draw_circuit": {
        "circuit_name": str,
    },
    "histogram": {},
    "sparse_pauli_op": {
        "pauli_list":  str,
        "coeffs":  str
    },
    "draw_graph": {
        "matrix":  str,
        "folder": str,
        "filename": str
    },
    "apply_objective_value": {
        "binary_vector":  str,
        "matrix": str,
        "var_result": str
    },
    "apply_bitfield": {
        "integer_value": int,
        "bit_length": int,
        "var_result": str
    },
    "extract_most_likely_state": {
        "state_vector":  str,
        "var_result": str
    },
    "apply_hamiltonian": {},
    "QAOA": {
        "sampler": str,
        "optimizer": str,
        "reps": int,
        "var_result": str
    }
}
