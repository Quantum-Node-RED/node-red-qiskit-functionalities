import json
import base64
import io

from qiskit_ibm_runtime.fake_provider import FakeKyoto
from qiskit.circuit import QuantumCircuit, Gate
from qiskit.pulse import builder, DriveChannel
from qiskit.transpiler import InstructionProperties
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
 
backend = FakeKyoto()
 
custom_gate = Gate("my_gate", 1, [])
qc = QuantumCircuit(1, 1)
qc.append(custom_gate, [0])
qc.measure(0, 0)
 
with builder.build() as custom_sched_q0:
    builder.play([0.1] * 160, DriveChannel(0))
 
backend.target.add_instruction(
    custom_gate,
    {(0,): InstructionProperties(calibration=custom_sched_q0)},
)
 
# Re-generate the passmanager with the new backend target
passmanager = generate_preset_pass_manager(optimization_level=1, backend=backend)
qc = passmanager.run(qc)


# Save the plot to a buffer
buffer = io.BytesIO()
qc.draw('mpl', idle_wires=False).savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()



result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))




