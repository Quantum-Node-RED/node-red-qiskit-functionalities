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

file_path = 'backend_state.pkl'
with open(file_path, 'rb') as f:
    backend = pickle.load(f)

os.remove(file_path)

ghz = QuantumCircuit(15)
ghz.h(0)
ghz.cx(0, range(1, 15))
 
depths = []
gate_counts = []
multiqubit_gate_counts = []
# TODO: 自定义优化等级
levels = [str(x) for x in range(4)]
for level in range(4):
    pass_manager = generate_preset_pass_manager(
        optimization_level=level,
        backend=backend,
    )
    circ = pass_manager.run(ghz)
    depths.append(circ.depth())
    gate_counts.append(sum(circ.count_ops().values()))
    multiqubit_gate_counts.append(circ.count_ops()["cx"])
 
fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.bar(levels, depths, label="Depth")
ax1.set_xlabel("Optimization Level")
ax1.set_ylabel("Depth")
ax1.set_title("Output Circuit Depth")
ax2.bar(levels, gate_counts, label="Number of Circuit Operations")
ax2.bar(levels, multiqubit_gate_counts, label="Number of CX gates")
ax2.set_xlabel("Optimization Level")
ax2.set_ylabel("Number of gates")
ax2.legend()
ax2.set_title("Number of output circuit gates")
fig.tight_layout()

buffer = io.BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)
optimization_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()



current_directory = os.path.dirname(os.path.abspath(__file__))

# Read the image file
image_filename = "optimization.webp"

# Get the full path to the image file
image_path = os.path.join(current_directory, image_filename)

# Read the image file as a base64 string
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')



result = {
    "optimization_image": optimization_b64,
    "result_image": base64_image
}

print(json.dumps(result))