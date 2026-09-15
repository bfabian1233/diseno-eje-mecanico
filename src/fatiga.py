import math


def limite_fatiga_base(Sut_MPa):
    """
    Límite de fatiga no modificado Se'
    para acero.
    """

    if Sut_MPa <= 0:
        raise ValueError("Sut debe ser mayor que cero.")

    if Sut_MPa <= 1400:
        return 0.5 * Sut_MPa

    return 700.0

def factor_superficie(Sut_MPa, acabado):

    acabados = {
        "rectificado": (1.58, -0.085),
        "maquinado": (4.51, -0.265),
        "laminado": (57.7, -0.718),
        "forjado": (272.0, -0.995)
    }

    if acabado not in acabados:
        raise ValueError("Acabado superficial no válido.")

    a, b = acabados[acabado]

    return a * Sut_MPa**b

def factor_tamano(d_mm):

    if d_mm <= 0:
        raise ValueError("El diámetro debe ser mayor que cero.")

    if d_mm <= 2.79:
        return 1.0

    if d_mm <= 51:
        return 1.24 * d_mm**(-0.107)

    if d_mm <= 254:
        return 1.51 * d_mm**(-0.157)

    raise ValueError(
        "Diámetro fuera del rango implementado."
    )

def factor_confiabilidad(confiabilidad):

    valores = {
        50: 1.000,
        90: 0.897,
        95: 0.868,
        99: 0.814,
        99.9: 0.753,
        99.99: 0.702
    }

    if confiabilidad not in valores:
        raise ValueError(
            "Confiabilidad no disponible."
        )

    return valores[confiabilidad]

def limite_fatiga_modificado(
    Sut_MPa,
    d_mm,
    acabado,
    confiabilidad
):

    Se_prime = limite_fatiga_base(Sut_MPa)

    ka = factor_superficie(
        Sut_MPa,
        acabado
    )

    kb = factor_tamano(
        d_mm
    )

    kc = 1.0
    kd = 1.0

    ke = factor_confiabilidad(
        confiabilidad
    )

    k_misc = 1.0

    Se = (
        Se_prime
        * ka
        * kb
        * kc
        * kd
        * ke
        * k_misc
    )

    return {
        "Se_prime": Se_prime,
        "ka": ka,
        "kb": kb,
        "kc": kc,
        "kd": kd,
        "ke": ke,
        "Se": Se
    }

def esfuerzos_fatiga(
    M,
    T,
    d_m,
    Kf=1.0,
    Kfs=1.0
):

    # Flexión alternante
    sigma_a = (
        Kf
        * 32
        * abs(M)
        / (math.pi * d_m**3)
    ) / 1e6

    # Flexión media
    sigma_m = 0.0

    # Torsión alternante
    tau_a = 0.0

    # Torque constante -> esfuerzo medio
    tau_m = (
        Kfs
        * 16
        * abs(T)
        / (math.pi * d_m**3)
    ) / 1e6

    sigma_a_eq = math.sqrt(
        sigma_a**2
        + 3 * tau_a**2
    )

    sigma_m_eq = math.sqrt(
        sigma_m**2
        + 3 * tau_m**2
    )

    return {
        "sigma_a": sigma_a,
        "sigma_m": sigma_m,
        "tau_a": tau_a,
        "tau_m": tau_m,
        "sigma_a_eq": sigma_a_eq,
        "sigma_m_eq": sigma_m_eq
    }

def factor_seguridad_goodman(
    sigma_a_eq,
    sigma_m_eq,
    Se_MPa,
    Sut_MPa
):

    termino = (
        sigma_a_eq / Se_MPa
        + sigma_m_eq / Sut_MPa
    )

    if termino <= 0:
        return float("inf")

    return 1 / termino