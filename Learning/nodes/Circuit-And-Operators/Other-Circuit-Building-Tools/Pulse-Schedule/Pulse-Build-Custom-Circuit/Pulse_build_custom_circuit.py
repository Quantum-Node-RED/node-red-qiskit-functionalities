from qiskit import QuantumCircuit
from qiskit.circuit import Gate
import io
import base64
import json
 
circ = QuantumCircuit(1, 1)
custom_gate = Gate('my_custom_gate', 1, [3.14, 1])
# 3.14 is an arbitrary parameter for demonstration
circ.append(custom_gate, [0])
circ.measure(0, 0)


# Save the plot to a buffer
buffer = io.BytesIO()
circ.draw('mpl').savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()



result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))




