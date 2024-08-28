import base64
import json
from math import pi
from qiskit_aer.primitives import Sampler
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import io

# quantum circuit to make a Bell state
bell = QuantumCircuit(2)
bell.h(0)
bell.cx(0, 1)
bell.measure_all()
 
# execute the quantum circuits
quasi_dists = Sampler().run(bell, shots=1000).result().quasi_dists[0]
second_quasi_dists = Sampler().run(bell, shots=1000).result().quasi_dists[0]


# Plot results with custom options
draw_str = plot_histogram(
    [quasi_dists, second_quasi_dists],
    legend=["first", "second"],
    sort="desc",
    figsize=(15, 12),
    color=["orange", "black"],
    bar_labels=False,
)
buffer = io.BytesIO()
draw_str.savefig(buffer, format='png') 
buffer.seek(0)
draw_str_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

result = {
    "options_histogram": draw_str_b64
}

print(json.dumps(result))
