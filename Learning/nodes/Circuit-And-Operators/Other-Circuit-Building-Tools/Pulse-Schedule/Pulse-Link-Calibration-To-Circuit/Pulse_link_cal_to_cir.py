from qiskit import QuantumCircuit
from qiskit import pulse
from qiskit.pulse.library import Gaussian
from qiskit_ibm_runtime.fake_provider import FakeValenciaV2
from qiskit_ibm_runtime.fake_provider import FakeHanoiV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import json
import base64
import io

def instruction_to_sentence(instruction, qubits):
    name = instruction.name
    num_qubits = instruction.num_qubits
    num_clbits = instruction.num_clbits
    params = instruction.params
    
    qubit_str = ', '.join(map(str, qubits))
    
    sentence = (
        f"The instruction '{name}' is applied to {num_qubits} qubit(s) ({qubit_str}), "
        f"affecting {num_clbits} classical bit(s), with parameters {params}."
    )
    
    return sentence
 
circ = QuantumCircuit(2, 2)
circ.h(0)
circ.cx(0, 1)
circ.measure(0, 0)
circ.measure(1, 1)
 
backend = FakeValenciaV2()
 
with pulse.build(backend, name='hadamard') as h_q0:
    pulse.play(Gaussian(duration=128, amp=0.1, sigma=16), pulse.drive_channel(0))

circ.add_calibration('h', [0], h_q0)
 
backend = FakeHanoiV2()
passmanager = generate_preset_pass_manager(optimization_level=1, backend=backend)
circ = passmanager.run(circ)
instruction_results = []
 
# Print instructions that only affect qubits 0 and 1
for instruction, qubits in FakeHanoiV2().instructions:
    if qubits and set(qubits).issubset({0, 1}):
        instruction_results.append(instruction_to_sentence(instruction, qubits))

# for sent in instruction_results:
#     print(sent)

# Save the plot to a buffer
buffer = io.BytesIO()
circ.draw('mpl', idle_wires=False).savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()



result = {
    "result_image": b64_str,
    "result_instructions": instruction_results
}

# Return the result as a JSON string
print(json.dumps(result))




