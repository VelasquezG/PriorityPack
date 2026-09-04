from app.algorithms.merge_sort import merge_sort


shipments = [
    {"Order_ID": "A001", "Priority_Score": 25},
    {"Order_ID": "A002", "Priority_Score": 80},
    {"Order_ID": "A003", "Priority_Score": 40},
    {"Order_ID": "A004", "Priority_Score": 100},
    {"Order_ID": "A005", "Priority_Score": 60},
]


print("ANTES:")
print(shipments)

print()
print("DESPUÉS:")

sorted_shipments = merge_sort(shipments)

for shipment in sorted_shipments:
    print(
        shipment["Order_ID"],
        "->",
        shipment["Priority_Score"]
    )