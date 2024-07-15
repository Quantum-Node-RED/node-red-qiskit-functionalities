from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.fake_provider import FakeAuckland, FakeWashingtonV2
from qiskit import QuantumRegister, QuantumCircuit
import base64
import json
import matplotlib.pyplot as plt
import io
 
# TODO enable user to use their token  
# service = QiskitRuntimeService(channel="ibm_quantum", token="YOUR API TOKEN")
# backend = service.backend("ibm_brisbane")

# Use fake pulse-enabled backend
backend = FakeWashingtonV2()
 
# Run with optimization level 3 and 'asap' scheduling pass
pass_manager = generate_preset_pass_manager(
    optimization_level=3,
    backend=backend,
)
pass_manager = generate_preset_pass_manager(optimization_level=3, backend=backend)
 
# Create a circuit
qubits = QuantumRegister(2, name="q")
circuit = QuantumCircuit(qubits)
a, b = qubits
circuit.h(a)
circuit.cx(a, b)
circuit.cx(b, a)
 
# Transpile it by calling the run method of the pass manager
transpiled = pass_manager.run(circuit)
 
# Draw it, excluding idle qubits from the diagram
transpiled_circuit_image = transpiled.draw("mpl", idle_wires=False)
buffer = io.BytesIO()
transpiled_circuit_image.savefig(buffer, format='png')
buffer.seek(0)
transpiled_circuit_image_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

# create own pass manager
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import (
    Collect2qBlocks,
    ConsolidateBlocks,
    UnitarySynthesis,
)
 
basis_gates = ["rx", "ry", "rxx"]
translate = PassManager(
    [
        Collect2qBlocks(),
        ConsolidateBlocks(basis_gates=basis_gates),
        UnitarySynthesis(basis_gates),
    ]
)
qubits = QuantumRegister(2, name="q")
circuit = QuantumCircuit(qubits)
 
a, b = qubits
circuit.h(a)
circuit.cx(a, b)
circuit.cx(b, a)
 
own_pass_manager_example_image =  circuit.draw("mpl")
buffer = io.BytesIO()
own_pass_manager_example_image.savefig(buffer, format='png')
buffer.seek(0)
own_pass_manager_example_image_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

translated = translate.run(circuit)
translated_image = translated.draw("mpl")
buffer = io.BytesIO()
translated_image.savefig(buffer, format='png')
buffer.seek(0)
translated_image_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

# create a staged pass manager
from qiskit.transpiler import PassManager, StagedPassManager
from qiskit.transpiler.passes import UnitarySynthesis, Unroll3qOrMore
 
basis_gates = ["rx", "ry", "rxx"]
init = PassManager([UnitarySynthesis(basis_gates, min_qubits=3), Unroll3qOrMore()])
staged_pm = StagedPassManager(
    stages=["init", "translation"], init=init, translation=translate
)
import numpy as np
from qiskit.circuit.library import HGate, PhaseGate, RXGate, TdgGate, TGate
from qiskit.transpiler.passes import CXCancellation, InverseCancellation
 
pass_manager = generate_preset_pass_manager(3, backend)
inverse_gate_list = [
    HGate(),
    (RXGate(np.pi / 4), RXGate(-np.pi / 4)),
    (PhaseGate(np.pi / 4), PhaseGate(-np.pi / 4)),
    (TGate(), TdgGate()),
]
logical_opt = PassManager(
    [
        CXCancellation(),
        InverseCancellation(inverse_gate_list),
    ]
)
 
# Add pre-layout stage to run extra logical optimization
pass_manager.pre_layout = logical_opt

result = {
    "transpiled_circuit_image": transpiled_circuit_image_b64,
    "own_pass_manager_example_image": own_pass_manager_example_image_b64,
    "translated_image": translated_image_b64
}

print(json.dumps(result))
