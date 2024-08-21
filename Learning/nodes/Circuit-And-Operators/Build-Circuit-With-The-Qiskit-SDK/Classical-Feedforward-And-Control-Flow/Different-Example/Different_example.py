import json,base64,io
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
qubits = QuantumRegister(3)
clbits = ClassicalRegister(3)
circuit = QuantumCircuit(qubits, clbits)
(q0, q1, q2) = qubits
(c0, c1, c2) = clbits
 
circuit.h([q0, q1])
circuit.measure(q0, c0)
circuit.measure(q1, c1)
with circuit.switch(clbits) as case:
    with case(0b000, 0b011):
        circuit.z(q2)
    with case(0b001):
        circuit.y(q2)
    with case(case.DEFAULT):
        circuit.x(q2)
circuit.measure(q2, c2)

from qiskit_aer import AerSimulator
simulator = AerSimulator()
result = simulator.run(circuit, shots=1024).result()

counts = result.get_counts(circuit)
 
circuit_diagram=circuit.draw("mpl")
buffer=io.BytesIO()
circuit_diagram.savefig(buffer, format="png")
buffer.seek(0)
circuit_diagram_base64=base64.b64encode(buffer.read()).decode("utf-8")
buffer.close()
result={
    "measure":counts,
    "circuit_diagram": circuit_diagram_base64
}
print(json.dumps(result))
 