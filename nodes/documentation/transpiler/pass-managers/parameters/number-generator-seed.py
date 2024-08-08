import io
import base64
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

# Random number generator seed
pass_manager = generate_preset_pass_manager(
    optimization_level=1, seed_transpiler=11, basis_gates=["sx", "rz", "cx"]
)
optimized_1 = pass_manager.run(qc)
qc_buffer = io.BytesIO()
optimized_1.draw("mpl").savefig(qc_buffer, format='png')
qc_buffer.seek(0)
optimized_1_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()
 

result = {
  "optimized_1_image": optimized_1_str
}

print(json.dumps(result))
