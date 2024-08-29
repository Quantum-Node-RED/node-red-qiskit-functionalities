import base64
import json
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.primitives import StatevectorSampler
import io
import numpy as np

circuit = QuantumCircuit(2)
circuit.h(0)
circuit.cx(0,1)
circuit.measure_all()

# Draw the circuit
default_draw = circuit.draw()
default_draw_str = str(default_draw)

sampler = StatevectorSampler()

# Transpile circuit
pm = generate_preset_pass_manager(optimization_level=1)
isa_circuit = pm.run(circuit)
# Run using V2 sampler
result = sampler.run([circuit]).result()
# Access result data for PUB 0
data_pub = result[0].data
# Access bitstring for the classical register "meas"
bitstrings = data_pub.meas.get_bitstrings()
# print(f"The number of bitstrings is: {len(bitstrings)}")
# Get counts for the classical register "meas"
counts = data_pub.meas.get_counts()
# print(f"The counts are: {counts}")

result = {
    "circuit_text": default_draw_str,
    "the_number_of_bitstrings_is": str(len(bitstrings)),
    "the_counts_are": str(counts)
}

print(json.dumps(result))