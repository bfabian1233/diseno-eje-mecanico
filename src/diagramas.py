import numpy as np
import matplotlib.pyplot as plt
import os


def calcular_diagramas(longitud, cargas, RA, RB, puntos=500):

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


def graficar_diagramas(x, cortante, momento):

    os.makedirs("resultados", exist_ok=True)

    # Cortante
    plt.figure()
    plt.plot(x, cortante)
    plt.axhline(0)
    plt.xlabel("Posición [m]")
    plt.ylabel("Fuerza cortante [N]")
    plt.title("Diagrama de fuerza cortante")
    plt.grid()

    plt.savefig(
        "resultados/cortante.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    # Momento
    plt.figure()
    plt.plot(x, momento)
    plt.axhline(0)
    plt.xlabel("Posición [m]")
    plt.ylabel("Momento flector [N·m]")
    plt.title("Diagrama de momento flector")
    plt.grid()

    plt.savefig(
        "resultados/momento.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()