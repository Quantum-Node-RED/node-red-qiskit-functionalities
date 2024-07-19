import io
import base64
import json
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from qiskit.circuit.library import EfficientSU2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler import Target
from qiskit.circuit.controlflow import IfElseOp, SwitchCaseOp, ForLoopOp
 
# Default configuration
backend = FakeSherbrooke()
target = backend.target
 
qc = EfficientSU2(12, entanglement="circular", reps=1)

# Coupling map
coupling_map = target.build_coupling_map()
 
# Basis gates
basis_gates = list(target.operation_names)

# Device error ratesDefault configuration
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
  "qc_t_cm_bg_et": qc_t_cm_bg_et_str
}

print(json.dumps(result))

