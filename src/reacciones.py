def calcular_reacciones(longitud, cargas):
    """
    Calcula las reacciones en los apoyos A y B
    de un eje simplemente apoyado.

    cargas = [(posicion, fuerza), ...]

    Fuerza positiva: hacia arriba
    Fuerza negativa: hacia abajo
    """

    if longitud <= 0:
        raise ValueError("La longitud debe ser mayor que cero.")

    suma_fuerzas = sum(
        fuerza for posicion, fuerza in cargas
    )

    suma_momentos_A = sum(
        fuerza * posicion
        for posicion, fuerza in cargas
    )

    reaccion_B = -suma_momentos_A / longitud

    reaccion_A = -suma_fuerzas - reaccion_B

    return reaccion_A, reaccion_B