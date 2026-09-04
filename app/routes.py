# app/routes.py

import time
from pathlib import Path

import pandas as pd

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    send_file
)

from app.services.priority_service import calculate_priorities
from app.algorithms.merge_sort import merge_sort


main = Blueprint("main", __name__)


# ============================================================
# RUTAS DEL PROYECTO
# ============================================================

# app/routes.py
# parent      -> app
# parent.parent -> PriorityPack

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIRECTORY = PROJECT_ROOT / "data"

PROCESSED_DIRECTORY = DATA_DIRECTORY / "processed"

PRIORITIZED_FILE = (
    PROCESSED_DIRECTORY /
    "amazon_delivery_prioritized.csv"
)


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

@main.route("/", methods=["GET"])
def index():

    return render_template(
        "index.html"
    )


# ============================================================
# PROCESAR ARCHIVO CSV
# ============================================================

@main.route("/process", methods=["POST"])
def process_file():

    # ========================================================
    # 1. VALIDAR ARCHIVO
    # ========================================================

    if "file" not in request.files:

        return jsonify({
            "error":
                "No se recibió ningún archivo."
        }), 400


    file = request.files["file"]


    if file.filename == "":

        return jsonify({
            "error":
                "No se seleccionó ningún archivo."
        }), 400


    if not file.filename.lower().endswith(".csv"):

        return jsonify({
            "error":
                "El archivo debe tener formato CSV."
        }), 400


    # ========================================================
    # 2. LEER CSV
    # ========================================================

    try:

        df = pd.read_csv(file)

    except Exception as error:

        return jsonify({
            "error":
                (
                    "No fue posible leer el CSV: "
                    f"{str(error)}"
                )
        }), 400


    # ========================================================
    # 3. VALIDAR COLUMNAS
    # ========================================================

    required_columns = [
        "Order_ID",
        "Order_Time",
        "Weather",
        "Traffic",
        "Area"
    ]


    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]


    if missing_columns:

        return jsonify({
            "error":
                "Faltan columnas obligatorias.",

            "missing_columns":
                missing_columns

        }), 400


    # ========================================================
    # 4. LIMPIAR DATOS DE TEXTO
    # ========================================================

    text_columns = [
        "Weather",
        "Traffic",
        "Vehicle",
        "Area",
        "Category"
    ]


    for column in text_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )


    # ========================================================
    # 5. OBTENER HORA DEL PEDIDO
    # ========================================================

    df["Order_Hour"] = pd.to_datetime(
        df["Order_Time"],
        format="%H:%M:%S",
        errors="coerce"
    ).dt.hour


    # ========================================================
    # 6. CONVERTIR A LISTA
    # ========================================================

    shipments = df.to_dict(
        orient="records"
    )


    # ========================================================
    # 7. CALCULAR PRIORITY SCORE
    # ========================================================

    start_priority = time.perf_counter()


    processed_shipments = (
        calculate_priorities(
            shipments
        )
    )


    end_priority = time.perf_counter()


    priority_time = (
        end_priority -
        start_priority
    )


    # ========================================================
    # 8. ORDENAR CON MERGE SORT
    # ========================================================

    start_sort = time.perf_counter()


    sorted_shipments = merge_sort(
        processed_shipments
    )


    end_sort = time.perf_counter()


    merge_sort_time = (
        end_sort -
        start_sort
    )


    # ========================================================
    # 9. CREAR DATAFRAME
    # ========================================================

    result_df = pd.DataFrame(
        sorted_shipments
    )


    # ========================================================
    # 10. GUARDAR CSV PRIORIZADO
    # ========================================================

    PROCESSED_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )


    result_df.to_csv(
        PRIORITIZED_FILE,
        index=False
    )


    # ========================================================
    # 11. DISTRIBUCIÓN DE PRIORIDADES
    # ========================================================

    priority_distribution = (
        result_df[
            "Priority_Level"
        ]
        .value_counts()
        .to_dict()
    )


    # ========================================================
    # 12. TOP 10
    # ========================================================

    top_shipments = []


    for shipment in sorted_shipments[:10]:

        top_shipments.append({

            "Order_ID":
                shipment.get(
                    "Order_ID"
                ),

            "Priority_Score":
                shipment.get(
                    "Priority_Score"
                ),

            "Priority_Level":
                shipment.get(
                    "Priority_Level"
                ),

            "Traffic":
                shipment.get(
                    "Traffic"
                ),

            "Weather":
                shipment.get(
                    "Weather"
                ),

            "Area":
                shipment.get(
                    "Area"
                ),

            "Order_Hour":
                shipment.get(
                    "Order_Hour"
                )
        })


    # ========================================================
    # 13. RESPUESTA
    # ========================================================

    return jsonify({

        "total_shipments":
            len(sorted_shipments),

        "processing_time": {

            "priority_score":
                round(
                    priority_time,
                    6
                ),

            "merge_sort":
                round(
                    merge_sort_time,
                    6
                )
        },

        "priority_distribution":
            priority_distribution,

        "top_shipments":
            top_shipments

    })


# ============================================================
# DESCARGAR CSV PRIORIZADO
# ============================================================

@main.route(
    "/download",
    methods=["GET"]
)
def download_file():

    # ========================================================
    # VERIFICAR QUE EXISTA
    # ========================================================

    if not PRIORITIZED_FILE.exists():

        return jsonify({

            "error":
                "No existe un archivo priorizado."

        }), 404


    # ========================================================
    # DESCARGAR ARCHIVO
    # ========================================================

    return send_file(

        PRIORITIZED_FILE,

        as_attachment=True,

        download_name=
            "amazon_delivery_prioritized.csv",

        mimetype="text/csv"
    )