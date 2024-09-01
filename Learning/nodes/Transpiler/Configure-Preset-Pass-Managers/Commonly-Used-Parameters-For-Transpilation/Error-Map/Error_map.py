import io
import base64
import json
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from qiskit.visualization import plot_error_map

backend = FakeSherbrooke()

qc_buffer = io.BytesIO()
plot_error_map(backend, figsize=(30, 24)).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
error_map_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

result = {
  "error_map": error_map_str
}

print(json.dumps(result))
