import io
import base64
import json
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from qiskit.circuit.library import EfficientSU2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
 
# Default configuration
backend = FakeSherbrooke()
target = backend.target
 
qc = EfficientSU2(12, entanglement="circular", reps=1)

pass_manager = generate_preset_pass_manager(
    optimization_level=1, target=target, seed_transpiler=12345
)
qc_t_target = pass_manager.run(qc)
# View the circuit
qc_buffer = io.BytesIO()
qc_t_target.draw("mpl", idle_wires=False, fold=-1).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t_target_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

result = {
  "circuit_diagram": qc_t_target_str
}

print(json.dumps(result))

