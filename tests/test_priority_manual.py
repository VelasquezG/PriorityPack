from app.services.priority_service import (
    calculate_priority_score,
    get_priority_level
)


# Envío de prueba
shipment = {
    "Traffic": "Medium",
    "Weather": "Windy",
    "Area": "Metropolitian",
    "Order_Hour": 15
}


# Calcular prioridad
score = calculate_priority_score(shipment)

# Obtener nivel
level = get_priority_level(score)


print("================================")
print("      PRUEBA PRIORITYPACK")
print("================================")
print(f"Traffic:      {shipment['Traffic']}")
print(f"Weather:      {shipment['Weather']}")
print(f"Area:         {shipment['Area']}")
print(f"Order Hour:   {shipment['Order_Hour']}")
print("--------------------------------")
print(f"Priority Score: {score}")
print(f"Priority Level: {level}")
print("================================")