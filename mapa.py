"""
mapa.py
-------
Genera un mapa N x M con 4 tipos de terreno.

Para CAMBIAR EL TAMANO del mapa, modifica las variables FILAS y COLUMNAS
mas abajo (deben ser >= 100 segun el enunciado).
"""
import numpy as np


# ============================================================
# CONFIGURACION GLOBAL DEL MAPA
# (cambia estos valores para experimentar con otros tamanos)
# ============================================================

FILAS = 120        # tamano del mapa (debe ser >= 100)
COLUMNAS = 120     # tamano del mapa (debe ser >= 100)
SEED = 42          # semilla aleatoria (cambia para obtener otro mapa)


# ============================================================
# CONSTANTES DE TERRENO
# Cada celda del mapa contiene uno de estos valores
# ============================================================

LLANURA  = 0       # transitable, costo bajo
BOSQUE   = 1       # transitable, costo alto
MONTANIA = 2       # OBSTACULO (no se puede cruzar)
AGUA     = 3       # OBSTACULO (no se puede cruzar)


# ============================================================
# PESOS (costos de moverse a cada tipo de celda)
# ============================================================

PESOS = {
    LLANURA: 1,    # moverse a llanura cuesta 1
    BOSQUE:  3,    # moverse a bosque cuesta 3 (mas dificil)
    # Montana y Agua no estan: son obstaculos
}


# ============================================================
# PROBABILIDADES (con que frecuencia aparece cada terreno)
# La suma debe ser 1.0
# ============================================================

PROBABILIDADES = {
    LLANURA:  0.40,    # 40% del mapa es llanura
    BOSQUE:   0.30,    # 30% es bosque
    MONTANIA: 0.15,    # 15% es montana
    AGUA:     0.15,    # 15% es agua
}


# ============================================================
# COLORES (para dibujar el mapa con matplotlib)
# ============================================================

COLORES = {
    LLANURA:  "#c8e6a0",   # verde claro
    BOSQUE:   "#2e7d32",   # verde oscuro
    MONTANIA: "#6d4c41",   # marron
    AGUA:     "#1976d2",   # azul
}


# ============================================================
# FUNCIONES
# ============================================================

def generar_mapa(filas=FILAS, columnas=COLUMNAS, seed=SEED):
    """
    Genera una matriz filas x columnas donde cada celda
    es LLANURA, BOSQUE, MONTANIA o AGUA elegido al azar
    segun las probabilidades definidas arriba.
    """
    rng = np.random.default_rng(seed)
    terrenos = [LLANURA, BOSQUE, MONTANIA, AGUA]
    probs = [PROBABILIDADES[t] for t in terrenos]
    return rng.choice(terrenos, size=(filas, columnas), p=probs)


def es_obstaculo(celda):
    """Devuelve True si la celda es MONTANIA o AGUA."""
    return celda == MONTANIA or celda == AGUA


def costo_de(celda):
    """Devuelve el costo (peso) de entrar a esa celda."""
    return PESOS.get(int(celda), float('inf'))
