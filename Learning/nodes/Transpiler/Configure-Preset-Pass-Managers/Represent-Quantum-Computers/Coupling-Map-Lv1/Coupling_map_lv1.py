import io
import base64
import json
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from qiskit.circuit.library import EfficientSU2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_circuit_layout
 
# Default configuration
backend = FakeSherbrooke()
target = backend.target
 
qc = EfficientSU2(12, entanglement="circular", reps=1)

# Coupling map
coupling_map = target.build_coupling_map()

pass_manager = generate_preset_pass_manager(
    optimization_level=1, coupling_map=coupling_map, seed_transpiler=12345
)
qc_t_cm_lv1 = pass_manager.run(qc)
# View the circuit
qc_buffer = io.BytesIO()
qc_t_cm_lv1.draw("mpl", idle_wires=False, fold=-1).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t_cm_lv1_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

qc_buffer = io.BytesIO()
plot_circuit_layout(qc_t_cm_lv1, backend, view="physical").savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t_cm_lv1_layout_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

result = {
  "qc_t_cm_lv1": qc_t_cm_lv1_str,
  "qc_t_cm_lv1_layout": qc_t_cm_lv1_layout_str
}

print(json.dumps(result))

