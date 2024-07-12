import io
import base64
import json
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from qiskit.circuit.library import EfficientSU2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.visualization import plot_circuit_layout
from qiskit.transpiler import Target
from qiskit.circuit.controlflow import IfElseOp, SwitchCaseOp, ForLoopOp
 
# Default configuration
backend = FakeSherbrooke()
target = backend.target
 
qc = EfficientSU2(12, entanglement="circular", reps=1)

# View the circuit
qc_buffer = io.BytesIO()
qc.decompose().draw("mpl").savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

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

# Coupling map
coupling_map = target.build_coupling_map()
 
pass_manager = generate_preset_pass_manager(
    optimization_level=0, coupling_map=coupling_map, seed_transpiler=12345
)
qc_t_cm_lv0 = pass_manager.run(qc)
# View the circuit
qc_buffer = io.BytesIO()
qc_t_cm_lv0.draw("mpl", idle_wires=False, fold=-1).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t_cm_lv0_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

qc_buffer = io.BytesIO()
plot_circuit_layout(qc_t_cm_lv0, backend, view="physical").savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t_cm_lv0_layout_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

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

# Device error rates

err_targ = Target.from_configuration(
    basis_gates=basis_gates,
    coupling_map=coupling_map,
    num_qubits=target.num_qubits,
    custom_name_mapping={ "if_else": IfElseOp, "switch_case": SwitchCaseOp, "for_loop": ForLoopOp },
)
 
for i, (op, qargs) in enumerate(target.instructions):
    if op.name in basis_gates:
        err_targ[op.name][qargs] = target.instruction_properties(i)

pass_manager = generate_preset_pass_manager(
    optimization_level=1, target=err_targ, seed_transpiler=12345
)
qc_t_cm_bg_et = pass_manager.run(qc)
qc_buffer = io.BytesIO()
qc_t_cm_bg_et.draw("mpl", idle_wires=False, fold=-1).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t_cm_bg_et_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

result = {
  "qc_image": qc_str, 
  "qc_t_target": qc_t_target_str,
  "qc_t_cm_lv0": qc_t_cm_lv0_str,
  "qc_t_cm_lv0_layout": qc_t_cm_lv0_layout_str,
  "qc_t_cm_lv1": qc_t_cm_lv1_str,
  "qc_t_cm_lv1_layout": qc_t_cm_lv1_layout_str,
  "qc_t_cm_bg": qc_t_cm_bg_str,
  "qc_t_cm_bg_et": qc_t_cm_bg_et_str,
  "basis_gates": basis_gates,
}

print(json.dumps(result))

