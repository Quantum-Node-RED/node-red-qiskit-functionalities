import io
import base64
import json
import os

 
from qiskit import QuantumCircuit
from qiskit.qasm3 import dump, dumps
 
# Create a simple circuit and convert it to a string
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0,1)
qc.measure_all()
 
string = dumps(qc)


# Create a simple circuit and write it to a file
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0,1)
qc.measure_all()
 
f = open("my_file.txt", 'w')
dump(qc, f)
# Get the absolute path of the file
absolute_path = os.path.abspath("my_file.txt")
f.close()


# # Save the plot to a buffer
# buffer = io.BytesIO()
# circuit.draw(output ='mpl').savefig(buffer, format='png')
# buffer.seek(0)

# # Convert the plot to a Base64 string
# b64_str = base64.b64encode(buffer.read()).decode('utf-8')
# buffer.close()



result = {
    "result_string": string,
    "result_file": absolute_path
}

# Return the result as a JSON string
print(json.dumps(result))
