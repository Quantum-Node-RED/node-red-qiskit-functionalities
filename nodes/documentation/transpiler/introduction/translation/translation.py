import base64
import json
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeAuckland, FakeWashingtonV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import io
from qiskit.visualization import plot_circuit_layout
from qiskit_aer import Aer
import pickle
import os

file_path = 'backend_state.pkl'
with open(file_path, 'rb') as f:
    backend = pickle.load(f)
    
# os.remove(file_path)    

native_gates = "native gates: "+str(backend.operation_names)
qc = QuantumCircuit(2)
qc.swap(0, 1)
qubit_circuit = qc.decompose().draw('mpl')
buffer = io.BytesIO()
qubit_circuit.savefig(buffer, format='png') 
buffer.seek(0)
qubit_circuit_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

qc2 = QuantumCircuit(3)
qc2.ccx(0, 1, 2)
qubit_circuit_2 = qc2.decompose().draw('mpl')
buffer = io.BytesIO()
qubit_circuit_2.savefig(buffer, format='png') 
buffer.seek(0)
qubit_circuit_2_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()


result = {
    "native_gates": native_gates,
    "qubit_circuit_image": qubit_circuit_b64,
    "qubit_circuit_image_2": qubit_circuit_2_b64
}

print(json.dumps(result))

