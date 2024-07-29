import base64
import json
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.primitives import StatevectorEstimator
import io
import numpy as np

# circuit for which you want to obtain the expected value
qc = QuantumCircuit(2)
qc.ry(Parameter('theta'), 0)
qc.h(0)
qc.cx(0,1)

# observable(s) whose expected values you want to compute
from qiskit.quantum_info import SparsePauliOp
observable = SparsePauliOp(["II", "XX", "YY", "ZZ"], coeffs=[1, 1, -1, 1])
 
# value(s) for the circuit parameter(s)
parameter_values = [[0], [np.pi/6], [np.pi/2]]

# Generate a pass manager without providing a backend
pm = generate_preset_pass_manager(optimization_level=1)
isa_circuit = pm.run(qc)
isa_observable = observable.apply_layout(isa_circuit.layout)

# Initilaize Estimator
estimator = StatevectorEstimator()

# Run and get results
job = estimator.run([(isa_circuit, isa_observable, parameter_values)])
result = job.result()

# Process result to make it JSON serializable and format to match precision of Qiskit code
expectation_values = [ev.tolist() if isinstance(ev, np.ndarray) else ev for ev in result[0].data.evs]
formatted_expectation_values = [round(ev, 8) for ev in expectation_values]

result = {
    "result_class": str(type(result)),
    "expectation_value": formatted_expectation_values,
    "metadata": result[0].metadata
}

print(json.dumps(result))