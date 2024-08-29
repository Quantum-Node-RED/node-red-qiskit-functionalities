import io
import base64
import json
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import random_unitary
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from qiskit.transpiler import Layout
 
# Approximation degree
UU = random_unitary(4, seed=12345)
rand_U = UnitaryGate(UU)
 
qubits = QuantumRegister(2, name="q")
qc = QuantumCircuit(qubits)
qc.append(rand_U, qubits)

# Initial layout
backend = FakeSherbrooke()
 
a, b = qubits
initial_layout = Layout({a: 5, b: 6})
# list form
# initial_layout = [5, 6]
 
pass_manager = generate_preset_pass_manager(
    optimization_level=1, backend=backend, initial_layout=initial_layout
)
transpiled_circ = pass_manager.run(qc)
 
# View the circuit
qc_buffer = io.BytesIO()
transpiled_circ.draw("mpl", idle_wires=False).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
transpiled_circ_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

result = {
  "circuit_diagram": transpiled_circ_str
}

print(json.dumps(result))
