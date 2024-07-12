import io
import base64
import json
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Operator, random_unitary
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from qiskit.synthesis.two_qubit.two_qubit_decompose import trace_to_fid
 
 
UU = random_unitary(4, seed=12345)
rand_U = UnitaryGate(UU)

qc = QuantumCircuit(2)
qc.append(rand_U, range(2))
qc.swap(0, 1)

# View the circuit
qc_buffer = io.BytesIO()
qc.draw("mpl", style="iqp").savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()
 
backend = FakeSherbrooke()
 
# pass_manager = generate_preset_pass_manager(
#     optimization_level=0, backend=backend, seed_transpiler=12345
# )
# qc_t0_exact = pass_manager.run(qc)
# qc_t0_exact.draw("mpl", idle_wires=False)

# pass_manager = generate_preset_pass_manager(
#     optimization_level=1, backend=backend, seed_transpiler=12345
# )
# qc_t1_exact = pass_manager.run(qc)
# qc_t1_exact.draw("mpl", idle_wires=False)

# pass_manager = generate_preset_pass_manager(
#     optimization_level=2, backend=backend, seed_transpiler=12345
# )
# qc_t2_exact = pass_manager.run(qc)
# qc_t2_exact.draw("mpl", idle_wires=False)

pass_manager = generate_preset_pass_manager(
    optimization_level=3, backend=backend, seed_transpiler=12345
)
qc_t3_exact = pass_manager.run(qc)

# View the circuit
qc_buffer = io.BytesIO()
qc_t3_exact.draw("mpl", idle_wires=False).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t3_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()


pass_manager = generate_preset_pass_manager(
    optimization_level=3,
    approximation_degree=0.99,
    backend=backend,
    seed_transpiler=12345,
)
qc_t3_approx = pass_manager.run(qc)

# View the circuit
qc_buffer = io.BytesIO()
qc_t3_approx.draw("mpl", idle_wires=False).savefig(qc_buffer, format='png')
qc_buffer.seek(0)
qc_t3_approx_str = base64.b64encode(qc_buffer.read()).decode('utf-8')
qc_buffer.close()

# Reduce circuits down to 2 qubits so they are easy to simulate
qc_t3_exact_small = QuantumCircuit.from_instructions(qc_t3_exact)
qc_t3_approx_small = QuantumCircuit.from_instructions(qc_t3_approx)
 
# Compute the fidelity
exact_fid = trace_to_fid(
    np.trace(np.dot(Operator(qc_t3_exact_small).adjoint().data, UU))
)
approx_fid = trace_to_fid(
    np.trace(np.dot(Operator(qc_t3_approx_small).adjoint().data, UU))
)

result = {
  "qc_image": qc_str, 
  "qc_t3_image": qc_t3_str,
  "qc_t3_approx_image": qc_t3_approx_str,
  "synthesis_fidelity_exact": round(exact_fid, 3),
  "synthesis_fidelity_approx": round(approx_fid, 3)
}

print(json.dumps(result))
