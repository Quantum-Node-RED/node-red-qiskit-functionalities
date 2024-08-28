import json
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import random_unitary
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# Approximation degree
UU = random_unitary(4, seed=12345)
rand_U = UnitaryGate(UU)
 
qubits = QuantumRegister(2, name="q")
qc = QuantumCircuit(qubits)
qc.append(rand_U, qubits)
pass_manager = generate_preset_pass_manager(
    optimization_level=1, approximation_degree=0.85, basis_gates=["sx", "rz", "cx"]
)
approx_qc = pass_manager.run(qc)
optimal_cx_num = approx_qc.count_ops()["cx"]

result = {
  "optimal_cx_num": optimal_cx_num
}

print(json.dumps(result))
