import base64
import json
from qiskit import QuantumCircuit
from qiskit import QuantumRegister, ClassicalRegister
import io

# Build a quantum circuit
q_a = QuantumRegister(3, name="a")
q_b = QuantumRegister(5, name="b")
c_a = ClassicalRegister(3)
c_b = ClassicalRegister(5)
 
circuit = QuantumCircuit(q_a, q_b, c_a, c_b)
circuit.x(q_a[1])
circuit.x(q_b[1])
circuit.x(q_b[2])
circuit.x(q_b[4])
circuit.barrier()
circuit.h(q_a)
circuit.barrier(q_a)
circuit.h(q_b)
circuit.cswap(q_b[0], q_b[1], q_b[2])
circuit.cswap(q_b[2], q_b[3], q_b[4])
circuit.cswap(q_b[3], q_b[4], q_b[0])
circuit.barrier(q_b)
circuit.measure(q_a, c_a)
circuit.measure(q_b, c_b);

# Draw the circuit
customize_mpl_draw_str = circuit.draw(output="mpl", reverse_bits=True)
buffer = io.BytesIO()
customize_mpl_draw_str.savefig(buffer, format='png') 
buffer.seek(0)
customize_mpl_draw_str_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

result = {
    "circuit_diagram": customize_mpl_draw_str_b64
}

print(json.dumps(result))
