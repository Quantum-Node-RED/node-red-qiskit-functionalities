# This is for import optimiztion, that is importing only the required modules, rather than using a wildcard import
# "Component":["Module","Alias"]
class Component_Dependency:
    Quantum_Circuit = ["qiskit.QuantumCircuit",]
    Classical_Register = ["qiskit.ClassicalRegister"]
    Quantum_Register = ["qiskit.QuantumRegister"]
    Numpy = ["numpy", "np"]
    CX_gate = ["qiskit.circuit.library.CXGate"]
    CZ_gate = ["qiskit.circuit.library.CZGate",]
    H_gate = ["qiskit.circuit.library.HGate"]
    RX_gate = ["qiskit.circuit.library.RXGate"]
    RZ_gate = ["qiskit.circuit.library.RZGate"]
    SX_gate = ["qiskit.circuit.library.SXGate"]
    X_gate = ["qiskit.circuit.library.XGate"]
    U_gate = ["qiskit.circuit.library.UGate"]
    Qiskit_runtime_service = ["qiskit_ibm_runtime.QiskitRuntimeService"]
    Aer = ["qiskit_aer.AerSimulator"]
    Execute = ["qiskit.execute"]
    Plot_histogram = ["qiskit.visualization.plot_histogram"]
    SparsePauliOp = ["qiskit.quantum_info.SparsePauliOp"]
    QuasiDistribution = ["qiskit.result.QuasiDistribution"]
    QAOA = ["qiskit_algorithms.QAOA"]
    VQE = ["qiskit_algorithms.VQE"]
    Optimizers = ["qiskit_algorithms.optimizers.{optimizer}"]
    Pyplot = ["matplotlib.pyplot", "plt"]
    Base64 = ["base64"]
    IO = ["io"]
    Warnings = ["warnings"]
    NetworkX = ["networkx", "nx"]
    OS = ["os"]
    JSON = ["json"]
    Pauli=["qiskit.quantum_info.Pauli"]
    Sampler=["qiskit.primitives.Sampler"]
    ParameterVector=["qiskit.circuit.ParameterVector"]
    Estimator=["qiskit.primitives.Estimator"]
    Minimize=["scipy.optimize.minimize"]
    Session=["qiskit_ibm_runtime.Session"]
    SamplerV2=["qiskit_ibm_runtime.SamplerV2", "Sampler"]
    Generate_preset_pass_manager=["qiskit.transpiler.preset_passmanagers.generate_preset_pass_manager"]






