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
 
 
 
class FakeLOCCBackend(BackendV2):
    """Fake multi chip backend."""
 
    def __init__(self, distance=3, number_of_chips=3):
        """Instantiate a new fake multi chip backend.
 
        Args:
            distance (int): The heavy hex code distance to use for each chips'
                coupling map. This number **must** be odd. The distance relates
                to the number of qubits by:
                :math:`n = \\frac{5d^2 - 2d - 1}{2}` where :math:`n` is the
                number of qubits and :math:`d` is the ``distance``
            number_of_chips (int): The number of chips to have in the multichip backend
                each chip will be a heavy hex graph of ``distance`` code distance.
        """
        super().__init__(name='Fake LOCC backend')
        # Create a heavy-hex graph using the rustworkx library, then instantiate a new target
        self._graph = rx.generators.directed_heavy_hex_graph(distance, bidirectional=False)
        num_qubits = len(self._graph) * number_of_chips
        self._target = Target("Fake multi-chip backend", num_qubits=num_qubits)
 
        # Generate instruction properties for single qubit gates and a measurement, delay,
        #  and reset operation to every qubit in the backend.
        rng = np.random.default_rng(seed=12345678942)
        rz_props = {}
        x_props = {}
        sx_props = {}
        measure_props = {}
        delay_props = {}
 
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
        # Add chip local 2q gate which is CZ
        cz_props = {}
        for i in range(number_of_chips):
            for root_edge in self._graph.edge_list():
                offset = i * len(self._graph)
                edge = (root_edge[0] + offset, root_edge[1] + offset)
                cz_props[edge] = InstructionProperties(
                    error=rng.uniform(7e-4, 5e-3), duration=rng.uniform(1e-8, 9e-7)
                )
        self._target.add_instruction(CZGate(), cz_props)
 
        cx_props = {}
        # Add interchip 2q gates which are ecr (effectively CX)
        # First determine which nodes to connect
        node_indices = self._graph.node_indices()
        edge_list = self._graph.edge_list()
        inter_chip_nodes = {}
        for node in node_indices:
            count = 0
            for edge in edge_list:
                if node == edge[0]:
                    count+=1
            if count == 1:
                inter_chip_nodes[node] = count
        # Create inter-chip ecr props
        cx_props = {}
        inter_chip_edges = list(inter_chip_nodes.keys())
        for i in range(1, number_of_chips):
            offset = i * len(self._graph)
            edge = (inter_chip_edges[1] + (len(self._graph) * (i-1)) , inter_chip_edges[0] + offset)
            cx_props[edge] = InstructionProperties(
                error=rng.uniform(7e-4, 5e-3), duration=rng.uniform(1e-8, 9e-7)
            )
 
        self._target.add_instruction(ECRGate(), cx_props)
 
    @property
    def target(self):
        return self._target
 
    @property
    def max_circuits(self):
        return None
 
    @property
    def graph(self):
        return self._graph
 
 
    @classmethod
    def _default_options(cls):
        return Options(shots=1024)
 
    def run(self, circuit, **kwargs):
        raise NotImplementedError("This backend does not contain a run method")
    

backend = FakeLOCCBackend(3, 3)

 
num_qubits = 50
ghz = QuantumCircuit(num_qubits)
ghz.h(range(num_qubits))
ghz.cx(0, range(1, num_qubits))
op_counts = ghz.count_ops()

pm = generate_preset_pass_manager(optimization_level=3, backend=backend)
transpiled_ghz = pm.run(ghz)
op_counts = transpiled_ghz.count_ops()
 
# print("Post-Transpilation: ")
# print(f"CZ gates: {op_counts['cz']}")
# print(f"ECR gates: {op_counts['ecr']}")
# print(f"SX gates: {op_counts['sx']}")
# print(f"RZ gates: {op_counts['rz']}")


current_directory = os.path.dirname(os.path.abspath(__file__))

# Read the image file
image_filename = "Run_circuit_on_custom_backend.png"

# Get the full path to the image file
image_path = os.path.join(current_directory, image_filename)

# Read the image file as a base64 string
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
 



result = {
    "Post-Transpilation": {
        "CZ gates": op_counts["cz"],
        "ECR gates": op_counts["ecr"],
        "SX gates": op_counts["sx"],
        "RZ gates": op_counts["rz"]
    },
    "result_image": base64_image
}

# Return the result as a JSON string
print(json.dumps(result))
