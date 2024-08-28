import io
import base64
import json
from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator, Diagonal
 
# Create circuit to test transpiler on
oracle = Diagonal([1] * 7 + [-1])
qc = QuantumCircuit(3)
qc.h([0, 1, 2])
qc = qc.compose(GroverOperator(oracle))
 
# Add measurements to the circuit
qc.measure_all()
 
# View the circuit
qc_buffer = io.BytesIO()
qc.draw(output='mpl').savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

result = {
  "circuit_diagram": qc_str
}

print(json.dumps(result))
