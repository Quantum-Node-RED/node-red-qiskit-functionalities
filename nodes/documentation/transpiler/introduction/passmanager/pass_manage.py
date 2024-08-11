from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.fake_provider import FakeWashingtonV2
from qiskit import QuantumRegister, QuantumCircuit
import base64
import json
import io
import sys
 
data = json.loads(sys.argv[1])
token = data["token"]
if token != "None":
    service = QiskitRuntimeService(channel="ibm_quantum", token=token)
    backend = service.backend("ibm_brisbane")
else:
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


result = {
    "transpiled_circuit_image": transpiled_circuit_image_b64
}

print(json.dumps(result))
