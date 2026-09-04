# tests/plot_algorithm_comparison.py

import matplotlib.pyplot as plt


# ============================================================
# DATOS DEL BENCHMARK
# ============================================================

sizes = [
    1000,
    5000,
    10000,
    20000,
    43739
]

merge_sort_times = [
    0.002680,
    0.016729,
    0.042414,
    0.088254,
    0.202798
]

bubble_sort_times = [
    0.071839,
    2.247129,
    9.457787,
    42.583670,
    272.035920
]


# ============================================================
# GRÁFICA CON ESCALA LOGARÍTMICA
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    sizes,
    merge_sort_times,
    marker="o",
    label="Merge Sort - O(n log n)"
)

plt.plot(
    sizes,
    bubble_sort_times,
    marker="o",
    label="Bubble Sort - O(n²)"
)


# Escala logarítmica en el eje Y
plt.yscale("log")


plt.title(
    "Comparación de rendimiento - Escala logarítmica"
)

plt.xlabel(
    "Cantidad de registros"
)

plt.ylabel(
    "Tiempo de ejecución (segundos)"
)

plt.legend()

plt.grid(True, which="both")

plt.tight_layout()


# Guardar gráfica
plt.savefig(
    "data/processed/algorithm_comparison_log.png",
    dpi=300
)


plt.show()