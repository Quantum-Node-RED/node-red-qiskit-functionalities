import qiskit.qasm2
import io
import base64
import json

program = '''
    OPENQASM 2.0;
    include "qelib1.inc";
    qreg q[2];
    creg c[2];
 
    h q[0];
    cx q[0], q[1];
 
    measure q -> c;
'''


circuit = qiskit.qasm2.loads(program)


# Save the plot to a buffer
buffer = io.BytesIO()
circuit.draw(output ='mpl').savefig(buffer, format='png')
buffer.seek(0)

# Convert the plot to a Base64 string
b64_str = base64.b64encode(buffer.read()).decode('utf-8')
buffer.close()



result = {
    "result_image": b64_str
}

# Return the result as a JSON string
print(json.dumps(result))
