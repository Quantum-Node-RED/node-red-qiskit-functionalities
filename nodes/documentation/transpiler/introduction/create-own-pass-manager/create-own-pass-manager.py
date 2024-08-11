from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.fake_provider import FakeWashingtonV2
from qiskit import QuantumRegister, QuantumCircuit
import base64
import json
import io
import sys
 
# data = json.loads(sys.argv[1])

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



result = {
    "own_pass_manager_example_image": own_pass_manager_example_image_b64,
    "translated_image": translated_image_b64
}

print(json.dumps(result))
