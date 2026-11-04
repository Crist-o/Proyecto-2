import math
import statistics
from typing import List, Tuple


# Funciones existentes previamente


def moda(values: List[float]) -> float:
    """Devuelve la moda (el valor que más se repite) de una lista de números."""
    if not values:
        raise ValueError("La lista no puede estar vacía")
    return statistics.mode(values)


def volumen_paralelepipedo(largo: float, ancho: float, alto: float) -> float:
    """Calcula el volumen de un paralelepípedo multiplicando largo * ancho * alto."""
    return largo * ancho * alto