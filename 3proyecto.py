"""Script principal interactivo para la gestión de rutas y lugares."""

from pathlib import Path

from grafo import Dijkstra
from io_handler import cargar_grafo_desde_csv, guardar_conexion

ARCHIVO_DATOS = Path("nodos.csv")


def solicitar_nodo(mensaje: str) -> str:
    """Solicita el identificador de una ubicación o nodo."""
    while True:
        entrada = input(mensaje).strip().upper()
        if entrada:
            return entrada
        print("Error: El nombre del lugar no puede estar vacío.")


def solicitar_peso(mensaje: str) -> float:
    """Solicita un tiempo/peso válido capturando ValueError."""
    while True:
        try:
            texto_ingresado = input(mensaje)
            peso = float(texto_ingresado)
            if peso <= 0:
                print("Error: El peso debe ser mayor a 0.")
                continue
            return peso
        except ValueError:
            print("Error: Entrada inválida. Ingrese un flotante válido.")


def solicitar_medio(mensaje: str) -> str:
    """Solicita el medio de transporte para el traslado."""
    while True:
        entrada = input(mensaje).strip().upper()
        if entrada:
            return entrada
        print("Error: El medio de transporte no puede estar vacío.")


def registrar_nueva_conexion() -> None:
    """Captura interactiva y segura de nuevas conexiones para el CSV."""
    print("\n--- Registrar Nuevo Traslado ---")
    origen = solicitar_nodo("Ingrese la Ubicación de Origen: ")
    destino = solicitar_nodo("Ingrese la Ubicación de Destino: ")

    if origen == destino:
        print("Error: El origen y el destino no pueden ser iguales.")
        return

    peso = solicitar_peso("Ingrese el Tiempo en minutos (ej. 10.5): ")
    medio = solicitar_medio(
        "Ingrese el Medio de Transporte (AUTO, BICI, CAMION, TREN, etc.): "
    )

    try:
        guardar_conexion(ARCHIVO_DATOS, origen, destino, peso, medio)
        print(
            f"Éxito: Traslado '{origen} <-> {destino}' "
            f"({peso} min via {medio}) guardado."
        )
    except IOError as error:
        print(f"Error de persistencia: {error}")


def ejecutar_dijkstra_interactivo() -> None:
    """Carga el grafo desde el CSV y ejecuta la consulta de Dijkstra."""
    grafo = cargar_grafo_desde_csv(ARCHIVO_DATOS)
    nodos_disponibles = sorted(list(grafo.nodos.keys()))

    if not nodos_disponibles:
        print("\nEl archivo 'nodos.csv' está vacío o no existe.")
        print("Registre al menos una conexión antes de ejecutar Dijkstra.")
        return

    print(f"\nUbicaciones cargadas en memoria: {', '.join(nodos_disponibles)}")
    inicio = solicitar_nodo("Ingrese la Ubicación de Inicio: ")

    if inicio not in grafo.nodos:
        print(f"Error: La ubicación '{inicio}' no existe en la red.")
        return

    destino = solicitar_nodo("Ingrese la Ubicación de Destino: ")
    if destino not in grafo.nodos:
        print(f"Error: La ubicación '{destino}' no existe en la red.")
        return

    calculador = Dijkstra(grafo)
    detalles_ruta, tiempo_total = calculador.calcular_camino_minimo(
        inicio, destino
    )

    if tiempo_total == float("inf"):
        print(f"\nNo existe ruta disponible entre '{inicio}' y '{destino}'.")
        return

    print("\n================ RUTA ÓPTIMA ENCONTRADA ================")
    print(f"Punto de Partida: {inicio}")
    for origen_tramo, medio_tramo, peso_tramo in detalles_ruta:
        print(f"  └─> Usar [{medio_tramo}] ({peso_tramo:.1f} min)")
    print(f"Llegada: {destino}")
    print(f"Tiempo Total de Traslado: {tiempo_total:.1f} minutos")
    print("========================================================")


def menu_principal() -> None:
    """Presenta el menú principal del sistema de transporte urbano."""
    while True:
        print("\n=== SISTEMA DE RUTAS Y MEDIOS DE TRANSPORTE ===")
        print("1. Ingresar nuevo traslado (Guardar en CSV)")
        print("2. Cargar red y calcular ruta óptima (Dijkstra)")
        print("3. Salir")

        opcion = input("Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            registrar_nueva_conexion()
        elif opcion == "2":
            ejecutar_dijkstra_interactivo()
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione 1, 2 o 3.")


if __name__ == "__main__":
    menu_principal()