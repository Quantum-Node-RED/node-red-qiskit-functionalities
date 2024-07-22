
from qiskit.circuit import QuantumCircuit, QuantumRegister, ClassicalRegister
import json,io,base64

qubits = QuantumRegister(2)
clbits = ClassicalRegister(2)
circuit = QuantumCircuit(qubits, clbits)
(q0, q1) = qubits
(c0, c1) = clbits
 
circuit.h(q0)
circuit.measure(q0, c0)
with circuit.if_test((c0, 1)) as else_:
    circuit.h(q1)
with else_:
    circuit.x(q1)
measure=str(circuit.measure(q1, c1))
circuite_diagram=circuit.draw("mpl") 
buffer=io.BytesIO()
circuite_diagram.savefig(buffer, format="png")
buffer.seek(0)
circuit_diagram_base64=base64.b64encode(buffer.read()).decode("utf-8")
buffer.close()
result={
    "measure":measure,
    "circuit_diagram": circuit_diagram_base64
}
print(json.dumps(result))
