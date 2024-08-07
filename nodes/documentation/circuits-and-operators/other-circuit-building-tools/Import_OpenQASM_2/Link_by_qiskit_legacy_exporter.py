
import io
import base64
import json

from qiskit import qasm2
from qiskit.circuit.random import random_circuit
from qiskit.circuit import Instruction



 
program = """
    OPENQASM 2.0;
    include "qelib1.inc";
 
    qreg q[4];
    creg c[4];
 
    h q[0];
    cx q[0], q[1];
 
    // 'rxx' is not actually in `qelib1.inc`,
    // but Qiskit used to behave as if it were.
    rxx(0.75) q[2], q[3];
 
    measure q -> c;
"""
circuit = qasm2.loads(
    program,
    custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS,
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
