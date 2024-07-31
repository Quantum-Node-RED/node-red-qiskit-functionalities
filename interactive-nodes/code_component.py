#The code components can be futher classified
#As in the Gate_componets will be their own class
#Maths_components will be their own class
#Tools_components will be their own class
#Circuit_components will be their own class
class Code_Component:
    # Circuits
    Quantum_Circuit_Begin = "{circuit_name} = QuantumCircuit({num_qubits})"
    measure = "{circuit_name}.meausre({qbit})"
    swap = "{circuit_name}.swap({qbit1}, {qbit2})"
    classical_register= "{var_name} = ClassicalRegister({num_qubits})"
    quantum_register= "{var_name} = QuantumRegister({num_qubits})"
    reset= "{circuit_name}.reset({qbit})"
    # Maths
    matrix = "{var_name} = np.array({matrix})"
    # Gates
    CX_gate = "{circuit_name}.cx({qbit1}, {qbit2})"
    CZ_gate = "{circuit_name}.cz({qbit1}, {qbit2})"
    CU_gate= "{circuit_name}.cu({theta}, {phi}, {lam}, {qbit1}, {qbit2})"
    H_gate = "{circuit_name}.h({qbit})"
    RX_gate = "{circuit_name}.rx({theta}, {qbit})"
    RZ_gate = "{circuit_name}.rz({theta}, {qbit})"
    RY_gate = "{circuit_name}.ry({theta}, {qbit})"
    SX_gate = "{circuit_name}.sx({qbit})"
    X_gate = "{circuit_name}.x({qbit})"
    barrier = "{circuit_name}.barrier({qbit})"
    phase = "{circuit_name}.p({theta}, {qbit})"
    I_gate = "{circuit_name}.i({qbit})"
    U_gate = "{circuit_name}.u({theta}, {phi}, {lam}, {qbit})"
    Toffoli_gate = "{circuit_name}.toffoli({qbit1}, {qbit2}, {qbit3})"
    CCX_gate = "{circuit_name}.ccx({qbit1}, {qbit2}, {qbit3})"
    mutli_controlled_U_gate="from qiskit.circuit.library import UGate\n{circuit_name}.mct({qbit1}, {qbit2}, {qbit3})"
    # Tools
    local_simulator = """
                default='qasm_simulator'
                {var_name} = Aer.get_backend({simulator} or default)
                {var_name_result} = execute({circuit_name}, backend = {var_name}, shots = %s).result()
                {var_name_counts} = {var_name_result}.get_counts()
                print({var_name_counts})
                """
    draw= "{circuit_name}.draw(output='{output_type}')"
    encode_image = """
                import matplotlib.pyplot as plt
                import base64
                import io
                import warnings
                warnings.filterwarnings("ignore", category=UserWarning)
                buffer = io.BytesIO()
                plt.savefig(buffer,  format='png')
                buffer.seek(0)
                b64_str = base64.b64encode(buffer.read())
                print(b64_str)
                buffer.close()
                """
    histogram = """
                from qiskit.visualization import plot_histogram
                simulator = Aer.get_backend('qasm_simulator')
                result = execute(qc, backend = simulator, shots = %s).result()
                plot_histogram(result.get_counts(), color='midnightblue', title="Circuit Output")   
                """


    def code_import(self):
        import_code = "import numpy as np\nfrom qiskit import QuantumCircuit\n"
        return import_code