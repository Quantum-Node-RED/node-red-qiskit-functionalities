import sys
import json
from numpy.linalg import eigvalsh
from qiskit.quantum_info import SparsePauliOp

input = sys.argv[1]
parsed_input = json.loads(input)

optimal_value = parsed_input["optimal_value"]
pauli_list = parsed_input["paulis"]

hamiltonian_data = []
hamiltonian_coeffs = []
for pauli in pauli_list:
  hamiltonian_data.append(pauli["term"])
  hamiltonian_coeffs.append(pauli["coeff"])

observable_matrix = SparsePauliOp(hamiltonian_data, coeffs=hamiltonian_coeffs)
solution_eigenvalue = min(eigvalsh(observable_matrix))

assert isinstance(optimal_value, (int, float)) and isinstance(solution_eigenvalue, (int, float)), "Error: value is not number."
assert solution_eigenvalue != 0, "Error: solution_eigenvalue is zero."

percent_error = round(abs((optimal_value - solution_eigenvalue)/solution_eigenvalue), 6)


result = {
  "quantum_result": optimal_value,
  "classical_result": solution_eigenvalue,
  "percent_error": percent_error
}

print(json.dumps(result))

  