import base64
import json
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit import QuantumRegister, ClassicalRegister
from qiskit_ibm_runtime.fake_provider import FakeAuckland, FakeWashingtonV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import io
from qiskit.visualization import plot_circuit_layout
from qiskit_aer import Aer
import pickle
import os

# Build a quantum circuit
circuit = QuantumCircuit(3, 3)
circuit.x(1)
circuit.h(range(3))
circuit.cx(0, 1)
circuit.measure(range(3), range(3));

# Draw the circuit
default_draw = circuit.draw()
default_draw_str = str(default_draw)

result = {
    "default_draw_text": default_draw_str
}

print(json.dumps(result))
