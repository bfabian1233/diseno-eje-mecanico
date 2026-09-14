import math


def esfuerzo_flexion(M, d):
    return 32 * M / (math.pi * d**3)


def esfuerzo_torsion(T, d):
    return 16 * T / (math.pi * d**3)


def esfuerzo_von_mises(sigma, tau):
    return math.sqrt(sigma**2 + 3 * tau**2)


def factor_seguridad(Sy, sigma_vm):
    return Sy / sigma_vm