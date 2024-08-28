import io
import base64
import json
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from qiskit.circuit.library import EfficientSU2
 
# Default configuration
backend = FakeSherbrooke()
target = backend.target
 
qc = EfficientSU2(12, entanglement="circular", reps=1)

# View the circuit
qc_buffer = io.BytesIO()
qc.decompose().draw("mpl").savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

result = {
  "circuit_diagram": qc_str
}

print(json.dumps(result))

