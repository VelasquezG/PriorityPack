
"""Pruebas de lectura y validación de archivos CSV para PriorityPack."""

from io import StringIO

import pandas as pd
import pytest

from app.services.csv_service import (
    CSVValidationError,
    read_shipments_csv,
)


def valid_csv():
    """Crea un CSV válido para las pruebas."""
    return StringIO(
        "Order_ID,Order_Time,Weather,Traffic,Area,Vehicle,Category\n"
        "ORDER001,12:30:00,Sunny,Low,Urban,Car,Electronics\n"
        "ORDER002,19:15:00,Fog,Jam,Semi-Urban,Truck,Food\n"
    )


def test_read_valid_csv():
    """Lee un CSV válido y verifica sus columnas y registros."""
    df = read_shipments_csv(valid_csv())

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "Order_Hour" in df.columns
    assert df.iloc[0]["Order_ID"] == "ORDER001"
    assert df.iloc[0]["Order_Hour"] == 12
    assert df.iloc[1]["Order_Hour"] == 19


def test_empty_csv():
    """Rechaza un archivo CSV completamente vacío."""
    with pytest.raises(CSVValidationError, match="vacío"):
        read_shipments_csv(StringIO(""))


def test_csv_without_records():
    """Rechaza un CSV que solo contiene encabezados."""
    csv_file = StringIO(
        "Order_ID,Order_Time,Weather,Traffic,Area\n"
    )

    with pytest.raises(CSVValidationError, match="no contiene registros"):
        read_shipments_csv(csv_file)


def test_missing_required_columns():
    """Rechaza un CSV al que le faltan columnas obligatorias."""
    csv_file = StringIO(
        "Order_ID,Weather,Traffic,Area\n"
        "ORDER001,Sunny,Low,Urban\n"
    )

    with pytest.raises(CSVValidationError, match="Faltan columnas obligatorias"):
        read_shipments_csv(csv_file)


def test_duplicate_columns():
    """Rechaza un CSV con encabezados duplicados."""
    csv_file = StringIO(
        "Order_ID,Order_Time,Weather,Traffic,Area,Area\n"
        "ORDER001,12:30:00,Sunny,Low,Urban,Urban\n"
    )

    with pytest.raises(CSVValidationError, match="encabezados duplicados"):
        read_shipments_csv(csv_file)


def test_invalid_order_time():
    """Convierte una hora inválida en un valor faltante."""
    csv_file = StringIO(
        "Order_ID,Order_Time,Weather,Traffic,Area\n"
        "ORDER001,hora-invalida,Sunny,Low,Urban\n"
    )

    df = read_shipments_csv(csv_file)

    assert pd.isna(df.iloc[0]["Order_Hour"])


def test_text_columns_are_trimmed():
    """Elimina espacios de los valores de texto."""
    csv_file = StringIO(
        "Order_ID,Order_Time,Weather,Traffic,Area\n"
        "ORDER001,12:30:00, Sunny , Low , Urban \n"
    )

    df = read_shipments_csv(csv_file)

    assert df.iloc[0]["Weather"] == "Sunny"
    assert df.iloc[0]["Traffic"] == "Low"
    assert df.iloc[0]["Area"] == "Urban"


def test_empty_text_becomes_missing():
    """Convierte los campos de texto vacíos en valores faltantes."""
    csv_file = StringIO(
        "Order_ID,Order_Time,Weather,Traffic,Area\n"
        "ORDER001,12:30:00,,Low,Urban\n"
    )

    df = read_shipments_csv(csv_file)

    assert pd.isna(df.iloc[0]["Weather"])


def test_invalid_csv_format():
    """Rechaza un archivo con una estructura CSV mal formada."""
    csv_file = StringIO(
        'Order_ID,Order_Time,Weather,Traffic,Area\n'
        '"ORDER001,12:30:00,Sunny,Low,Urban\n'
    )

    with pytest.raises(CSVValidationError, match="No fue posible leer"):
        read_shipments_csv(csv_file)
