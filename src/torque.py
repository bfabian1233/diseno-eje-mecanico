import math


def calcular_torque(potencia_kw, rpm):
    if potencia_kw <= 0:
        raise ValueError("La potencia debe ser mayor que cero.")

    if rpm <= 0:
        raise ValueError("Las RPM deben ser mayores que cero.")

    potencia_w = potencia_kw * 1000
    omega = 2 * math.pi * rpm / 60

    torque = potencia_w / omega

    return torque