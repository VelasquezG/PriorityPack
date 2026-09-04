from app.algorithms.traditional_sort import bubble_sort


shipments = [
    {"Order_ID": "A", "Priority_Score": 30},
    {"Order_ID": "B", "Priority_Score": 90},
    {"Order_ID": "C", "Priority_Score": 50},
    {"Order_ID": "D", "Priority_Score": 10},
]


print("Lista original:")

for shipment in shipments:
    print(
        shipment["Order_ID"],
        "->",
        shipment["Priority_Score"]
    )


sorted_shipments = bubble_sort(shipments)


print()
print("Lista ordenada con Bubble Sort:")

for shipment in sorted_shipments:
    print(
        shipment["Order_ID"],
        "->",
        shipment["Priority_Score"]
    )


is_sorted = all(
    sorted_shipments[i]["Priority_Score"]
    >= sorted_shipments[i + 1]["Priority_Score"]
    for i in range(len(sorted_shipments) - 1)
)


print()
print(f"¿Resultado correctamente ordenado?: {is_sorted}")