from qiskit import pulse
from qiskit.pulse import library
 
amp = 1
sigma = 10
num_samples = 128
 
import io
import base64
import json

import numpy as np
 
times = np.arange(num_samples)
gaussian_samples = np.exp(-1/2 *((times - num_samples / 2) ** 2 / sigma**2))
 
gaus = library.Waveform(gaussian_samples, name="WF Gaus")



# Save the plot to a buffer
buffer = io.BytesIO()
gaus.draw().savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()



result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))




