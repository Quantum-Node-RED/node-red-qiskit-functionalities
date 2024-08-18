import base64
import json
from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer
import io

circuit = QuantumCircuit(1)
for _ in range(10):
    circuit.h(0)

# Draw the circuit
style_draw_str = circuit_drawer(circuit, output="mpl", plot_barriers=False)
buffer = io.BytesIO()
style_draw_str.savefig(buffer, format='png') 
buffer.seek(0)
style_draw_str_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

result = {
    "circuit_diagram": style_draw_str_b64
}

print(json.dumps(result))
