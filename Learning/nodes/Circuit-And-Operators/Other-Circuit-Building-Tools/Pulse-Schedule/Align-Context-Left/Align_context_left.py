from qiskit import pulse
from qiskit.pulse import library
from qiskit_ibm_runtime.fake_provider import FakeValenciaV2
 

import io
import base64
import json

backend = FakeValenciaV2()


with pulse.build(backend, name='Left align example') as program:
    with pulse.align_left():
        gaussian_pulse = library.Gaussian(100, 0.5, 20)
        pulse.play(gaussian_pulse, pulse.drive_channel(0))
        pulse.play(gaussian_pulse, pulse.drive_channel(1))
        pulse.play(gaussian_pulse, pulse.drive_channel(1))


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




