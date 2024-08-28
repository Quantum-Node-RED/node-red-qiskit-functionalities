import base64
import json
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeAuckland, FakeWashingtonV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import io
from qiskit.visualization import plot_circuit_layout
from qiskit_aer import Aer
import pickle
import os

# take a 15-qubit GHZ circuit executed 100 times, using a “bad” (disconnected) initial_layout. 
backend = FakeAuckland()
 
ghz = QuantumCircuit(15)
ghz.h(0)
ghz.cx(0, range(1, 15))
 
pass_manager = generate_preset_pass_manager(
    optimization_level=1,
    backend=backend,
    layout_method="trivial",  # Fixed layout mapped in circuit order
)

# draw the image of circuit depth and gate count
depths = []
for _ in range(100):
    depths.append(pass_manager.run(ghz).depth())
 
plt.figure(figsize=(8, 6))
plt.hist(depths, align="left", color="#AC557C")
plt.xlabel("Depth", fontsize=14)
plt.ylabel("Counts", fontsize=14)

buffer = io.BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)
layout = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

circuit_image = ghz.draw('mpl', idle_wires=False)
buffer = io.BytesIO()
circuit_image.savefig(buffer, format='png') 
buffer.seek(0)
circuit_image_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

# Plot the hardware graph and indicate which hardware qubits were chosen to run the circuit
transpiled_circ = pass_manager.run(ghz)

current_directory = os.path.dirname(os.path.abspath(__file__))

# Read the image file
image_filename = "routing.png"

# Get the full path to the image file
image_path = os.path.join(current_directory, image_filename)

# Read the image file as a base64 string
with open(image_path, "rb") as image_file:
   qubits_used_image_b64 = base64.b64encode(image_file.read()).decode('utf-8')

# https://graphviz.org/download/ to download the graphvizs
# qubits_used_image = plot_circuit_layout(transpiled_circ, backend)
# buffer = io.BytesIO()
# qubits_used_image.savefig(buffer, format='png') 
# buffer.seek(0)
# qubits_used_image_b64 = base64.b64encode(buffer.read()).decode('utf-8')
# buffer.close()

result = {
    "layout_image": layout,
    "circuit_image": circuit_image_b64,
    "qubit_image":  qubits_used_image_b64 
}

with open('backend_state.pkl', 'wb') as f:
    pickle.dump(backend, f)

print(json.dumps(result))


