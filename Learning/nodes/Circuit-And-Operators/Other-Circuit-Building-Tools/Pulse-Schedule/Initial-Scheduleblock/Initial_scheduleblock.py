from qiskit import pulse
 
import io
import base64
import json

with pulse.build(name='my_example') as my_program:
    # Add instructions here
    pass

obj = str(my_program)


# # Save the plot to a buffer
# buffer = io.BytesIO()
# circ.draw('mpl').savefig(buffer, format='png')
# buffer.seek(0)

# # Convert the plot to a Base64 string
# b64_str = base64.b64encode(buffer.read()).decode('utf-8')
# buffer.close()



result = {
    "result_obj": obj
}

# Return the result as a JSON string
print(json.dumps(result))




