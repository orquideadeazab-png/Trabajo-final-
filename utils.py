"""
Utilidades de manejo de datos para SIAP.

Funciones para cargar y guardar el registro de estudiantes en CSV,
y para construir el DataFrame que alimenta el dashboard.
"""

from __future__ import annotations
import os
import pandas as pd

COLUMNAS = [
    "nombre",
    "grado",
    "pct_visual",
    "pct_auditivo",
    "pct_kinestesico",
    "estilo_dominante",
    "ritmo",
    "necesidad",
]


def cargar_estudiantes(ruta_csv: str) -> pd.DataFrame:
    """Carga el registro de estudiantes desde un CSV. Si no existe, crea uno vacío."""
    if os.path.exists(ruta_csv):
        return pd.read_csv(ruta_csv)
    return pd.DataFrame(columns=COLUMNAS)


def guardar_estudiantes(df: pd.DataFrame, ruta_csv: str) -> None:
    """Guarda el registro de estudiantes en un CSV."""
    os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)
    df.to_csv(ruta_csv, index=False)


def agregar_estudiante(df: pd.DataFrame, registro: dict) -> pd.DataFrame:
    """Agrega un nuevo estudiante (fila) al DataFrame y lo devuelve."""
    nuevo = pd.DataFrame([registro], columns=COLUMNAS)
    return pd.concat([df, nuevo], ignore_index=True)
