import sys
import json
from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import Aer
from qiskit_algorithms import AmplificationProblem
from qiskit_algorithms import Grover

# msg.payload from node-red
data = json.loads(sys.argv[1])

target_state = data.get('target_state', '11')  

oracle = QuantumCircuit(2)
if target_state == '11':
    oracle.cz(0, 1)
elif target_state == '10':
    oracle.x(1)
    oracle.cz(0, 1)
    oracle.x(1)
elif target_state == '01':
    oracle.x(0)
    oracle.cz(0, 1)
    oracle.x(0)
elif target_state == '00':
    oracle.x([0, 1])
    oracle.cz(0, 1)
    oracle.x([0, 1])
else:
    raise ValueError("Invalid target state")

grover_circuit = QuantumCircuit(2)
grover_circuit.h([0, 1])
grover_circuit.append(oracle, [0, 1])
grover_circuit.h([0, 1])

problem = AmplificationProblem(grover_circuit, is_good_state=lambda bitstring: bitstring == '11')

grover = Grover()
result = grover.amplify(problem)

backend = Aer.get_backend('qasm_simulator')
qc = result.circuit
qc.measure_all()

tqc = transpile(qc, backend)
qobj = assemble(tqc)
result = backend.run(qobj).result()
counts = result.get_counts()

print(json.dumps(counts))