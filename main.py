"""
main.py
-------
Programa principal:
  1. Genera el mapa.
  2. Elige inicio y meta validos.
  3. Ejecuta UCS y A*.
  4. Imprime tabla comparativa y guarda imagenes.

Para cambiar el TAMANO del mapa: modifica FILAS y COLUMNAS en mapa.py
Para cambiar el MAPA generado:  modifica SEED en mapa.py
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

from mapa import (generar_mapa, es_obstaculo, COLORES,
                  LLANURA, BOSQUE, MONTANIA, AGUA,
                  FILAS, COLUMNAS, SEED)
from algoritmos import ucs, a_estrella


SEED_PUNTOS = 7   # semilla para inicio y meta (cambia para otros puntos)


def elegir_inicio_y_meta(mapa, seed=SEED_PUNTOS):
    """Elige dos puntos transitables alejados entre si."""
    rng = np.random.default_rng(seed)
    filas, columnas = mapa.shape

    # Distancia minima entre inicio y meta para que el camino sea interesante
    distancia_minima = min(filas, columnas) * 0.6

    while True:
        inicio = (int(rng.integers(0, filas)), int(rng.integers(0, columnas)))
        meta = (int(rng.integers(0, filas)), int(rng.integers(0, columnas)))
        dist = abs(inicio[0]-meta[0]) + abs(inicio[1]-meta[1])
        if (not es_obstaculo(mapa[inicio])
                and not es_obstaculo(mapa[meta])
                and dist > distancia_minima):
            return inicio, meta


def dibujar(mapa, inicio, meta, camino=None, expandidos=None,
            titulo="", archivo="salida.png"):
    """Pinta el mapa con terrenos, camino y nodos expandidos."""
    cmap = ListedColormap([COLORES[LLANURA], COLORES[BOSQUE],
                           COLORES[MONTANIA], COLORES[AGUA]])

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(mapa, cmap=cmap, vmin=0, vmax=3)
    ax.set_title(titulo)

    if expandidos:
        ys = [n[0] for n in expandidos]
        xs = [n[1] for n in expandidos]
        ax.scatter(xs, ys, c="white", s=2, alpha=0.3)

    if camino:
        ys = [c[0] for c in camino]
        xs = [c[1] for c in camino]
        ax.plot(xs, ys, color="red", linewidth=2)

    ax.scatter(inicio[1], inicio[0], c="lime", s=200, marker="o",
               edgecolors="black", zorder=5)
    ax.scatter(meta[1], meta[0], c="yellow", s=200, marker="*",
               edgecolors="black", zorder=5)

    parches = [
        Patch(color=COLORES[LLANURA],  label="Llanura (costo 1)"),
        Patch(color=COLORES[BOSQUE],   label="Bosque (costo 3)"),
        Patch(color=COLORES[MONTANIA], label="Montana (obstaculo)"),
        Patch(color=COLORES[AGUA],     label="Agua (obstaculo)"),
    ]
    ax.legend(handles=parches, loc="upper right", fontsize=8)
    ax.set_xticks([]); ax.set_yticks([])
    plt.tight_layout()
    plt.savefig(archivo, dpi=100, bbox_inches="tight")
    plt.close()
    print(f"  -> Guardado: {archivo}")


if __name__ == "__main__":
    # 1. Generar mapa
    print(f"Generando mapa procedural {FILAS}x{COLUMNAS} con seed={SEED}...")
    mapa = generar_mapa()
    print(f"  Tamano del mapa: {mapa.shape}")
    for nombre, val in [("Llanura", LLANURA), ("Bosque", BOSQUE),
                        ("Montana", MONTANIA), ("Agua", AGUA)]:
        pct = 100 * np.sum(mapa == val) / mapa.size
        print(f"  {nombre}: {pct:.2f}%")

    # 2. Elegir inicio y meta
    inicio, meta = elegir_inicio_y_meta(mapa)
    print(f"\nInicio: {inicio}")
    print(f"Meta:   {meta}")
    dibujar(mapa, inicio, meta, titulo="Mapa inicial",
            archivo="mapa_inicial.png")

    # 3. UCS
    print("\n--- UCS (no informada) ---")
    res_ucs = ucs(mapa, inicio, meta)
    print(f"  Costo: {res_ucs['costo']}")
    print(f"  Nodos expandidos: {res_ucs['expandidos']}")
    print(f"  Tiempo: {res_ucs['tiempo_ms']:.2f} ms")
    dibujar(mapa, inicio, meta,
            camino=res_ucs["camino"],
            expandidos=res_ucs["cerrados"],
            titulo=f"UCS: {res_ucs['expandidos']} nodos, costo {res_ucs['costo']}",
            archivo="resultado_ucs.png")

    # 4. A*
    print("\n--- A* (informada con Manhattan) ---")
    res_a = a_estrella(mapa, inicio, meta)
    print(f"  Costo: {res_a['costo']}")
    print(f"  Nodos expandidos: {res_a['expandidos']}")
    print(f"  Tiempo: {res_a['tiempo_ms']:.2f} ms")
    dibujar(mapa, inicio, meta,
            camino=res_a["camino"],
            expandidos=res_a["cerrados"],
            titulo=f"A*: {res_a['expandidos']} nodos, costo {res_a['costo']}",
            archivo="resultado_astar.png")

    # 5. Tabla comparativa
    print("\n" + "=" * 60)
    print(f"{'Algoritmo':<22}{'Expandidos':>12}{'Costo':>10}{'Tiempo(ms)':>14}")
    print("-" * 60)
    print(f"{'UCS':<22}{res_ucs['expandidos']:>12}{res_ucs['costo']:>10}{res_ucs['tiempo_ms']:>14.2f}")
    print(f"{'A* (Manhattan)':<22}{res_a['expandidos']:>12}{res_a['costo']:>10}{res_a['tiempo_ms']:>14.2f}")
    print("=" * 60)
