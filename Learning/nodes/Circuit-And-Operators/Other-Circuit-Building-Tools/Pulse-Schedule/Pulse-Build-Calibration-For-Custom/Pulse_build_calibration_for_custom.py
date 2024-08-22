from qiskit import QuantumCircuit
import io
import base64
import json

from qiskit import pulse
from qiskit.pulse.library import Gaussian
from qiskit_ibm_runtime.fake_provider import FakeValenciaV2
 
backend = FakeValenciaV2()

with pulse.build(backend, name='custom') as my_schedule:
    pulse.play(Gaussian(duration=64, amp=0.2, sigma=8), pulse.drive_channel(0))

# Save the plot to a buffer
buffer = io.BytesIO()
my_schedule.draw().savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()



result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))




