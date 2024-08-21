import json,io,base64
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
angle = Parameter("angle")  # undefined number
 
# Create and optimize circuit once
qc = QuantumCircuit(1)
qc.rx(angle, 0)
 
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
qc = generate_preset_pass_manager(optimization_level=3, basis_gates=['u', 'cx']).run(qc)
 
circuit_diagram=qc.draw("mpl")
buffer=io.BytesIO()
circuit_diagram.savefig(buffer, format="png")
buffer.seek(0)
circuit_diagram_base64=base64.b64encode(buffer.read()).decode("utf-8")
buffer.close()
result={
    "circuit_diagram": circuit_diagram_base64,
    "parameters": str(qc.parameters)
}
print(json.dumps(result))
