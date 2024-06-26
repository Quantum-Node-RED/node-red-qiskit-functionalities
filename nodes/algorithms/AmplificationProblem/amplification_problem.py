import sys
import json
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit_aer.primitives import Sampler
from qiskit_algorithms import AmplificationProblem
from qiskit_algorithms import Grover

# msg.payload from node-red
data = json.loads(sys.argv[1])
target = data["target"]

oracle = QuantumCircuit(2)
if target == '11':
    oracle.cz(0, 1)
elif target == '10':
    oracle.x(1)
    oracle.cz(0, 1)
    oracle.x(1)
elif target == '01':
    oracle.x(0)
    oracle.cz(0, 1)
    oracle.x(0)
elif target == '00':
    oracle.x([0, 1])
    oracle.cz(0, 1)
    oracle.x([0, 1])
else:
    raise ValueError("Invalid target state")

backend = Aer.get_backend('qasm_simulator')

grover_circuit = QuantumCircuit(2)
grover_circuit.h([0, 1])
grover_circuit.append(oracle, [0, 1])   
grover_circuit.h([0, 1])

problem = AmplificationProblem(grover_circuit, is_good_state=lambda bitstring: bitstring == target)

grover = Grover(sampler=Sampler())
result = grover.amplify(problem)

result = {"oracle_evaluation": result.oracle_evaluation, "top_measurement": result.top_measurement,
          "circuit_results":result.circuit_results}
print(json.dumps(result))
