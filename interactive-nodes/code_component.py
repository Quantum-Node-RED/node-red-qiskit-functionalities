from code_component_dependency import Component_Dependency
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
        import_statement=[Component_Dependency.Quantum_Circuit,],
        function="",
        calling_function="{circuit_name} = QuantumCircuit({num_qbits}, {num_cbits})"
    ),

    "measure": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.measure({qbit}, {cbit})"
    ),

    "swap": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.swap({qbit1}, {qbit2})"
    ),

    "classical_register": Code_Component(
        import_statement=[Component_Dependency.Classical_Register],
        function="",
        calling_function="{var_name} = ClassicalRegister({num_qbits})"
    ),

    "quantum_register": Code_Component(
        import_statement=[Component_Dependency.Quantum_Register],
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
        import_statement=[Component_Dependency.Numpy],
        function="",
        calling_function="""{var_name} = np.array(eval({matrix}))"""
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
        import_statement=[Component_Dependency.U_gate],
        function="",
        calling_function="{circuit_name}.append(UGate({theta}, {phi}, {lam}).control({num_of_control_qubits}), {list_of_control_qubits}+{target_qubit}))"
    ),

    # Tools
    "local_simulator": Code_Component(
        import_statement=[Component_Dependency.Aer, Component_Dependency.Execute],
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
            Component_Dependency.Pyplot,
            Component_Dependency.IO,
            Component_Dependency.Warnings,
            Component_Dependency.Base64
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
            Component_Dependency.Pyplot,
            Component_Dependency.IO,
            Component_Dependency.Base64,
            Component_Dependency.JSON
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
        import_statement=[Component_Dependency.Plot_histogram],
        function="",
        calling_function="""
            simulator = Aer.get_backend('qasm_simulator')
            result = execute(qc, backend=simulator, shots=%s).result()
            plot_histogram(result.get_counts(), color='midnightblue', title='Circuit Output')
        """
    ),

    # Function
    "sparse_pauli_op": Code_Component(
        import_statement=[Component_Dependency.SparsePauliOp],
        function="",
        calling_function="""pauli_list = {pauli_list}
coeffs = {coeffs}
{variable} = SparsePauliOp(pauli_list, coeffs=coeffs)
        """
    ),

    # Visualisation
    "draw_graph": Code_Component(
        import_statement=[
            Component_Dependency.NetworkX,
            Component_Dependency.Numpy,
            Component_Dependency.Pyplot,
            Component_Dependency.OS
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
        import_statement=[Component_Dependency.Numpy],
        function="""def objective_value(x, w):
    X = np.outer(x, (1 - x))
    w_01 = np.where(w != 0, 1, 0)
    return np.sum(w_01 * X)""",
        calling_function="""
            {variable} = objective_value({binary_vector}, {matrix})
        """
    ),

    "apply_bitfield": Code_Component(
        import_statement=[Component_Dependency.Numpy],
        function="""def bitfield(n, L):
    result = np.binary_repr(n, L)
    return [int(digit) for digit in result]""",
        calling_function="""
            {var_result} = bitfield({integer_value}, {bit_length})
        """
    ),

    "extract_most_likely_state": Code_Component(
        import_statement=[
            Component_Dependency.Numpy, 
            Component_Dependency.QuasiDistribution  # Using the defined import for QuasiDistribution
        ],
        function="""def extract_most_likely_state(state_vector, num_qubits):
    if isinstance(state_vector, QuasiDistribution):
        values = list(state_vector.values())
    else:
        values = state_vector
    k = np.argmax(np.abs(values))
    result = np.binary_repr(k, num_qubits)
    x = [int(digit) for digit in result]
    x.reverse()
    return np.asarray(x)""",
        calling_function="""
            {variable} = extract_most_likely_state({state_vector}.quasi_dists[0], {num_qubits})
        """
    ),

    "apply_hamiltonian": Code_Component(
        import_statement=[
                    Component_Dependency.Pauli,
                    Component_Dependency.SparsePauliOp,
                    Component_Dependency.Numpy],
        function="""def get_operator(weight_matrix):
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

    return SparsePauliOp(pauli_list, coeffs=coeffs), shift""",
        calling_function="qubit_op, offset = get_operator(weight_matrix)"
    ),

    "define_sampler": Code_Component(
        import_statement=[Component_Dependency.Sampler],
        function="",
        calling_function="{variable} = Sampler()"
    ),

    "apply_optimizer": Code_Component(
        import_statement=[Component_Dependency.Optimizers],
        function="",
        calling_function="{var_result} = {optimizer}.minimize({objective_function}, x0={initial_point})"
    ),

    "apply_energy_cost_objective_function": Code_Component(
        import_statement=[Component_Dependency.Numpy],
        function="""def objective_function(params):
        qc, _ = ansatz(params)
        job = sampler.run(qc)
        result = job.result()
        counts = result.quasi_dists[0].binary_probabilities()
        energy = calculate_expectation_value(counts, hamiltonian)
        return np.real(energy)
        """,
        calling_function=""
    ),

    "execute_quantum_circuit_with_sampler": Code_Component(
        import_statement=[],
        function="""
    def execute_circuit_with_sampler(qc, sampler):
        job = sampler.run(qc)
        result = job.result()
        return result
    """,
        calling_function="""
    {circuit_name}.measure(range(4), range(4))
{variable} = execute_circuit_with_sampler({circuit_name}, {sampler})
    """
    ),

    "print": Code_Component(
        import_statement=[],
        function="",
        calling_function="""print("result: ", {variable})"""
    ),

    "QAOA": Code_Component(
        import_statement=[
            Component_Dependency.QAOA, 
            Component_Dependency.Optimizers  # Using the defined import for QAOA and Optimizer
        ],
        function="",
        calling_function="{var_result} = QAOA({sampler}, {optimizer}(), reps={reps})"
    ),
    # VQE: 
    "initialize_parameters": Code_Component(
        import_statement=[
            Component_Dependency.ParameterVector,
            Component_Dependency.Numpy
        ],
        function="",
        calling_function="""theta = ParameterVector('θ', {num_thetas})
initial_params = 2 * np.pi * np.random.random({num_thetas})
        """
    ),
    "estimator": Code_Component(
        import_statement=[
            Component_Dependency.Estimator,
        ],
        function="",
        calling_function="estimator = Estimator()"
    ),
}
