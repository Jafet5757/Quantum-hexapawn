""" 
Expresión:
  sumatoria(i=2 hasta n con paso 2) de raiz(n/i)
"""
import math
import numpy as np
import matplotlib.pyplot as plt

def complex_QBS(max_n=30):
  """ 
    Complejidad del algoritmo de búsqueda binaria cuántica 
  """
  values = []
  for n in range(2, max_n+2, 2):
    sumatoria = 0
    for i in range(2, n+2, 2):
      sumatoria += math.sqrt(n/i)
    print(f"Sumatoria para n={n}: {sumatoria}")
    values.append(sumatoria)

  return values

def complex_classical_search(max_n=30):
  """ 
    Complejidad del algoritmo de búsqueda binaria clásica
    es lineal O(n) 
  """
  # Create a list of values
  values = np.arange(2, max_n, 2)

  return values

def plot_complexity(max_n=30):

  # Get the values for the quantum algorithm
  values_qbs = complex_QBS(max_n)
  # Get the values for the classical algorithm
  values_classical = complex_classical_search(max_n)

  # Plot the values
  plt.plot(values_qbs, label="Quantum Binary Search")
  plt.plot(values_classical, label="Classical Binary Search")
  plt.xlabel("n")
  plt.ylabel("Complexity")
  plt.legend()
  plt.show()

if __name__ == "__main__":
  plot_complexity(max_n=30)