import base64
import json
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.primitives import StatevectorSampler
import io
import numpy as np

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0,1)
qc.measure_all()

# Generate a pass manager without providing a backend
pm = generate_preset_pass_manager(optimization_level=1)
isa_circuit = pm.run(qc)

# Initilaize Estimator
sampler = StatevectorSampler()

# execute 1 circuit with Sampler V2
job = sampler.run([isa_circuit]) 
pub_result = job.result()[0]
# print(f" > Result class: {type(pub_result)}")

# create two circuits
circuit1 = qc.copy()
circuit2 = qc.copy()
 
# transpile circuits 
pm = generate_preset_pass_manager(optimization_level=1)
isa_circuit1 = pm.run(circuit1)
isa_circuit2 = pm.run(circuit2)
# execute 2 circuits using Sampler V2
job = sampler.run([(isa_circuit1), (isa_circuit2)])
pub_result_1 = job.result()[0]
pub_result_2 = job.result()[1]
# print(f" > Result class: {type(pub_result)}")

result = {
    "result_class_1_circuit": str(type(pub_result)),
    "result_class_2_circuit_p1": str(type(pub_result_1)),
    "result_class_2_circuit_p2": str(type(pub_result_2))
}

print(json.dumps(result))