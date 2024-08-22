from qiskit import pulse
from qiskit.pulse import library
from qiskit_ibm_runtime.fake_provider import FakeValenciaV2
 

import io
import base64
import json

backend = FakeValenciaV2()


with pulse.build(backend, name='Offset example') as program:
    gaussian_pulse = library.Gaussian(100, 0.5, 20)
    with pulse.phase_offset(3.14, pulse.drive_channel(0)):
        pulse.play(gaussian_pulse, pulse.drive_channel(0))
        with pulse.frequency_offset(10e6, pulse.drive_channel(0)):
            pulse.play(gaussian_pulse, pulse.drive_channel(0))
 

# Save the plot to a buffer
buffer = io.BytesIO()
program.draw().savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()



result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))




