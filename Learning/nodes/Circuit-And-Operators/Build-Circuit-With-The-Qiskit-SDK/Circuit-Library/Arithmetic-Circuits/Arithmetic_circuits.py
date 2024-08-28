from qiskit.circuit.library import CDKMRippleCarryAdder
adder = CDKMRippleCarryAdder(3)  # Adder of 3-bit numbers
from qiskit.primitives import Sampler
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import base64,io,json
# Create the number A=2
reg_a = QuantumRegister(3, 'a')
number_a = QuantumCircuit(reg_a)
number_a.initialize(2) # Number 2; |010>
 
# Create the number B=3
reg_b = QuantumRegister(3, 'b')
number_b = QuantumCircuit(reg_b)
number_b.initialize(3)  # Number 3; |011>
 
# Create a circuit to hold everything, including a classical register for
# the result
reg_result = ClassicalRegister(3)
circuit = QuantumCircuit(*adder.qregs, reg_result)
 
# Compose number initializers with the adder. Adder stores the result to
# register B, so we'll measure those qubits.
circuit = circuit.compose(number_a, qubits=reg_a).compose(number_b, qubits=reg_b).compose(adder)
circuit.measure(reg_b, reg_result)
circuit_diagram=circuit.draw('mpl')
buffer=io.BytesIO()
circuit_diagram.savefig(buffer, format='png')
buffer.seek(0)
circuit_diagram_base64 = base64.b64encode(buffer.read()).decode('utf-8')

result=Sampler().run(circuit).result()
output=result.quasi_dists[0]
result={
    "circuit_diagram":circuit_diagram_base64,
    "output":str(output)
}
print(json.dumps(result))