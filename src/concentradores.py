def calcular_factores_fatiga(Kt, Kts, q, qs):
    """
    Calcula los factores de concentración
    efectivos para fatiga.

    Kt  = concentración teórica en flexión
    Kts = concentración teórica en torsión
    q   = sensibilidad a la entalla en flexión
    qs  = sensibilidad a la entalla en torsión
    """

    if Kt < 1 or Kts < 1:
        raise ValueError(
            "Kt y Kts deben ser mayores o iguales a 1."
        )

    if not 0 <= q <= 1:
        raise ValueError(
            "q debe estar entre 0 y 1."
        )

    if not 0 <= qs <= 1:
        raise ValueError(
            "qs debe estar entre 0 y 1."
        )

    Kf = 1 + q * (Kt - 1)
    Kfs = 1 + qs * (Kts - 1)

    return Kf, Kfs