import io
import json
from qiskit import QuantumCircuit
import base64
import matplotlib.pyplot as plt
import base64
import io



# Quantum Circuit Begin test
test = QuantumCircuit(2)
test.cx(1, 0)
test.h(0)
test.cz(0, 1)
test.rx(0.5, 1)
# Quantum Circuit End
buffer = io.BytesIO()
test.draw(output='mpl').savefig(buffer, format='png')
buffer.seek(0)
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()
print(json.dumps(b64_str))
