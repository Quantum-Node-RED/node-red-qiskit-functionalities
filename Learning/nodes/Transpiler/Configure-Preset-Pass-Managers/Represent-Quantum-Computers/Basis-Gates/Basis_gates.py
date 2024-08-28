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

# Coupling map
coupling_map = target.build_coupling_map()

# Basis gates
basis_gates = list(target.operation_names)
pass_manager = generate_preset_pass_manager(
    optimization_level=1,
    coupling_map=coupling_map,
    basis_gates=basis_gates,
    seed_transpiler=12345,
)
qc_t_cm_bg = pass_manager.run(qc)
qc_buffer = io.BytesIO()
qc_t_cm_bg.draw("mpl", idle_wires=False, fold=-1).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t_cm_bg_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

result = {
  "circuit_diagram": qc_t_cm_bg_str,
  "basis_gates": basis_gates,
}

print(json.dumps(result))

