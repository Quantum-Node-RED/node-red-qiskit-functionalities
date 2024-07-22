import qiskit.qasm2
import io
import base64
import json
import os
from qiskit import QuantumCircuit

# 创建一个量子电路
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])


# Save the circuit to a QASM file
qasm_filename = "myfile.qasm"
qiskit.qasm2.dump(qc, qasm_filename)




# Load the QASM file
circuit = qiskit.qasm2.load(qasm_filename)

# Save the plot to a buffer
buffer = io.BytesIO()
circuit.draw(output ='mpl').savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()


# Delete the QASM file
os.remove(qasm_filename)


result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))
