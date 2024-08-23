import io
import json
import sys
import base64
import pickle
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler import InstructionProperties
from qiskit.circuit.library import XGate, YGate

input = sys.argv[1]
parsed_input = json.loads(input)

file_path = 'target.pickle'

# Load the target from a file
with open(file_path, 'rb') as f:
    target = pickle.load(f)




 
X = XGate()
Y = YGate()
 
dd_sequence = [X, Y, X, Y]


 
y_gate_properties = {}
for qubit in range(target.num_qubits):
    y_gate_properties.update(
        {
            (qubit,): InstructionProperties(
                duration=target["x"][(qubit,)].duration,
                error=target["x"][(qubit,)].error,
            )
        }
    )
 
target.add_instruction(YGate(), y_gate_properties)


file_path='target_plus.pickle'
# Save the target to a file
with open(file_path, 'wb') as f:
    pickle.dump(target, f)


result = {
    "result_instructions": list(target.operation_names),
}

# Return the result as a JSON string
print(json.dumps(result))
