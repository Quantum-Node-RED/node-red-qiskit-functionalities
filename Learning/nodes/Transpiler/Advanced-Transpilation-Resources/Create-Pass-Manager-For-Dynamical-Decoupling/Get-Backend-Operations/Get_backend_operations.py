import io
import json
import sys
from qiskit_ibm_runtime import QiskitRuntimeService
import pickle

input = sys.argv[1]
parsed_input = json.loads(input)

token = parsed_input['token']
 
service = QiskitRuntimeService(channel="ibm_quantum", token=token)
backend = service.backend("ibm_brisbane")
 
target = backend.target
basis_gates = list(target.operation_names)

file_path = 'target.pickle'

# Save the target to a file
with open(file_path, 'wb') as f:
    pickle.dump(target, f)


result = {
    "result_operations": basis_gates
}

# Return the result as a JSON string
print(json.dumps(result))
