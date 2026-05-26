"""
algoritmos.py
-------------
Implementacion de UCS y A* siguiendo Russell & Norvig.

IDEA CLAVE:
    UCS y A* son el MISMO algoritmo.
    Lo unico que cambia es como se ordena la cola de prioridad:
        UCS:  por g(n)            (costo acumulado)
        A* :  por g(n) + h(n)     (costo acumulado + heuristica)

Las constantes (LLANURA, BOSQUE, MONTANIA, AGUA) y los pesos
estan definidos en mapa.py.
"""
import heapq
import time
from mapa import es_obstaculo, costo_de


# ============================================================
# Funciones auxiliares
# ============================================================

def obtener_vecinos(nodo, mapa):
    """
    Devuelve los vecinos transitables (N, S, E, O) del nodo,
    junto con el costo de entrar a cada uno.
    """
    i, j = nodo
    filas, columnas = mapa.shape
    vecinos = []

    # Cuatro direcciones: arriba (-1,0), abajo (1,0), derecha (0,1), izquierda (0,-1)
    for di, dj in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
        ni, nj = i + di, j + dj
        # Que este dentro del mapa Y que no sea obstaculo
        if 0 <= ni < filas and 0 <= nj < columnas:
            if not es_obstaculo(mapa[ni, nj]):
                vecinos.append(((ni, nj), costo_de(mapa[ni, nj])))

    return vecinos


def reconstruir_camino(padres, meta):
    """Reconstruye el camino siguiendo el diccionario 'padres' hacia atras."""
    camino = [meta]
    while padres[camino[-1]] is not None:
        camino.append(padres[camino[-1]])
    camino.reverse()
    return camino


def manhattan(a, b):
    """
    Heuristica: distancia Manhattan.
    Es admisible porque nunca sobreestima el costo real
    (el costo minimo de moverse a una celda es 1, llanura).
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ============================================================
# UCS - Busqueda de Costo Uniforme
# Russell & Norvig, capitulo 3.
# Expande siempre el nodo de menor g(n).
# ============================================================
def ucs(mapa, inicio, meta):
    t0 = time.perf_counter()

    # Estructuras
    frontera = [(0, inicio)]      # cola de prioridad: (costo, nodo)
    g = {inicio: 0}               # mejor costo conocido a cada nodo
    padres = {inicio: None}       # de quien viene cada nodo
    explorados = set()            # nodos ya procesados
    expandidos = 0                # contador

    while frontera:
        # 1. Sacamos el nodo con menor g
        costo_actual, nodo = heapq.heappop(frontera)

        # 2. Si ya lo procesamos, lo saltamos
        if nodo in explorados:
            continue

        # 3. Si es la meta, terminamos
        if nodo == meta:
            return _resultado(padres, meta, costo_actual,
                              expandidos, explorados, t0)

        # 4. Lo marcamos como explorado
        explorados.add(nodo)
        expandidos += 1

        # 5. Expandimos sus vecinos
        for vecino, costo_paso in obtener_vecinos(nodo, mapa):
            nuevo_g = costo_actual + costo_paso

            # Si encontramos un camino mas barato al vecino, lo guardamos
            if nuevo_g < g.get(vecino, float('inf')):
                g[vecino] = nuevo_g
                padres[vecino] = nodo
                heapq.heappush(frontera, (nuevo_g, vecino))

    # No hay camino
    return _resultado(padres, None, float('inf'),
                      expandidos, explorados, t0)


# ============================================================
# A* - Busqueda Informada
# Russell & Norvig, capitulo 4.
# Identico a UCS pero ordena por f(n) = g(n) + h(n).
# ============================================================
def a_estrella(mapa, inicio, meta):
    t0 = time.perf_counter()

    # Estructuras (igual que UCS, salvo que la cola lleva f en vez de g)
    f_inicio = 0 + manhattan(inicio, meta)
    frontera = [(f_inicio, inicio)]
    g = {inicio: 0}
    padres = {inicio: None}
    explorados = set()
    expandidos = 0

    while frontera:
        # 1. Sacamos el nodo con menor f
        _, nodo = heapq.heappop(frontera)

        # 2. Si ya lo procesamos, lo saltamos
        if nodo in explorados:
            continue

        # 3. Si es la meta, terminamos
        if nodo == meta:
            return _resultado(padres, meta, g[meta],
                              expandidos, explorados, t0)

        # 4. Lo marcamos como explorado
        explorados.add(nodo)
        expandidos += 1

        # 5. Expandimos sus vecinos
        for vecino, costo_paso in obtener_vecinos(nodo, mapa):
            nuevo_g = g[nodo] + costo_paso

            if nuevo_g < g.get(vecino, float('inf')):
                g[vecino] = nuevo_g
                padres[vecino] = nodo
                # ===== UNICA DIFERENCIA CON UCS =====
                # UCS:  heappush(frontera, (nuevo_g, vecino))
                # A* :  heappush(frontera, (nuevo_g + h, vecino))
                f = nuevo_g + manhattan(vecino, meta)
                heapq.heappush(frontera, (f, vecino))

    return _resultado(padres, None, float('inf'),
                      expandidos, explorados, t0)


# ============================================================
# Auxiliar para empaquetar el resultado
# ============================================================
def _resultado(padres, meta, costo, expandidos, explorados, t0):
    tiempo_ms = (time.perf_counter() - t0) * 1000
    camino = reconstruir_camino(padres, meta) if meta else []
    return {
        "camino": camino,
        "costo": costo,
        "expandidos": expandidos,
        "cerrados": explorados,
        "tiempo_ms": tiempo_ms,
    }
