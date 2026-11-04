"""Módulo para el manejo persistente de datos en formato CSV."""

import csv
from pathlib import Path

from grafo import Grafo


def guardar_conexion(
    ruta_archivo: Path,
    origen: str,
    destino: str,
    peso: float,
    medio: str,
) -> None:
    """Guarda una conexión con medio de transporte en el CSV (append)."""
    existe_archivo = ruta_archivo.exists()
    try:
        with open(
            ruta_archivo, mode="a", newline="", encoding="utf-8"
        ) as archivo:
            escritor = csv.writer(archivo)
            if not existe_archivo:
                escritor.writerow(
                    ["Origen", "Destino", "Peso", "Medio_Transporte"]
                )
            escritor.writerow([origen, destino, f"{peso:.1f}", medio])
    except IOError as error:
        msg = f"Error al escribir en {ruta_archivo}: {error}"
        raise IOError(msg) from error


def cargar_grafo_desde_csv(ruta_archivo: Path) -> Grafo:
    """Carga los nodos y conexiones desde el CSV e instancia el grafo."""
    grafo = Grafo()
    if not ruta_archivo.exists():
        return grafo

    try:
        with open(
            ruta_archivo, mode="r", encoding="utf-8"
        ) as archivo:
            lector = csv.DictReader(archivo)
            for num_linea, fila in enumerate(lector, start=2):
                try:
                    origen = fila["Origen"].strip().upper()
                    destino = fila["Destino"].strip().upper()
                    peso = float(fila["Peso"])
                    medio = fila.get(
                        "Medio_Transporte", "INDEFINIDO"
                    ).strip().upper()

                    if peso <= 0:
                        print(
                            f"Advertencia: Línea {num_linea} "
                            "omitida por peso <= 0."
                        )
                        continue
                    grafo.agregar_arista(origen, destino, peso, medio)
                except KeyError as error_clave:
                    print(
                        f"Advertencia: Línea {num_linea} omitida, "
                        f"falta la columna {error_clave}."
                    )
                except ValueError as error_valor:
                    print(
                        f"Advertencia: Línea {num_linea} omitida "
                        f"por datos corruptos: {error_valor}."
                    )
    except FileNotFoundError:
        print(f"El archivo {ruta_archivo} no existe todavía.")
    except IOError as error_io:
        print(f"Error de lectura en el archivo {ruta_archivo}: {error_io}")

    return grafo