import numpy as np
import matplotlib.pyplot as plt
import os


def calcular_diagramas(longitud, cargas, RA, RB, puntos=500):
    """
    Calcula los diagramas de cortante y momento
    para un eje simplemente apoyado.

    cargas = [(posicion, fuerza), ...]
    """

    x = np.linspace(0, longitud, puntos)

    cortante = np.zeros_like(x)
    momento = np.zeros_like(x)

    for i, xi in enumerate(x):

        V = RA
        M = RA * xi

        for posicion, fuerza in cargas:

            if xi >= posicion:
                V += fuerza
                M += fuerza * (xi - posicion)

        if xi >= longitud:
            V += RB

        cortante[i] = V
        momento[i] = M

    return x, cortante, momento


def crear_grafica(
    x,
    y,
    titulo,
    ylabel
):

    fig, ax = plt.subplots()

    ax.plot(x, y)

    ax.axhline(
        0,
        linewidth=0.8
    )

    ax.fill_between(
        x,
        y,
        0,
        alpha=0.15
    )

    ax.set_xlabel(
        "Posición a lo largo del eje [m]"
    )

    ax.set_ylabel(
        ylabel
    )

    ax.set_title(
        titulo
    )

    ax.grid(True)

    fig.tight_layout()

    return fig


def guardar_grafica(
    fig,
    nombre
):

    os.makedirs(
        "resultados",
        exist_ok=True
    )

    ruta = os.path.join(
        "resultados",
        nombre
    )

    fig.savefig(
        ruta,
        dpi=300,
        bbox_inches="tight"
    )

    return ruta