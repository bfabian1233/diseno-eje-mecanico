import math


def esfuerzo_flexion(M, d, Kt=1.0):

    return (
        Kt
        * 32
        * M
        / (math.pi * d**3)
    )


def esfuerzo_torsion(T, d, Kts=1.0):

    return (
        Kts
        * 16
        * T
        / (math.pi * d**3)
    )


def esfuerzo_von_mises(sigma, tau):
    return math.sqrt(sigma**2 + 3 * tau**2)


def factor_seguridad(Sy, sigma_vm):
    return Sy / sigma_vm

def diametro_minimo(
    M,
    T,
    Sy,
    n,
    Kt=1.0,
    Kts=1.0
):

    termino = math.sqrt(
        4 * (Kt * M)**2
        + 3 * (Kts * T)**2
    )

    d = (
        (16 * n * termino)
        / (math.pi * Sy)
    ) ** (1 / 3)

    return d

def seleccionar_diametro_comercial(d_mm):

    diametros_comerciales = [
        10, 12, 15, 16, 18, 20,
        22, 25, 28, 30, 32, 35,
        38, 40, 45, 50, 55, 60,
        65, 70, 75, 80
    ]

    for diametro in diametros_comerciales:
        if diametro >= d_mm:
            return diametro

    raise ValueError(
        "El diámetro calculado supera el rango comercial definido."
    )