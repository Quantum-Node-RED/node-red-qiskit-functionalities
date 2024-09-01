import base64
import json
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import io

# circuit for which you want to obtain the expected value
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0,1)
qc.measure_all()

# Draw the circuit
mpl_draw_str = qc.draw("mpl", style="iqp")
buffer = io.BytesIO()
mpl_draw_str.savefig(buffer, format='png') 
buffer.seek(0)
mpl_draw_str_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

result = {
    "circuit_image": mpl_draw_str_b64
}

print(json.dumps(result))