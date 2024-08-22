import qiskit.qasm2
import io
import base64
import json
import os

from qiskit import QuantumCircuit, qasm2
 
# Define any circuit.
circuit = QuantumCircuit(2, 2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0, 1], [0, 1])
 
# Export to a string.
program = qasm2.dumps(circuit)
file_name = "my_file.qasm"
 
# Export to a file.
qasm2.dump(circuit, file_name)


# Get the absolute path of the file
absolute_path = os.path.abspath(file_name)



result = {
    "result_path": absolute_path
}

# Return the result as a JSON string
print(json.dumps(result))
