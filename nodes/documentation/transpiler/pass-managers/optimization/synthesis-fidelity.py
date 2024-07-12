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
 
backend = FakeSherbrooke()

pass_manager = generate_preset_pass_manager(
    optimization_level=3, backend=backend, seed_transpiler=12345
)
qc_t3_exact = pass_manager.run(qc)

pass_manager = generate_preset_pass_manager(
    optimization_level=3,
    approximation_degree=0.99,
    backend=backend,
    seed_transpiler=12345,
)
qc_t3_approx = pass_manager.run(qc)

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
  "synthesis_fidelity_exact": round(exact_fid, 3),
  "synthesis_fidelity_approx": round(approx_fid, 3)
}

print(json.dumps(result))
