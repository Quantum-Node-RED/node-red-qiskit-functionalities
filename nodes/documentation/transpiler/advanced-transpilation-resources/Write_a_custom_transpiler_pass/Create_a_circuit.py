import io
import json
import sys
import base64
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

qr = QuantumRegister(3, 'qr')
cr = ClassicalRegister(3, 'cr')
qc = QuantumCircuit(qr, cr)

qc.h(qr[0])
qc.cx(qr[0], qr[1])
qc.measure(qr[0], cr[0])
qc.rz(np.pi/2, qr[1]).c_if(cr, 2)


# Save the plot to a buffer
buffer = io.BytesIO()
qc.draw(output = "mpl").savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

 




result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))
