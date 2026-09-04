import time

import pandas as pd

from app.services.priority_service import calculate_priorities
from app.algorithms.merge_sort import merge_sort


# ==========================================
# 1. CARGAR DATASET
# ==========================================

CSV_PATH = "data/raw/amazon_delivery.csv"

df = pd.read_csv(CSV_PATH)


# ==========================================
# 2. LIMPIAR COLUMNAS DE TEXTO
# ==========================================

text_columns = [
    "Weather",
    "Traffic",
    "Vehicle",
    "Area",
    "Category"
]

for column in text_columns:
    df[column] = df[column].astype("string").str.strip()


# ==========================================
# 3. OBTENER HORA DEL PEDIDO
# ==========================================

df["Order_Hour"] = pd.to_datetime(
    df["Order_Time"],
    format="%H:%M:%S",
    errors="coerce"
).dt.hour


# ==========================================
# 4. CONVERTIR DATAFRAME A DICCIONARIOS
# ==========================================

shipments = df.to_dict(orient="records")


print()
print("==========================================")
print("       PRIORITYPACK")
print("==========================================")

print(f"Total de envíos: {len(shipments)}")


# ==========================================
# 5. CALCULAR PRIORIDADES
# ==========================================

print()
print("Calculando Priority Score...")

start_priority = time.perf_counter()

processed_shipments = calculate_priorities(shipments)

end_priority = time.perf_counter()

priority_time = end_priority - start_priority


print(f"Tiempo de cálculo de prioridad: {priority_time:.6f} segundos")


# ==========================================
# 6. MERGE SORT
# ==========================================

print()
print("Ejecutando Merge Sort...")

start_sort = time.perf_counter()

sorted_shipments = merge_sort(processed_shipments)

end_sort = time.perf_counter()

sort_time = end_sort - start_sort


# ==========================================
# 7. RESULTADOS DEL ALGORITMO
# ==========================================

print()
print("==========================================")
print("       RESULTADOS MERGE SORT")
print("==========================================")

print(f"Tiempo de Merge Sort: {sort_time:.6f} segundos")


# ==========================================
# 8. VERIFICAR QUE ESTÉ ORDENADO
# ==========================================

is_sorted = all(
    sorted_shipments[i]["Priority_Score"]
    >= sorted_shipments[i + 1]["Priority_Score"]
    for i in range(len(sorted_shipments) - 1)
)


print(f"¿Resultado correctamente ordenado?: {is_sorted}")


# ==========================================
# 9. DISTRIBUCIÓN DE PRIORIDADES
# ==========================================

result_df = pd.DataFrame(sorted_shipments)

print()
print("==========================================")
print("       DISTRIBUCIÓN DE PRIORIDADES")
print("==========================================")

print(
    result_df["Priority_Level"]
    .value_counts()
)


# ==========================================
# 10. TOP 10 ENVÍOS
# ==========================================

print()
print("==========================================")
print("       TOP 10 ENVÍOS PRIORITARIOS")
print("==========================================")

top_shipments = sorted_shipments[:10]

for shipment in top_shipments:
    print(
        f"{shipment['Order_ID']} -> "
        f"Score: {shipment['Priority_Score']} -> "
        f"Prioridad: {shipment['Priority_Level']}"
    )


# ==========================================
# 11. ESTADÍSTICAS DEL SCORE
# ==========================================

print()
print("==========================================")
print("       ESTADÍSTICAS DEL SCORE")
print("==========================================")

print(
    result_df["Priority_Score"].describe()
)