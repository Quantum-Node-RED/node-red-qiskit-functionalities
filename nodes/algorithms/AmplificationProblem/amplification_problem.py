import sys
import json
import io
import base64
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit_aer.primitives import Sampler
from qiskit_algorithms import AmplificationProblem, Grover
from qiskit.visualization import circuit_drawer
import matplotlib.pyplot as plt

try:
    # msg.payload from node-red
    data = json.loads(sys.argv[1])
    target = data["target"]
    iterations_times = data.get("iterations",-1)
except json.JSONDecodeError:
    print("Error: Failed to decode JSON from input.")
    sys.exit(1)
except IndexError:
    print("Error: No input data provided.")
    sys.exit(1)

num_qubits = len(target)
oracle = QuantumCircuit(num_qubits)

try:
    if not all(c in '01' for c in target):
        raise ValueError("Target must be a binary string.")

    num_qubits = len(target)
    oracle = QuantumCircuit(num_qubits)

    # Apply X gates where the target bits are 0
    for i, char in enumerate(target):
        if char == '0':
            oracle.x(i)

    # Apply multi-controlled NOT gate
    oracle.mcx(list(range(num_qubits-1)), num_qubits-1)

    # Reapply X gates to restore the states
    for i, char in enumerate(target):
        if char == '0':
            oracle.x(i)

    # Apply Z gate to the ancilla to introduce a phase flip
    oracle.z(num_qubits-1)  

    backend = Aer.get_backend('qasm_simulator')

    problem = AmplificationProblem(oracle, is_good_state=lambda bitstring: bitstring == target)
    if iterations_times == -1:
        grover = Grover(sampler=Sampler())
    else:
        if ',' in iterations_times:
            iterations_times = iterations_times.split(',')
            iterations_times = [int(i) for i in iterations_times]
            grover = Grover(iterations=iterations_times, sampler=Sampler())
        else:    
            iterations_times = int(iterations_times)    
            grover = Grover(iterations=iterations_times, sampler=Sampler())
    result = grover.amplify(problem)

    circuit_image = circuit_drawer(problem.grover_operator.decompose(), output='mpl')
    buffer = io.BytesIO()
    circuit_image.savefig(buffer, format='png')
    buffer.seek(0)
    image_b64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    result_dict = result.circuit_results
    new_result_dict = {}
    for d in result_dict:
        for key, value in d.items():
            new_result_dict[key] = value    

    states = list(new_result_dict.keys())
    counts = list(new_result_dict.values())

    buffer = io.BytesIO()
    plt.figure(figsize=(10, 5)) 
    plt.bar(states, counts, color='blue')  
    plt.xlabel('Quantum States')  
    plt.ylabel('Counts')  
    plt.title('Results of Quantum Measurements')  
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    circuit_image_b64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    output = {
        "oracle_evaluation": result.oracle_evaluation,
        "top_measurement": result.top_measurement,
        "circuit_results": result.circuit_results,
        "circuit_results_image": circuit_image_b64,
        "circuit_image": image_b64
    }

    print(json.dumps(output))
except Exception as e:
    print(f"An error occurred: {str(e)}")
    sys.exit(1)

