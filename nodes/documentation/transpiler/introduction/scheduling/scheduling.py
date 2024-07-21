from qiskit_ibm_runtime.fake_provider import FakeWashingtonV2
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.timing_constraints import TimingConstraints
import base64
import json
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
from qiskit_ibm_runtime.fake_provider import FakeAuckland, FakeWashingtonV2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
import io
from qiskit.visualization import plot_circuit_layout, timeline_drawer, timeline
from qiskit_aer import Aer
import pickle
 
ghz = QuantumCircuit(5)
ghz.h(0)
ghz.cx(0, range(1, 5))  
 
 
# Use fake pulse-enabled backend
backend = FakeWashingtonV2()
 
# Run with optimization level 3 and 'asap' scheduling pass
pass_manager = generate_preset_pass_manager(
    optimization_level=3,
    backend=backend,
    timing_constraints=backend.target.timing_constraints(),
    scheduling_method="asap"
)
 
 
circ = pass_manager.run(ghz, backend)
circ_image = circ.draw(output="mpl", idle_wires=False)
# This method marked as Deprecated since version 1.1.0_pending
circ_timeline_image = timeline.draw(program=circ, show_delays=True, plot_barriers=True, show_clbits=True)

buffer = io.BytesIO()
circ_image.savefig(buffer, format='png')
buffer.seek(0)
circ_image_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

buffer = io.BytesIO()
circ_timeline_image.savefig(buffer, format='png')
buffer.seek(0)
circ_timeline_image_b64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()

result = {
    "circ_image": circ_image_b64,
    "circ_timeline_image": circ_timeline_image_b64
}

print(json.dumps(result))