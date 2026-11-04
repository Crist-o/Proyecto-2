"""Módulo POO para nodos, grafos y el algoritmo de Dijkstra."""

import heapq
from typing import Dict, List, Optional, Tuple


class Nodo:
    """Representa un nodo dentro de la red de transporte o lugares."""

    def __init__(self, nombre: str) -> None:
        """Inicializa el nodo con su nombre identificador."""
        self.nombre: str = nombre

    def __eq__(self, otro: object) -> bool:
        """Compara si dos nodos son iguales por su nombre."""
        if isinstance(otro, Nodo):
            return self.nombre == otro.nombre
        return False

    def __hash__(self) -> int:
        """Permite usar el nodo como clave en diccionarios y conjuntos."""
        return hash(self.nombre)

    def __repr__(self) -> str:
        """Representación textual del nodo."""
        return f"Nodo({self.nombre})"


class Grafo:
    """Representa un grafo ponderado no dirigido con medios de transporte."""

    def __init__(self) -> None:
        """Inicializa las estructuras internas del grafo."""
        self.nodos: Dict[str, Nodo] = {}
        # adyacencia: nodo -> vecino -> (peso, medio_transporte)
        self.adyacencia: Dict[Nodo, Dict[Nodo, Tuple[float, str]]] = {}

    def obtener_o_crear_nodo(self, nombre: str) -> Nodo:
        """Obtiene un nodo existente o crea uno nuevo si no existe."""
        if nombre not in self.nodos:
            nuevo_nodo = Nodo(nombre)
            self.nodos[nombre] = nuevo_nodo
            self.adyacencia[nuevo_nodo] = {}
        return self.nodos[nombre]

    def agregar_arista(
        self,
        origen_nombre: str,
        destino_nombre: str,
        peso: float,
        medio: str = "INDEFINIDO",
    ) -> None:
        """Agrega o actualiza una conexión bidireccional entre dos nodos."""
        origen = self.obtener_o_crear_nodo(origen_nombre)
        destino = self.obtener_o_crear_nodo(destino_nombre)

        self.adyacencia[origen][destino] = (peso, medio)
        self.adyacencia[destino][origen] = (peso, medio)

    def obtener_nodos(self) -> List[Nodo]:
        """Devuelve la lista de nodos presentes en el grafo."""
        return list(self.nodos.values())


class Dijkstra:
    """Clase encargada de calcular caminos mínimos mediante Dijkstra."""

    def __init__(self, grafo: Grafo) -> None:
        """Inicializa el algoritmo vinculándolo a una instancia de Grafo."""
        self.grafo: Grafo = grafo

    def calcular_camino_minimo(
        self, inicio_nombre: str, destino_nombre: str
    ) -> Tuple[List[Tuple[str, str, float]], float]:
        """Calcula la ruta más corta, los medios usados y el tiempo total."""
        if (
            inicio_nombre not in self.grafo.nodos
            or destino_nombre not in self.grafo.nodos
        ):
            return [], float("inf")

        inicio = self.grafo.nodos[inicio_nombre]
        destino = self.grafo.nodos[destino_nombre]

        distancias: Dict[Nodo, float] = {
            n: float("inf") for n in self.grafo.obtener_nodos()
        }
        previos: Dict[Nodo, Optional[Tuple[Nodo, str, float]]] = {
            n: None for n in self.grafo.obtener_nodos()
        }

        distancias[inicio] = 0.0
        cola: List[Tuple[float, str, Nodo]] = [(0.0, inicio.nombre, inicio)]

        while cola:
            dist_actual, _, nodo_actual = heapq.heappop(cola)

            if dist_actual > distancias[nodo_actual]:
                continue

            if nodo_actual == destino:
                break

            vecinos = self.grafo.adyacencia.get(nodo_actual, {})
            for vecino, (peso, medio) in vecinos.items():
                nueva_distancia = dist_actual + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    previos[vecino] = (nodo_actual, medio, peso)
                    heapq.heappush(
                        cola,
                        (nueva_distancia, vecino.nombre, vecino),
                    )

        distancia_total = distancias[destino]
        if distancia_total == float("inf"):
            return [], float("inf")

        # Reconstrucción de la ruta con detalles de transporte
        detalles_ruta: List[Tuple[str, str, float]] = []
        nodo_paso: Optional[Nodo] = destino

        while nodo_paso is not None and nodo_paso != inicio:
            info_prev = previos.get(nodo_paso)
            if info_prev is None:
                break
            padre, medio, peso_tramo = info_prev
            detalles_ruta.append((padre.nombre, medio, peso_tramo))
            nodo_paso = padre

        detalles_ruta.reverse()
        return detalles_ruta, distancia_total