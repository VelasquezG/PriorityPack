
"""Lectura y validación de archivos CSV para PriorityPack."""

import pandas as pd


REQUIRED_COLUMNS = [
    "Order_ID",
    "Order_Time",
    "Weather",
    "Traffic",
    "Area",
]

TEXT_COLUMNS = [
    "Weather",
    "Traffic",
    "Vehicle",
    "Area",
    "Category",
]


class CSVValidationError(ValueError):
    """Error controlado cuando el CSV no cumple los requisitos."""


def read_shipments_csv(file) -> pd.DataFrame:
    """Lee, valida y prepara los registros de envíos."""

    try:
        df = pd.read_csv(file)
    except pd.errors.EmptyDataError as error:
        raise CSVValidationError(
            "El archivo CSV está vacío."
        ) from error
    except (pd.errors.ParserError, UnicodeDecodeError) as error:
        raise CSVValidationError(
            "No fue posible leer el archivo. Verifica que sea un CSV válido."
        ) from error
    except Exception as error:
        raise CSVValidationError(
            "Ocurrió un error al leer el archivo CSV."
        ) from error

    if df.empty:
        raise CSVValidationError(
            "El archivo CSV no contiene registros para procesar."
        )

    # Normalizar nombres de columnas.
    df.columns = df.columns.astype(str).str.strip()

    if df.columns.duplicated().any():
        duplicated = df.columns[df.columns.duplicated()].tolist()
        raise CSVValidationError(
            "Hay encabezados duplicados: " + ", ".join(duplicated) + "."
        )

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise CSVValidationError(
            "Faltan columnas obligatorias: "
            + ", ".join(missing_columns)
            + "."
        )

    # Limpiar espacios sin convertir los valores nulos en "nan".
    for column in TEXT_COLUMNS:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip()
            df[column] = df[column].replace("", pd.NA)

    # Las horas inválidas quedan como valores faltantes.
    parsed_time = pd.to_datetime(
        df["Order_Time"].astype("string").str.strip(),
        format="%H:%M:%S",
        errors="coerce",
    )

    df["Order_Hour"] = parsed_time.dt.hour.astype("Int64")

    return df
