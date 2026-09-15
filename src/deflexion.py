import numpy as np
import math
import os
import matplotlib.pyplot as plt


def momento_inercia_eje(d):
    """
    Momento de inercia de área para un eje circular macizo.

    d = diámetro [m]
    """

    if d <= 0:
        raise ValueError(
            "El diámetro debe ser mayor que cero."
        )

    return math.pi * d**4 / 64


def integral_acumulada(x, y):
    """
    Integración numérica acumulada mediante
    la regla del trapecio.
    """

    resultado = np.zeros_like(y, dtype=float)

    for i in range(1, len(x)):

        dx = x[i] - x[i - 1]

        resultado[i] = (
            resultado[i - 1]
            + 0.5 * (y[i] + y[i - 1]) * dx
        )

    return resultado


def calcular_deflexion(
    x,
    momento,
    E,
    d
):
    """
    Calcula pendiente y deflexión de un eje
    simplemente apoyado.

    x       = posiciones [m]
    momento = momento flector [N·m]
    E       = módulo de elasticidad [Pa]
    d       = diámetro del eje [m]
    """

    I = momento_inercia_eje(d)

    # Curvatura
    curvatura = momento / (E * I)

    # Primera integración
    theta_base = integral_acumulada(
        x,
        curvatura
    )

    # Segunda integración
    y_base = integral_acumulada(
        x,
        theta_base
    )

    # Condiciones de frontera:
    # y(0) = 0
    # y(L) = 0

    L = x[-1]

    C1 = -y_base[-1] / L

    pendiente = theta_base + C1

    deflexion = y_base + C1 * x

    return pendiente, deflexion


def graficar_deformada(
    x,
    deflexion_resultante
):

    os.makedirs(
        "resultados",
        exist_ok=True
    )

    plt.figure()

    plt.plot(
        x,
        deflexion_resultante * 1000
    )

    plt.axhline(0)

    plt.xlabel("Posición en el eje [m]")
    plt.ylabel("Deflexión [mm]")
    plt.title("Deformada del eje")

    plt.grid()

    plt.savefig(
        "resultados/deflexion_eje.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()