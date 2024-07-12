import io
import base64
import json
from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator, Diagonal
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
 
# Create circuit to test transpiler on
oracle = Diagonal([1] * 7 + [-1])
qc = QuantumCircuit(3)
qc.h([0, 1, 2])
qc = qc.compose(GroverOperator(oracle))
 
# Add measurements to the circuit
qc.measure_all()

# Specify the system to target
backend = FakeSherbrooke()
 
# Transpile the circuit
pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
transpiled_circ = pass_manager.run(qc)
 
# View the transpiled circuit
transpiled_circ_buffer = io.BytesIO()
transpiled_circ.draw(output='mpl', idle_wires=False).savefig(transpiled_circ_buffer, format='png')
transpiled_circ_buffer.seek(0)
transpiled_circ_str = base64.b64encode(transpiled_circ_buffer.read()).decode('utf-8')
transpiled_circ_buffer.close()

result = {
  "transpiled_circ_image": transpiled_circ_str,
}

print(json.dumps(result))
