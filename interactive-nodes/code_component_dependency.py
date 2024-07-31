#This is for import optimiztion, that is importing only the required modules, rather than using a wildcard import
# "Component":["Module","Alias"]
class Code_Component_Dependency:
    table={
        "Quantum_Circuit":["qiskit.QuantumCircuit"],
        "Matrix":["numpy","np"],
        "CX_gate":["qiskit.circuit.library.CXGate"],
        "CZ_gate":["qiskit.circuit.library.CZGate"],
        "H_gate":["qiskit.circuit.library.HGate"],
        "RX_gate":["qiskit.circuit.library.RXGate"],
        "RZ_gate":["qiskit.circuit.library.RZGate"],
        "SX_gate":["qiskit.circuit.library.SXGate"],
        "X_gate":["qiskit.circuit.library.XGate"],
    }