
# app/routes.py

import time
from pathlib import Path

import pandas as pd

from flask import Blueprint, render_template, request, jsonify, send_file

from app.services.priority_service import calculate_priorities
from app.services.csv_service import CSVValidationError, read_shipments_csv
from app.services.analysis_service import benchmark_algorithms
from app.services.complexity_service import get_complexity_analysis
from app.algorithms.merge_sort import merge_sort


main = Blueprint("main", __name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = PROJECT_ROOT / "data"
PROCESSED_DIRECTORY = DATA_DIRECTORY / "processed"

PRIORITIZED_FILE = PROCESSED_DIRECTORY / "amazon_delivery_prioritized.csv"
SCORED_UNSORTED_FILE = PROCESSED_DIRECTORY / "amazon_delivery_scored_unsorted.csv"


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# ============================================================
# PROCESAR ARCHIVO CSV
# ============================================================

@main.route("/process", methods=["POST"])
def process_file():
    if "file" not in request.files:
        return jsonify({"error": "No se recibió ningún archivo."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No se seleccionó ningún archivo."}), 400

    if not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "El archivo debe tener formato CSV."}), 400

    try:
        df = read_shipments_csv(file)
    except CSVValidationError as error:
        return jsonify({"error": str(error)}), 400

    shipments = df.to_dict(orient="records")

    start_priority = time.perf_counter()
    processed_shipments = calculate_priorities(shipments)
    priority_time = time.perf_counter() - start_priority

    # Guardar los registros puntuados, pero todavía sin ordenar.
    # El benchmark utiliza la misma entrada para ambos algoritmos.
    PROCESSED_DIRECTORY.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(processed_shipments).to_csv(
        SCORED_UNSORTED_FILE,
        index=False,
    )

    start_sort = time.perf_counter()
    sorted_shipments = merge_sort(processed_shipments)
    merge_sort_time = time.perf_counter() - start_sort

    result_df = pd.DataFrame(sorted_shipments)
    result_df.to_csv(PRIORITIZED_FILE, index=False)

    priority_distribution = (
        result_df["Priority_Level"].value_counts().to_dict()
    )

    top_shipments = [
        {
            "Order_ID": shipment.get("Order_ID"),
            "Priority_Score": shipment.get("Priority_Score"),
            "Priority_Level": shipment.get("Priority_Level"),
            "Traffic": shipment.get("Traffic"),
            "Weather": shipment.get("Weather"),
            "Area": shipment.get("Area"),
            "Order_Hour": shipment.get("Order_Hour"),
        }
        for shipment in sorted_shipments[:10]
    ]

    return jsonify({
        "total_shipments": len(sorted_shipments),
        "processing_time": {
            "priority_score": round(priority_time, 6),
            "merge_sort": round(merge_sort_time, 6),
        },
        "priority_distribution": priority_distribution,
        "top_shipments": top_shipments,
    })


# ============================================================
# DESCARGAR CSV PRIORIZADO
# ============================================================

@main.route("/download", methods=["GET"])
def download_file():
    if not PRIORITIZED_FILE.exists():
        return jsonify({
            "error": "No existe un archivo priorizado."
        }), 404

    return send_file(
        PRIORITIZED_FILE,
        as_attachment=True,
        download_name="amazon_delivery_prioritized.csv",
        mimetype="text/csv",
    )


# ============================================================
# COMPARACIÓN EXPERIMENTAL DE ALGORITMOS
# ============================================================

@main.route("/benchmark", methods=["GET"])
def benchmark():
    # Utilizar los registros puntuados sin ordenar para comparar
    # ambos algoritmos con la misma entrada.
    if not SCORED_UNSORTED_FILE.exists():
        return jsonify({
            "error": "Primero debes procesar un archivo CSV."
        }), 400

    try:
        df = pd.read_csv(SCORED_UNSORTED_FILE)

        if "Priority_Score" not in df.columns:
            return jsonify({
                "error": "El archivo no contiene Priority_Score."
            }), 400

        shipments = df.to_dict(orient="records")

        if not shipments:
            return jsonify({
                "error": "No hay registros para comparar."
            }), 400

        candidate_sizes = [100, 500, 1000, 2000, 5000]

        test_sizes = [
            size
            for size in candidate_sizes
            if size <= len(shipments)
        ]

        if not test_sizes:
            test_sizes = [len(shipments)]

        results = benchmark_algorithms(
            shipments,
            test_sizes=test_sizes,
        )

        return jsonify({
            "total_shipments": len(shipments),
            "benchmark_results": results,
        })

    except (OSError, ValueError, KeyError) as error:
        return jsonify({
            "error": (
                f"No fue posible ejecutar el benchmark: {error}"
            )
        }), 400


# ============================================================
# ANÁLISIS TEÓRICO DE COMPLEJIDAD
# ============================================================

@main.route("/complexity", methods=["GET"])
def complexity():
    """
    Devuelve el análisis teórico de complejidad de Merge Sort
    y Bubble Sort, incluyendo la aplicación del Teorema Maestro.
    """
    return jsonify(get_complexity_analysis())
