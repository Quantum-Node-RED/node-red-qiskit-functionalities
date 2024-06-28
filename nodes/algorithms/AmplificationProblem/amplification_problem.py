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

num_qubits = len(target)
oracle = QuantumCircuit(num_qubits)

for i, char in enumerate(target):
    if char == '0':
        oracle.x(i)  
oracle.mcx(list(range(num_qubits-1)), num_qubits-1)  
for i, char in enumerate(target):
    if char == '0':
        oracle.x(i)  

backend = Aer.get_backend('qasm_simulator')

grover_circuit = QuantumCircuit(num_qubits)
grover_circuit.h(range(num_qubits))
grover_circuit.append(oracle, range(num_qubits))
grover_circuit.h(range(num_qubits))

problem = AmplificationProblem(grover_circuit, is_good_state=lambda bitstring: bitstring == target)

grover = Grover(sampler=Sampler())
result = grover.amplify(problem)

# The prossibility of the each state
result = {"oracle_evaluation": result.oracle_evaluation, "top_measurement": result.top_measurement,
          "circuit_results":result.circuit_results}
print(json.dumps(result))
