# Built-in modules
import math

# Imports from Qiskit
from qiskit import QuantumCircuit
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from qiskit.visualization import plot_distribution
import matplotlib.pyplot as plt

from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram

def grover_oracle(marked_states):
  """Build a Grover oracle for multiple marked states

  Here we assume all input marked states have the same number of bits

  Parameters:
      marked_states (str or list): Marked states of oracle

  Returns:
      QuantumCircuit: Quantum circuit representing Grover oracle
  """
  if not isinstance(marked_states, list):
      marked_states = [marked_states]
  # Compute the number of qubits in circuit
  num_qubits = len(marked_states[0])

  qc = QuantumCircuit(num_qubits)
  # Mark each target state in the input list
  for target in marked_states:
      # Flip target bit-string to match Qiskit bit-ordering
      rev_target = target[::-1]
      # Find the indices of all the '0' elements in bit-string
      zero_inds = [ind for ind in range(num_qubits) if rev_target.startswith("0", ind)]
      # Add a multi-controlled Z-gate with pre- and post-applied X-gates (open-controls)
      # where the target bit-string has a '0' entry
      qc.x(zero_inds)
      qc.compose(MCMT(ZGate(), num_qubits - 1, 1), inplace=True)
      qc.x(zero_inds)
  return qc

def grover_search(marked_states):
  
  if len(marked_states) == 0:
    return None
  
  oracle = grover_oracle(marked_states)
  oracle.draw(output="mpl", style="iqp")

  grover_op = GroverOperator(oracle)
  grover_op.decompose().draw(output="mpl", style="iqp")


  optimal_num_iterations = math.floor(
      math.pi / (4 * math.asin(math.sqrt(len(marked_states) / 2**grover_op.num_qubits)))
  )
  optimal_num_iterations


  qc = QuantumCircuit(grover_op.num_qubits)
  # Create even superposition of all basis states
  qc.h(range(grover_op.num_qubits))
  # Apply Grover operator the optimal number of times
  qc.compose(grover_op.power(optimal_num_iterations), inplace=True)
  # Measure all qubits
  qc.measure_all()
  qc.draw(output="mpl", style="iqp")

  from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

  pm = generate_preset_pass_manager( optimization_level=3)

  circuit_isa = pm.run(qc)
  #circuit_isa.draw(output="mpl", idle_wires=False, style="iqp")



  # To run on local simulator:
  #   1. Use the SatetvectorSampler from qiskit.primitives instead

  simulator = AerSimulator()

  # Transpilar el circuito para el simulador
  compiled_circuit = circuit_isa.decompose()

  # Ejecutar el circuito en el simulador con 10,000 tiros
  job = simulator.run(compiled_circuit, shots=10_000)
  result = job.result()

  # Obtener los resultados de las mediciones
  counts = result.get_counts()

  # Imprimir los resultados
  print(counts)

  # Mostrar un histograma de los resultados
  plot_histogram(counts)
  #plt.show()
  
  return counts
  
  
# marked_states = ["001111", "001101"]