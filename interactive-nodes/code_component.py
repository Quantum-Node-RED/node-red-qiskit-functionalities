class Code_Component:
    # Class variables
    import_statement = ""
    function = ""
    calling_function = ""

    def __init__(self, import_statement, function, calling_function):
        # Initialize the instance variables with provided values
        self.import_statement = import_statement
        self.function = function
        self.calling_function = calling_function

    def display_component(self):
        # Method to display the details of the code component
        print("Import Statement:")
        print(self.import_statement)
        print("\nFunction Definition:")
        print(self.function)
        print("\nCalling Function:")
        print(self.calling_function)

# Create an instance of the Code_Component class    

snippets = {

    # Circuit
    "Quantum_Circuit_Begin": Code_Component(
        import_statement=["QISKIT_QUANTUM_CIRCUIT"],
        function="",
        calling_function="{circuit_name} = QuantumCircuit({num_qbits})"
    ),

    "measure": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.measure({qbit})"
    ),

    "swap": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.swap({qbit1}, {qbit2})"
    ),

    "classical_register": Code_Component(
        import_statement=["QISKIT_CLASSICAL_REGISTER"],
        function="",
        calling_function="{var_name} = ClassicalRegister({num_qbits})"
    ),

    "quantum_register": Code_Component(
        import_statement=["QISKIT_QUANTUM_REGISTER"],
        function="",
        calling_function="{var_name} = QuantumRegister({num_qbits})"
    ),

    "reset": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.reset({qbit})"
    ),
    
    "barrier": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.barrier({qbit})"
    ),

    # Maths
    "matrix": Code_Component(
        import_statement=["NUMPY"],
        function="",
        calling_function="{var_name} = np.array(eval({matrix}))"
    ),

    # Gates
    "CX_gate": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.cx({control_qubit}, {target_qubit})"
    ),

    "CZ_gate": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.cz({control_qubit}, {target_qubit})"
    ),

    "CU_gate": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.cu({theta}, {phi}, {lam},{gamma}, {control_qubit}, {target_qubit})"
    ),

    "H_gate": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.h({qbit})"
    ),

    "RX_gate": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.rx({theta}, {qbit})"
    ),

    "RZ_gate": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.rz({theta}, {qbit})"
    ),

    "RY_gate": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.ry({theta}, {qbit})"
    ),

    "SX_gate": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.sx({qbit})"
    ),

    "X_gate": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.x({qbit})"
    ),

    "phase": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.p({theta}, {qbit})"
    ),

    "I_gate": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.i({qbit})"
    ),

    "U_gate": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.u({theta}, {phi}, {lam}, {qbit})"
    ),

    "Toffoli_gate": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.toffoli({control_qubit1}, {control_qubit2}, {target_qubit})"
    ),

    "CCX_gate": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.ccx({control_qubit1}, {control_qubit2}, {target_qubit})"
    ),

    "multi_controlled_U_gate": Code_Component(
        import_statement=["QISKIT_CIRCUIT_LIBRARY"],
        function="",
        calling_function="{circuit_name}.append(UGate({theta}, {phi}, {lam}).control({num_of_control_qubits}), {list_of_control_qubits}+{target_qubit}))"
    ),

    # Tools
    "local_simulator": Code_Component(
        import_statement=["QISKIT_AER_EXECUTE"],
        function="",
        calling_function="""
            default='qasm_simulator'
            {var_name} = Aer.get_backend({simulator} or default)
            {var_name_result} = execute({circuit_name}, backend={var_name}, shots={shots}).result()
            {var_name_counts} = {var_name_result}.get_counts()
            print({var_name_counts})
        """
    ),

    "draw": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.draw(output='{output_type}')"
    ),

    "encode_image": Code_Component(
        import_statement=[
            "PYPLOT",
            "IO",
            "WARNINGS",
            "BASE64"
        ],
        function="warnings.filterwarnings('ignore', category=UserWarning)",
        calling_function="""
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            b64_str = base64.b64encode(buffer.read())
            print(b64_str)
            buffer.close()
        """
    ),

    "draw_circuit": Code_Component(
        import_statement=[
            "PYPLOT",
            "IO",
            "BASE64",
            "JSON"
        ],
        function="",
        calling_function="""
buffer = io.BytesIO()
{circuit_name}.draw(output='mpl').savefig(buffer, format='png')
buffer.seek(0)
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()
print(json.dumps(b64_str))
"""
    ),

    "histogram": Code_Component(
        import_statement=["QISKIT_VISUALIZATION_HISTOGRAM"],
        function="",
        calling_function="""
            simulator = Aer.get_backend('qasm_simulator')
            result = execute(qc, backend=simulator, shots=%s).result()
            plot_histogram(result.get_counts(), color='midnightblue', title='Circuit Output')
        """
    ),

    # Function
    "sparse_pauli_op": Code_Component(
        import_statement=["QISKIT_SPARSE_PAULI_OP"],
        function="",
        calling_function="SparsePauliOp({pauli_list}, coeffs={coeffs})"
    ),

    # Visualisation
    "draw_graph": Code_Component(
        import_statement=[
            "NETWORKX",
            "NUMPY",
            "PYPLOT",
            "OS"
        ],
        function="",
        calling_function="""
            G = nx.from_numpy_array({matrix})
            layout = nx.random_layout(G, seed=10)
            num_nodes = len(G.nodes)
            colors = plt.cm.rainbow(np.linspace(0, 1, num_nodes))
            nx.draw(G, layout, node_color=colors)
            labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=labels)
            os.makedirs(folder, exist_ok=True)
            filepath = os.path.join(folder, filename)
            plt.savefig(filepath)
            plt.close()
        """
    ),

    # Algorithms - QAOA
    "apply_objective_value": Code_Component(
        import_statement=["NUMPY"],
        function="""def objective_value(x, w):
    X = np.outer(x, (1 - x))
    w_01 = np.where(w != 0, 1, 0)
    return np.sum(w_01 * X)""",
        calling_function="""
            {var_result} = objective_value({binary_vector}, {matrix})
        """
    ),

    "apply_bitfield": Code_Component(
        import_statement=["NUMPY"],
        function="""def bitfield(n, L):
    result = np.binary_repr(n, L)
    return [int(digit) for digit in result]""",
        calling_function="""
            {var_result} = bitfield({integer_value}, {bit_length})
        """
    ),

    "extract_most_likely_state": Code_Component(
        import_statement=[
            "NUMPY", 
            "QISKIT_RESULT_QUASI_DISTRIBUTION"  # Using the defined import for QuasiDistribution
        ],
        function="""def extract_most_likely_state(state_vector):
    if isinstance(state_vector, QuasiDistribution):
        values = list(state_vector.values())
    else:
        values = state_vector
    n = int(np.log2(len(values)))
    k = np.argmax(np.abs(values))
    x = bitfield(k, n)
    x.reverse()
    return np.asarray(x)""",
        calling_function="""
            {var_result} = extract_most_likely_state({state_vector})
        """
    ),

    "apply_hamiltonian": Code_Component(
        import_statement=[],
        function="",
        calling_function=""
    ),

    "QAOA": Code_Component(
        import_statement=[
            "QISKIT_ALGORITHMS_QAOA", 
            "QISKIT_ALGORITHMS_OPTIMIZERS"  # Using the defined import for QAOA and Optimizer
        ],
        function="",
        calling_function="{var_result} = QAOA({sampler}, {optimizer}(), reps={reps})"
    )
}
