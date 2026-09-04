# Cálculo del Priority Score

# app/services/priority_service.py

def normalize_text(value):
    """
    Normaliza valores de texto para evitar problemas
    con espacios o diferencias de mayúsculas/minúsculas.
    """
    if value is None:
        return ""

    return str(value).strip().lower()


# ==========================================
# PUNTAJES POR VARIABLE
# ==========================================

TRAFFIC_SCORE = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "jam": 4
}


WEATHER_SCORE = {
    "sunny": 1,
    "sandstorms": 2,
    "stormy": 2,
    "windy": 2,
    "fog": 3,
    "cloudy": 3
}


AREA_SCORE = {
    "other": 1,
    "urban": 2,
    "metropolitian": 3,
    "semi-urban": 4
}


# ==========================================
# FUNCIONES DE PUNTAJE
# ==========================================

def get_traffic_score(traffic):
    """
    Convierte Traffic en un valor de riesgo entre 1 y 4.
    """
    traffic = normalize_text(traffic)

    return TRAFFIC_SCORE.get(traffic, 1)


def get_weather_score(weather):
    """
    Convierte Weather en un valor de riesgo entre 1 y 3.
    """
    weather = normalize_text(weather)

    return WEATHER_SCORE.get(weather, 1)


def get_area_score(area):
    """
    Convierte Area en un valor de riesgo entre 1 y 4.
    """
    area = normalize_text(area)

    return AREA_SCORE.get(area, 1)


def get_hour_score(order_hour):
    """
    Convierte la hora del pedido en un nivel de riesgo.

    Las horas 19, 20 y 21 presentan históricamente
    los mayores tiempos de entrega en nuestro análisis.
    """

    try:
        hour = int(order_hour)
    except (ValueError, TypeError):
        return 1

    if hour in [19, 20, 21]:
        return 4

    if hour in [11, 12, 13, 14, 17, 18]:
        return 3

    if hour in [15, 16]:
        return 2

    return 1


# ==========================================
# NORMALIZACIÓN
# ==========================================

def normalize_score(score, minimum, maximum):
    """
    Lleva un puntaje de su rango original a una escala 0-100.
    """

    if maximum == minimum:
        return 0

    return ((score - minimum) / (maximum - minimum)) * 100


# ==========================================
# PRIORITY SCORE
# ==========================================

def calculate_priority_score(shipment):
    """
    Calcula el Priority Score de un envío.

    Variables utilizadas:
        Traffic    -> 35%
        Weather    -> 30%
        Order_Hour -> 20%
        Area       -> 15%

    Retorna un valor entre 0 y 100.
    """

    traffic = get_traffic_score(
        shipment.get("Traffic")
    )

    weather = get_weather_score(
        shipment.get("Weather")
    )

    area = get_area_score(
        shipment.get("Area")
    )

    hour = get_hour_score(
        shipment.get("Order_Hour")
    )

    # Normalizamos cada variable a 0-100

    traffic_normalized = normalize_score(
        traffic,
        1,
        4
    )

    weather_normalized = normalize_score(
        weather,
        1,
        3
    )

    area_normalized = normalize_score(
        area,
        1,
        4
    )

    hour_normalized = normalize_score(
        hour,
        1,
        4
    )

    # ======================================
    # CÁLCULO DEL SCORE
    # ======================================

    priority_score = (
        traffic_normalized * 0.35
        + weather_normalized * 0.30
        + hour_normalized * 0.20
        + area_normalized * 0.15
    )

    return round(priority_score, 2)


# ==========================================
# NIVEL DE PRIORIDAD
# ==========================================

def get_priority_level(priority_score):
    """
    Clasifica el envío según su Priority Score.
    """

    if priority_score >= 70:
        return "Alta"

    if priority_score >= 40:
        return "Media"

    return "Baja"


# ==========================================
# PROCESAR ENVÍO
# ==========================================

def process_shipment(shipment):
    """
    Calcula el score y nivel de prioridad
    de un único envío.
    """

    score = calculate_priority_score(shipment)

    shipment["Priority_Score"] = score

    shipment["Priority_Level"] = get_priority_level(
        score
    )

    return shipment


# ==========================================
# PROCESAR TODOS LOS ENVÍOS
# ==========================================

def calculate_priorities(shipments):
    """
    Calcula la prioridad de todos los envíos.
    """

    processed_shipments = []

    for shipment in shipments:
        processed_shipment = process_shipment(
            shipment.copy()
        )

        processed_shipments.append(
            processed_shipment
        )

    return processed_shipments