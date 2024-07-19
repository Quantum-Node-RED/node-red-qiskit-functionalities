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

# level 0
pass_manager = generate_preset_pass_manager(
    optimization_level=0, backend=backend, seed_transpiler=12345
)
qc_t0_exact = pass_manager.run(qc)
qc_buffer = io.BytesIO()
qc_t0_exact.draw("mpl", idle_wires=False).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t0_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

# level 1
pass_manager = generate_preset_pass_manager(
    optimization_level=1, backend=backend, seed_transpiler=12345
)
qc_t1_exact = pass_manager.run(qc)
qc_buffer = io.BytesIO()
qc_t1_exact.draw("mpl", idle_wires=False).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t1_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

# level 2
pass_manager = generate_preset_pass_manager(
    optimization_level=2, backend=backend, seed_transpiler=12345
)
qc_t2_exact = pass_manager.run(qc)
qc_buffer = io.BytesIO()
qc_t2_exact.draw("mpl", idle_wires=False).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t2_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

# level 3
pass_manager = generate_preset_pass_manager(
    optimization_level=3, backend=backend, seed_transpiler=12345
)
qc_t3_exact = pass_manager.run(qc)
qc_buffer = io.BytesIO()
qc_t3_exact.draw("mpl", idle_wires=False).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t3_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

result = {
  "qc_t0_image": qc_t0_str,
  "qc_t1_image": qc_t1_str,
  "qc_t2_image": qc_t2_str,
  "qc_t3_image": qc_t3_str
}

print(json.dumps(result))
