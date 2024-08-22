
import io
import base64
import json

from qiskit import qasm2
from qiskit.circuit.random import random_circuit
from qiskit.circuit import Instruction

import math
from qiskit.circuit import Gate
from qiskit.circuit.library import RZXGate




# Define a custom classical instruction that adds one to its argument.
program = '''
    include "qelib1.inc";
    qreg q[2];
    rx(arctan(pi, 3 + add_one(0.2))) q[0];
    cx q[0], q[1];
'''
 
def add_one(x):
    return x + 1
 
customs = [
    # Our `add_one` takes only one parameter.
    qasm2.CustomClassical("add_one", 1, add_one),
    # `arctan` takes two parameters, and `math.atan2` implements it.
    qasm2.CustomClassical("arctan", 2, math.atan2),
]
circuit = qasm2.loads(program, custom_classical=customs)




# Save the plot to a buffer
buffer = io.BytesIO()
circuit.draw(output ='mpl').savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()



result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))
