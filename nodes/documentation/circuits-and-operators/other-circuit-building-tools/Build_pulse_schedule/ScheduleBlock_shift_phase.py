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
 
 

# Create the Gaussian pulse
with pulse.build(backend=backend) as pulse_prog_orig:
    pulse.play(gaus, channel)

 
with pulse.build(backend=backend) as pulse_prog_shift_freq:
    pulse.shift_phase(np.pi, channel)
    pulse.play(gaus, channel)


# Plot the two pulse programs for comparison
fig, axs = plt.subplots(1, 2, figsize=(10, 3))

# Use the draw method to plot the pulse programs
pulse_prog_orig.draw(axis=axs[0])
axs[0].set_title("Original Pulse Program", y=1.1)

pulse_prog_shift_freq.draw(axis=axs[1])
axs[1].set_title("Pulse Program with shifted Phase", y=1.1)

plt.tight_layout()





# Save the plot to a buffer
buffer = io.BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()



result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))




