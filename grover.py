from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

qc = QuantumCircuit(3, 3)

qc.h([0, 1, 2])

# Marcamos el estado |110⟩
qc.x(0) # Marcamos el menos significativo
qc.ccz(0, 1, 2)
qc.x(0)

# Difusión cuántica
qc.h([0, 1, 2])
qc.x([0, 1, 2])
qc.ccz(0, 1, 2)
qc.x([0, 1, 2])
qc.h([0, 1, 2])

# Medición
qc.measure([0, 1, 2], [0, 1, 2])

# Simulación del circuito
simulator = AerSimulator()

result = simulator.run(qc, backend=simulator).result()
counts = result.get_counts()
plot_histogram(counts)
plt.show()