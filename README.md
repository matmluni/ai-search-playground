# Trabajo Parcial - Agentes de Búsqueda (UCS vs A*)

Comparación entre **búsqueda no informada (UCS)** y **búsqueda informada (A\*)**
sobre un mapa de videojuego generado de forma procedural.

## Requisitos

- Python 3.9 o superior
- Librerías: `numpy`, `matplotlib`

Instalación:

```bash
pip install numpy matplotlib
```

## Cómo correrlo

```bash
python3 main.py
```

Esto genera:

- `mapa_inicial.png` — Mapa con inicio y meta
- `resultado_ucs.png` — Camino encontrado por UCS
- `resultado_astar.png` — Camino encontrado por A\*

Y muestra en consola una tabla comparativa con nodos expandidos,
costo del camino y tiempo de ejecución.

## Estructura

| Archivo | Qué hace |
|---------|----------|
| `mapa.py` | Genera el mapa procedural y define los tipos de terreno |
| `algoritmos.py` | Implementa UCS y A\* |
| `main.py` | Orquesta la ejecución y genera las imágenes |

## Configuración

En `mapa.py` se pueden ajustar:

- `FILAS`, `COLUMNAS`: tamaño del mapa (≥ 100)
- `SEED`: semilla aleatoria (cambia para obtener otro mapa)
