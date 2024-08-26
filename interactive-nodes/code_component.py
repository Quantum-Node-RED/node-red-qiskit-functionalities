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

    "measure_all": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.measure(range({num_qbits}), range({num_cbits}))"
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
        calling_function="{circuit_name}.id({qbit})"
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
        import_statement=[Component_Dependency.Aer,
                         Component_Dependency.Session,
                         Component_Dependency.SamplerV2,
                         Component_Dependency.Generate_preset_pass_manager],
        function="",
        calling_function="""
aer_sim = AerSimulator()
pm=generate_preset_pass_manager(backend=aer_sim, optimization_level={optimization_level})
isa_qc=pm.run({circuit_name})
with Session (backend=aer_sim) as session:
    sampler = Sampler()
    result = sampler.run([isa_qc]).result()
print(result)
        """
    ),

    "draw": Code_Component(
        import_statement=[],
        function="",
        calling_function="{circuit_name}.draw(output='{output_type}')"
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

    "custom_programming": Code_Component(
        import_statement=[],
        function="",
        calling_function="{custom_code}"
    ),

    "draw_graph": Code_Component(
        import_statement=[
        Component_Dependency.NetworkX,
        Component_Dependency.Numpy,
        Component_Dependency.Pyplot,
        Component_Dependency.IO,
        Component_Dependency.Base64,
        Component_Dependency.Warnings,
        Component_Dependency.JSON
    ],
        function="""def visualise_graph(matrix):
        
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
        
    return b64_str""",
        calling_function="""{variable} = visualise_graph({matrix})
print(json.dumps({variable}))"""
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
        calling_function="{operator_name}, offset = get_operator(weight_matrix)"
    ),

    "define_sampler": Code_Component(
        import_statement=[Component_Dependency.Sampler],
        function="",
        calling_function="{variable} = Sampler()"
    ),

    "apply_optimizer": Code_Component(
        import_statement=[Component_Dependency.Minimize],
        function="",
        calling_function="""{variable} = minimize({cost_function}, initial_params, args=({circuit_name}, {param_vector}, {hamiltonian}, {estimator}), method="{optimizer}")"""
    ),

    "apply_energy_cost_objective_function": Code_Component(
        import_statement=[Component_Dependency.Numpy],
        function="""def objective_function(params, qc, param_vector, hamiltonian, estimator):
    assigned_qc = qc.assign_parameters({{param_vector: params}})
    energy = estimator.run(circuits=[assigned_qc], observables=[hamiltonian]).result().values[0]
    return np.real(energy)
        """,
        calling_function=""
    ),

    "execute_quantum_circuit_with_sampler": Code_Component(
        import_statement=[],
        function="""
    def execute_circuit_with_sampler(qc, sampler, params, param_vector):
        assigned_qc = qc.assign_parameters({{param_vector: params}})
        job = sampler.run(assigned_qc)
        result = job.result()
        return result
    """,
        calling_function="""{variable} = execute_circuit_with_sampler({circuit_name}, {sampler}, {result}.x, {param_vector})"""
    ),

    "print": Code_Component(
        import_statement=[],
        function="",
        calling_function="""print("{variable_name}: ", {variable})"""
    ),

    "QAOA": Code_Component(
        import_statement=[
            Component_Dependency.QAOA, 
            Component_Dependency.Optimizers  # Using the defined import for QAOA and Optimizer
        ],
        function="",
        calling_function="{var_result} = QAOA({sampler}, {optimizer}(), reps={reps})"
    ),

    "define_parameter": Code_Component(
        import_statement=[
            Component_Dependency.ParameterVector, 
            Component_Dependency.Numpy
        ],
        function="",
        calling_function="""initial_params = {initial_param}
{variable} = ParameterVector('θ', length={number_of_parameter} * {number_of_reps})"""
    ),

    "hyper_parameters": Code_Component(
        import_statement=[],
        function="",
        calling_function="{variable} = {value}"
    ),

    "estimator": Code_Component(
        import_statement=[
            Component_Dependency.Estimator,
        ],
        function="",
        calling_function="{variable} = Estimator()\n"
    ),
}
