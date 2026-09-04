# app/services/analysis_service.py

import time

from app.algorithms.merge_sort import merge_sort
from app.algorithms.traditional_sort import bubble_sort


def is_sorted_correctly(shipments):
    """
    Verifica que los envíos estén ordenados
    de mayor a menor Priority_Score.
    """

    return all(
        shipments[i]["Priority_Score"]
        >= shipments[i + 1]["Priority_Score"]
        for i in range(len(shipments) - 1)
    )


def measure_algorithm(algorithm, shipments):
    """
    Ejecuta un algoritmo y mide su tiempo de ejecución.
    """

    start = time.perf_counter()

    result = algorithm(shipments)

    end = time.perf_counter()

    execution_time = end - start

    return {
        "result": result,
        "time": execution_time,
        "correct": is_sorted_correctly(result)
    }


def compare_algorithms(shipments):
    """
    Compara Merge Sort contra Bubble Sort.

    Retorna los tiempos de ejecución y
    la relación de mejora.
    """

    merge_result = measure_algorithm(
        merge_sort,
        shipments
    )

    bubble_result = measure_algorithm(
        bubble_sort,
        shipments
    )

    if merge_result["time"] > 0:
        speedup = (
            bubble_result["time"]
            / merge_result["time"]
        )
    else:
        speedup = 0

    return {
        "merge_sort": {
            "time": merge_result["time"],
            "correct": merge_result["correct"]
        },

        "bubble_sort": {
            "time": bubble_result["time"],
            "correct": bubble_result["correct"]
        },

        "speedup": speedup
    }


def benchmark_algorithms(shipments, test_sizes=None):
    """
    Ejecuta un benchmark con diferentes tamaños
    de entrada.

    Retorna los resultados para generar
    tablas y gráficas.
    """

    if test_sizes is None:
        test_sizes = [
            1000,
            5000,
            10000,
            20000,
            len(shipments)
        ]

    results = []

    for size in test_sizes:

        test_data = shipments[:size]

        merge_result = measure_algorithm(
            merge_sort,
            test_data
        )

        bubble_result = measure_algorithm(
            bubble_sort,
            test_data
        )

        if merge_result["time"] > 0:
            speedup = (
                bubble_result["time"]
                / merge_result["time"]
            )
        else:
            speedup = 0

        results.append({
            "Registros": size,
            "Merge_Sort": merge_result["time"],
            "Bubble_Sort": bubble_result["time"],
            "Speedup": speedup,
            "Merge_Correcto": merge_result["correct"],
            "Bubble_Correcto": bubble_result["correct"]
        })

    return results