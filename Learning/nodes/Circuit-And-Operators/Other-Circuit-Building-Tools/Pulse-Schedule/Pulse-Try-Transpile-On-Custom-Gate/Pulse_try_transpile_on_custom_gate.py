from qiskit import QuantumCircuit
from qiskit.circuit import Gate
from qiskit import pulse
from qiskit.pulse.library import Gaussian
from qiskit_ibm_runtime.fake_provider import FakeValenciaV2
from qiskit_ibm_runtime.fake_provider import FakeHanoiV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit import QiskitError
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


custom_gate = Gate('my_custom_gate', 1, [3.14, 1])
# 3.14 is an arbitrary parameter for demonstration

circ = QuantumCircuit(2, 2)
circ.append(custom_gate, [1])


try:
    circ = passmanager.run(circ)
except QiskitError as e:
    error = str(e)




result = {
    "result_error": error
}

# Return the result as a JSON string
print(json.dumps(result))




