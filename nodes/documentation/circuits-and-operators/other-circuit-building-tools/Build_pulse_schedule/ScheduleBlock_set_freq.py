from qiskit import pulse
from qiskit.pulse import library
import io
import base64
import json
import numpy as np
import matplotlib.pyplot as plt
from qiskit.pulse import DriveChannel
from qiskit_ibm_runtime.fake_provider import FakeValenciaV2
 
channel = DriveChannel(0)
backend = FakeValenciaV2()

amp = 1
sigma = 10
num_samples = 128
gaus = pulse.library.Gaussian(num_samples, amp, sigma,
                              name="Parametric Gaus")
 
 
# Create the Gaussian pulse with frequency 4.5e9
with pulse.build(backend=backend) as pulse_prog_set_freq:
    pulse.set_frequency(4.5e9, channel)
    pulse.play(gaus, channel)





# Save the plot to a buffer
buffer = io.BytesIO()
pulse_prog_set_freq.draw().savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()



result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))




