import base64
import json
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeAuckland, FakeWashingtonV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import io

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

result = {
    "layout_image": layout 
}

print(json.dumps(result))


