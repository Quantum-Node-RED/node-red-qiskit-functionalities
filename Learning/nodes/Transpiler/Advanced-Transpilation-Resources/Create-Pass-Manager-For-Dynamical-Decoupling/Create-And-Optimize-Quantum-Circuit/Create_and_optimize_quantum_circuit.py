import io
import json
import sys
import base64
import pickle
from qiskit_ibm_runtime import QiskitRuntimeService

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.circuit.library import EfficientSU2

input = sys.argv[1]
parsed_input = json.loads(input)

file_path = 'target.pickle'

# Load the target from a file
with open(file_path, 'rb') as f:
    target = pickle.load(f)

 
qc = EfficientSU2(12, entanglement="circular", reps=1)
pm = generate_preset_pass_manager(1, target=target, seed_transpiler=12345)
qc_t = pm.run(qc)

file_path = 'qc_t.pickle'

# Save the target to a file
with open(file_path, 'wb') as f:
    pickle.dump(qc_t, f)



# Save the plot to a buffer
buffer = io.BytesIO()
qc_t.draw("mpl", fold=-1, idle_wires=False).savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()


result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))
