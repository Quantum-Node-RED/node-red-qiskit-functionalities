from qiskit.circuit.library import PauliEvolutionGate
from qiskit.circuit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
import io
import base64
import json
# Prepare an initial state with a Hamadard on the middle qubit
state = QuantumCircuit(3)
state.h(1)
 
hamiltonian = SparsePauliOp(["ZZI", "IZZ"])
evolution = PauliEvolutionGate(hamiltonian, time=1)
 
# Evolve state by appending the evolution gate
state.compose(evolution, inplace=True)
 
circuits_diagarm=state.draw('mpl')
buffer=io.BytesIO()
circuits_diagarm.savefig(buffer, format='png')
buffer.seek(0)
circuit_diagarm_base64 = base64.b64encode(buffer.read()).decode('utf-8')

result = {
    "circuit_diagram": circuit_diagarm_base64,
}

print(json.dumps(result))