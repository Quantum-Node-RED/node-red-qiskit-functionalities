from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from qiskit import pulse
from qiskit.pulse.library import Gaussian
from qiskit_ibm_runtime.fake_provider import FakeValenciaV2
from qiskit_ibm_runtime.fake_provider import FakeHanoiV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import json
import base64
import io

# def instruction_to_sentence(instruction, qubits):
#     name = instruction.name
#     num_qubits = instruction.num_qubits
#     num_clbits = instruction.num_clbits
#     params = instruction.params
    
#     qubit_str = ', '.join(map(str, qubits))
    
#     sentence = (
#         f"The instruction '{name}' is applied to {num_qubits} qubit(s) ({qubit_str}), "
#         f"affecting {num_clbits} classical bit(s), with parameters {params}."
#     )
    
#     return sentence
 
 
backend = FakeValenciaV2()
passmanager = generate_preset_pass_manager(optimization_level=1, backend=backend)


circ = QuantumCircuit(1, 1)
custom_gate = Gate('my_custom_gate', 1, [3.14, 1])
# 3.14 is an arbitrary parameter for demonstration
circ.append(custom_gate, [0])
circ.measure(0, 0)


with pulse.build(backend, name='custom') as my_schedule:
    pulse.play(Gaussian(duration=64, amp=0.2, sigma=8), pulse.drive_channel(0))

 
circ.add_calibration('my_custom_gate', [0], my_schedule, [3.14, 1])
# Alternatively: circ.add_calibration(custom_gate, [0], my_schedule)

circ = passmanager.run(circ)


# Save the plot to a buffer
buffer = io.BytesIO()
circ.draw('mpl', idle_wires=False).savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()



result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))




