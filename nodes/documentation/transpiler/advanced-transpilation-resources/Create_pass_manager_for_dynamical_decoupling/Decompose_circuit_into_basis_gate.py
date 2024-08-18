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
from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary as sel
from qiskit.transpiler.passes import BasisTranslator

input = sys.argv[1]
parsed_input = json.loads(input)

file_path = 'target.pickle'
with open(file_path, 'rb') as f:
    target = pickle.load(f)
basis_gates = list(target.operation_names)
os.remove(file_path)

file_path = 'qc_dd.pickle'
with open(file_path, 'rb') as f:
    qc_dd = pickle.load(f)
os.remove(file_path)

qc_dd = BasisTranslator(sel, basis_gates)(qc_dd)





# Save the plot to a buffer
buffer = io.BytesIO()
qc_dd.draw("mpl", fold=-1, idle_wires=False).savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()




result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))
