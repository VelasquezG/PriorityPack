
# app/services/complexity_service.py

"""
Análisis teórico de complejidad para PriorityPack.

Aplica el Teorema Maestro a Merge Sort y documenta
la complejidad temporal de Bubble Sort.
"""


def get_merge_sort_complexity():
    """
    Devuelve la resolución de la recurrencia de Merge Sort
    mediante el Teorema Maestro.
    """

    return {
        "algorithm": "Merge Sort",
        "recurrence": "T(n) = 2T(n/2) + Θ(n)",
        "a": 2,
        "b": 2,
        "f_n": "Θ(n)",
        "critical_term": "n^(log_b(a)) = n",
        "master_theorem_case": 2,
        "time_complexity": "Θ(n log n)",
        "space_complexity": "O(n)",
        "explanation": (
            "Merge Sort divide los datos en dos subproblemas "
            "de tamaño n/2 y combina las soluciones en tiempo lineal."
        ),
        "conclusion": (
            "Como f(n) = Θ(n) y n^(log_b(a)) = n, "
            "se aplica el caso 2 del Teorema Maestro."
        ),
    }


def get_bubble_sort_complexity():
    """
    Devuelve el análisis teórico de Bubble Sort.
    La complejidad no se obtiene aplicando directamente
    el Teorema Maestro.
    """

    return {
        "algorithm": "Bubble Sort",
        "recurrence": None,
        "time_complexity": "O(n²)",
        "average_time_complexity": "Θ(n²)",
        "space_complexity": "O(n)",
        "explanation": (
            "Bubble Sort realiza comparaciones entre elementos "
            "adyacentes mediante pasadas sucesivas. En el caso "
            "promedio y peor, el número de operaciones crece "
            "cuadráticamente."
        ),
    }


def get_complexity_analysis():
    """
    Devuelve el análisis teórico completo de PriorityPack.
    """

    return {
        "merge_sort": get_merge_sort_complexity(),
        "bubble_sort": get_bubble_sort_complexity(),
    }
