import io
import json
import sys
import base64
import pickle
import os
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler import InstructionProperties
from qiskit.circuit.library import XGate, YGate
import numpy as np
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes.scheduling import (
    ALAPScheduleAnalysis,
    PadDynamicalDecoupling,
)
from qiskit.visualization import timeline_drawer

input = sys.argv[1]
parsed_input = json.loads(input)

file_path = 'target_plus.pickle'

# Load the target from a file
with open(file_path, 'rb') as f:
    target = pickle.load(f)
os.remove(file_path)


file_path = 'qc_t.pickle'

# Load the qc_t from a file
with open(file_path, 'rb') as f:
    qc_t = pickle.load(f)
os.remove(file_path)
 


X = XGate()
Y = YGate()
 
dd_sequence = [X, Y, X, Y]
 
rng = np.random.default_rng(1234)
qc_t.assign_parameters(rng.uniform(-np.pi, np.pi, qc_t.num_parameters), inplace=True)

dd_pm = PassManager(
    [
        ALAPScheduleAnalysis(target=target),
        PadDynamicalDecoupling(target=target, dd_sequence=dd_sequence),
    ]
)
qc_dd = dd_pm.run(qc_t)




# Save the plot to a buffer
buffer = io.BytesIO()
timeline_drawer(qc_dd, show_idle=False).savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()




file_path = 'qc_dd.pickle'

# Save the target to a file
with open(file_path, 'wb') as f:
    pickle.dump(qc_dd, f)


result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))
