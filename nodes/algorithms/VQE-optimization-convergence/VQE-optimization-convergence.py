import sys
import json
import numpy as np
import pylab
import matplotlib.pyplot as plt 

from qiskit.primitives import Estimator
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import TwoLocal
from qiskit_algorithms import VQE
from qiskit_algorithms.utils import algorithm_globals
from qiskit_algorithms.optimizers import COBYLA, L_BFGS_B, SLSQP

input = sys.argv[1]
parse_input = json.loads(input)

num_qubits = parse_input["numQubits"]

H2_op = SparsePauliOp.from_list(  # TODO: convert to input or attributes
    [
        ("II", -1.052373245772859),
        ("IZ", 0.39793742484318045),
        ("ZI", -0.39793742484318045),
        ("ZZ", -0.01128010425623538),
        ("XX", 0.18093119978423156),
    ]
)

estimator = Estimator()

optimizers = [COBYLA(maxiter=80), L_BFGS_B(maxiter=60), SLSQP(maxiter=60)]
converge_counts = np.empty([len(optimizers)], dtype=object)
converge_vals = np.empty([len(optimizers)], dtype=object)

rotation_blocks = "ry"           # TODO: convert to input or attributes
entanglement_blocks = "cz"      # TODO: convert to input or attributes

for i, optimizer in enumerate(optimizers):
    algorithm_globals.random_seed = 50
    ansatz = TwoLocal(rotation_blocks=rotation_blocks, entanglement_blocks=entanglement_blocks)

    counts = []
    values = []

    def store_intermediate_result(eval_count, parameters, mean, std):
        counts.append(eval_count)
        values.append(mean)

    vqe = VQE(estimator, ansatz, optimizer, callback=store_intermediate_result)
    result = vqe.compute_minimum_eigenvalue(operator=H2_op)
    converge_counts[i] = np.asarray(counts)
    converge_vals[i] = np.asarray(values)


pylab.rcParams["figure.figsize"] = (12, 8)
for i, optimizer in enumerate(optimizers):
    pylab.plot(converge_counts[i], converge_vals[i], label=type(optimizer).__name__)
pylab.xlabel("Eval count")
pylab.ylabel("Energy")
pylab.title("Energy convergence for various optimizers")
pylab.legend(loc="upper right")
plt.show()
