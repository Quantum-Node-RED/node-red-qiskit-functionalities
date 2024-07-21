import base64
import io
import json
import pickle
import sys
from qiskit import QuantumCircuit

data = json.loads(sys.argv[1])
target = data["target"]
gates_list = data["gates"]
num_qubits = len(target)

if not all(c in '01' for c in target):
    raise ValueError("Target must be a binary string.")
    
# store the oracle for Grover's algorithm
oracle = QuantumCircuit(num_qubits)

for gate in gates_list:
    type = gate["type"]
    qubits_para = gate["qubits"]
    if type == "x":
        oracle.x(int(qubits_para[0]))
    elif type == "cz":
        oracle.cz(int(qubits_para[0]), int(qubits_para[1]))
    elif type == "ccx":
        oracle.ccx(int(qubits_para[0]), int(qubits_para[1]), int(qubits_para[2]))
    elif type == "ccz":
        oracle.ccz(int(qubits_para[0]), int(qubits_para[1]), int(qubits_para[2]))    


with open('oracle.pkl', 'wb') as f:
    pickle.dump(oracle, f) 
    
# with open('oracle.pkl', 'rb') as f:
#     oracle_test = pickle.load(f)    
    
    

# Test Script for nodes\test\flow\Build_Gate_Oracle_Test.json
# circuit_image = oracle.draw(output='mpl', filename='oracle.png')
# buffer = io.BytesIO()
# circuit_image.savefig(buffer, format='png')
# buffer.seek(0)
# image_b64 = base64.b64encode(buffer.read()).decode('utf-8')
# buffer.close()

# print(json.dumps({"target": target, "gates": gates_list, "num_qubits": num_qubits, "image": image_b64}))


