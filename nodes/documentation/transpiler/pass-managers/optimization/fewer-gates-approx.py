import io
import base64
import json
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import random_unitary
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
 
 
UU = random_unitary(4, seed=12345)
rand_U = UnitaryGate(UU)

qc = QuantumCircuit(2)
qc.append(rand_U, range(2))
qc.swap(0, 1)
 
backend = FakeSherbrooke()

pass_manager = generate_preset_pass_manager(
    optimization_level=3,
    approximation_degree=0.99,
    backend=backend,
    seed_transpiler=12345,
)
qc_t3_approx = pass_manager.run(qc)

# View the circuit
qc_buffer = io.BytesIO()
qc_t3_approx.draw("mpl", idle_wires=False).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t3_approx_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

result = {
  "qc_t3_approx_image": qc_t3_approx_str
}

print(json.dumps(result))
