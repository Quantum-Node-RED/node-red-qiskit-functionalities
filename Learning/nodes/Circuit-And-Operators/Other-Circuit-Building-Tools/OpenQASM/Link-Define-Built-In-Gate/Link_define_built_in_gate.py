
import io
import base64
import json

from qiskit import qasm2
from qiskit.circuit.random import random_circuit
from qiskit.circuit import Instruction



from qiskit.circuit import Gate
from qiskit.circuit.library import RZXGate
 
# Define a custom gate that takes one qubit and two angles.
class MyGate(Gate):
    def __init__(self, theta, phi):
        super().__init__("my", 1, [theta, phi])
 
custom_instructions = [
    qasm2.CustomInstruction("my", 2, 1, MyGate, builtin=True),
]
 
program = """
    OPENQASM 2.0;
    qreg q[1];
 
    my(0.25, 0.125) q[0];
"""
 
circuit = qasm2.loads(
    program,
    custom_instructions=custom_instructions,
)



instructions_list = []

for instr, qargs, cargs in circuit.data:
    qubits = [qarg._index for qarg in qargs]
    clbits = [carg._index for carg in cargs]
    q_list = []
    c_list = []

    for q in qubits:
        q_list.append("q["+str(q)+"]")

    for c in clbits:
        c_list.append("c["+str(c)+"]")
    
    if clbits:
        instructions_list.append(f"{instr.name} {', '.join(q_list)} -> {', '.join(c_list)}")
    else:
        instructions_list.append(f"{instr.name} {', '.join(q_list)}")





# Save the plot to a buffer
buffer = io.BytesIO()
circuit.draw(output ='mpl').savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()



result = {
    "result_image": b64_str,
    "result_instructions": instructions_list
}

# Return the result as a JSON string
print(json.dumps(result))
