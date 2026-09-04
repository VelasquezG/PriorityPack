# tests/test_algorithm_comparison.py

import time

import pandas as pd

from app.services.priority_service import calculate_priorities
from app.algorithms.merge_sort import merge_sort
from app.algorithms.traditional_sort import bubble_sort


CSV_PATH = "data/raw/amazon_delivery.csv"


# ============================================================
# 1. CARGAR DATASET
# ============================================================

df = pd.read_csv(CSV_PATH)


# ============================================================
# 2. LIMPIAR DATOS DE TEXTO
# ============================================================

text_columns = [
    "Weather",
    "Traffic",
    "Vehicle",
    "Area",
    "Category"
]

for column in text_columns:
    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
    )


# ============================================================
# 3. OBTENER HORA DEL PEDIDO
# ============================================================

df["Order_Hour"] = pd.to_datetime(
    df["Order_Time"],
    format="%H:%M:%S",
    errors="coerce"
).dt.hour


# ============================================================
# 4. CALCULAR PRIORIDADES
# ============================================================

shipments = df.to_dict(orient="records")

print()
print("==========================================")
print("       PRIORITYPACK")
print("==========================================")

print(f"Total de envíos disponibles: {len(shipments)}")

print()
print("Calculando Priority Score...")

start_priority = time.perf_counter()

processed_shipments = calculate_priorities(shipments)

end_priority = time.perf_counter()

priority_time = end_priority - start_priority

print(
    f"Tiempo de cálculo de prioridad: "
    f"{priority_time:.6f} segundos"
)


# ============================================================
# 5. TAMAÑOS PARA EL BENCHMARK
# ============================================================

test_sizes = [
    1000,
    5000,
    10000,
    20000,
    len(processed_shipments)
]


results = []


# ============================================================
# 6. COMPARAR ALGORITMOS
# ============================================================

for size in test_sizes:

    print()
    print("==========================================")
    print(f"       PRUEBA CON {size:,} REGISTROS")
    print("==========================================")

    test_data = processed_shipments[:size]


    # --------------------------------------------------------
    # MERGE SORT
    # --------------------------------------------------------

    print()
    print("Ejecutando Merge Sort...")

    start_merge = time.perf_counter()

    merge_result = merge_sort(test_data)

    end_merge = time.perf_counter()

    merge_time = end_merge - start_merge


    # Verificar resultado
    merge_correct = all(
        merge_result[i]["Priority_Score"]
        >= merge_result[i + 1]["Priority_Score"]
        for i in range(len(merge_result) - 1)
    )


    # --------------------------------------------------------
    # BUBBLE SORT
    # --------------------------------------------------------

    print("Ejecutando Bubble Sort...")

    start_bubble = time.perf_counter()

    bubble_result = bubble_sort(test_data)

    end_bubble = time.perf_counter()

    bubble_time = end_bubble - start_bubble


    # Verificar resultado
    bubble_correct = all(
        bubble_result[i]["Priority_Score"]
        >= bubble_result[i + 1]["Priority_Score"]
        for i in range(len(bubble_result) - 1)
    )


    # --------------------------------------------------------
    # CALCULAR MEJORA
    # --------------------------------------------------------

    if merge_time > 0:
        speedup = bubble_time / merge_time
    else:
        speedup = 0


    # --------------------------------------------------------
    # GUARDAR RESULTADOS
    # --------------------------------------------------------

    results.append({
        "Registros": size,
        "Merge_Sort": merge_time,
        "Bubble_Sort": bubble_time,
        "Speedup": speedup,
        "Merge_Correcto": merge_correct,
        "Bubble_Correcto": bubble_correct
    })


    # --------------------------------------------------------
    # MOSTRAR RESULTADOS
    # --------------------------------------------------------

    print()
    print(f"Merge Sort : {merge_time:.6f} segundos")
    print(f"Bubble Sort: {bubble_time:.6f} segundos")

    print(
        f"Mejora aproximada: "
        f"{speedup:.2f}x"
    )

    print(
        f"Merge Sort correcto: "
        f"{merge_correct}"
    )

    print(
        f"Bubble Sort correcto: "
        f"{bubble_correct}"
    )


# ============================================================
# 7. MOSTRAR TABLA FINAL
# ============================================================

results_df = pd.DataFrame(results)


print()
print("==========================================")
print("       COMPARACIÓN FINAL")
print("==========================================")

print(
    results_df.to_string(
        index=False,
        formatters={
            "Merge_Sort": "{:.6f}".format,
            "Bubble_Sort": "{:.6f}".format,
            "Speedup": "{:.2f}x".format
        }
    )
)