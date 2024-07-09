import io
import base64
from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator, Diagonal
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# load_dotenv()

# runtime_token = os.getenv("IBM_RUNTIME_CRED")

# QiskitRuntimeService.save_account(
#     channel="ibm_quantum",
#     token=runtime_token,
#     set_as_default=True,
#     # Use `overwrite=True` if you're updating your token.
#     overwrite=True,
# )

# service = QiskitRuntimeService() 
 
# Create circuit to test transpiler on
oracle = Diagonal([1] * 7 + [-1])
qc = QuantumCircuit(3)
qc.h([0, 1, 2])
qc = qc.compose(GroverOperator(oracle))
 
# Add measurements to the circuit
qc.measure_all()
 
# View the circuit
qc.draw(output='mpl')

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