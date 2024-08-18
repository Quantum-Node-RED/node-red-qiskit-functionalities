import base64
import json
from qiskit import QuantumCircuit
import io

# Build a quantum circuit
circuit = QuantumCircuit(3, 3)
circuit.x(1)
circuit.h(range(3))
circuit.cx(0, 1)
circuit.measure(range(3), range(3));

# Draw the circuit
mpl_draw_str = circuit.draw('mpl')
buffer = io.BytesIO()
mpl_draw_str.savefig(buffer, format='png') 
buffer.seek(0)
mpl_draw_str_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

result = {
    "circuit_diagram": mpl_draw_str_b64
}

print(json.dumps(result))
