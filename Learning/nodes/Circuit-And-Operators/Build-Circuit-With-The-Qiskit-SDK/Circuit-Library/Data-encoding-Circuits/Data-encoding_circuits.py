from qiskit.circuit.library import ZZFeatureMap
import base64
import io
import json
features = [0.2, 0.4, 0.8]
feature_map = ZZFeatureMap(feature_dimension=len(features))
encoded = feature_map.assign_parameters(features)
circuit_diagram=encoded.draw('mpl')
buffer=io.BytesIO() 
circuit_diagram.savefig(buffer, format='png')
buffer.seek(0)
circuit_diagarm_base64 = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()
result={
    "circuit_diagram": circuit_diagarm_base64,
}
print(json.dumps(result))