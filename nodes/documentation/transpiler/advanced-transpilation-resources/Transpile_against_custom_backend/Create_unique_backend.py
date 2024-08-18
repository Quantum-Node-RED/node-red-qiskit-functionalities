import io
import json
import sys
import os
import base64
import numpy as np
import rustworkx as rx
 
from qiskit.providers import BackendV2, Options
from qiskit.transpiler import Target, InstructionProperties
from qiskit.circuit.library import XGate, SXGate, RZGate, CZGate, ECRGate
from qiskit.circuit import Measure, Delay, Parameter, IfElseOp, Reset
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_gate_map, plot_coupling_map
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit import QuantumCircuit
 
 
 
class FakeTorusBackend(BackendV2):
    """Fake multi chip backend."""
 
    def __init__(self):
        """Instantiate a new backend that is inspired by a toric code"""
        super().__init__(name='Fake LOCC backend')
        graph = rx.generators.directed_grid_graph(20, 20)
        for column in range(20):
            graph.add_edge(column, 19*20 + column, None)
        for row in range(20):
            graph.add_edge(row * 20, row * 20 + 19, None)
        num_qubits = len(graph)
        rng = np.random.default_rng(seed=12345678942)
        rz_props = {}
        x_props = {}
        sx_props = {}
        measure_props = {}
        delay_props = {}
        self._target = Target("Fake Kookaburra", num_qubits=num_qubits)
        # Add 1q gates. Globally use virtual rz, x, sx, and measure
        for i in range(num_qubits):
            qarg = (i,)
            rz_props[qarg] = InstructionProperties(error=0.0, duration=0.0)
            x_props[qarg] = InstructionProperties(
                error=rng.uniform(1e-6, 1e-4), duration=rng.uniform(1e-8, 9e-7)
            )
            sx_props[qarg] = InstructionProperties(
                error=rng.uniform(1e-6, 1e-4), duration=rng.uniform(1e-8, 9e-7)
            )
            measure_props[qarg] = InstructionProperties(
                error=rng.uniform(1e-3, 1e-1), duration=rng.uniform(1e-8, 9e-7)
            )
            delay_props[qarg] = None
        self._target.add_instruction(XGate(), x_props)
        self._target.add_instruction(SXGate(), sx_props)
        self._target.add_instruction(RZGate(Parameter("theta")), rz_props)
        self._target.add_instruction(Measure(), measure_props)
        self._target.add_instruction(Reset(), measure_props)
        self._target.add_instruction(Delay(Parameter("t")), delay_props)
        cz_props = {}
        for edge in graph.edge_list():
            offset = i * len(graph)
            cz_props[edge] = InstructionProperties(
                error=rng.uniform(7e-4, 5e-3), duration=rng.uniform(1e-8, 9e-7)
            )
        self._target.add_instruction(CZGate(), cz_props)
 
    @property
    def target(self):
        return self._target
 
    @property
    def max_circuits(self):
        return None
 
    @classmethod
    def _default_options(cls):
        return Options(shots=1024)
 
    def run(self, circuit, **kwargs):
        raise NotImplementedError("Lasciate ogne speranza, voi ch'intrate")
    

backend = FakeTorusBackend()

 
num_qubits = int(backend.num_qubits / 2)
full_device_bv = QuantumCircuit(num_qubits, num_qubits - 1)
full_device_bv.x(num_qubits - 1)
full_device_bv.h(range(num_qubits))
full_device_bv.cx(range(num_qubits - 1), num_qubits - 1)
full_device_bv.h(range(num_qubits))
full_device_bv.measure(range(num_qubits - 1), range(num_qubits - 1))
tqc = transpile(full_device_bv, backend, optimization_level=3)
op_counts = tqc.count_ops()
 


current_directory = os.path.dirname(os.path.abspath(__file__))

# Read the image file
image_filename = "Create_unique_backend.png"

# Get the full path to the image file
image_path = os.path.join(current_directory, image_filename)

# Read the image file as a base64 string
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
 

# print(f"CZ gates: {op_counts['cz']}")
# print(f"X gates: {op_counts['x']}")
# print(f"SX gates: {op_counts['sx']}")
# print(f"RZ gates: {op_counts['rz']}")


result = {
    "Post-Transpilation": {
        "CZ gates": op_counts['cz'],
        "X gates": op_counts['x'],
        "SX gates": op_counts['sx'],
        "RZ gates": op_counts['rz']
    },
    "result_image": base64_image
}

# Return the result as a JSON string
print(json.dumps(result))
