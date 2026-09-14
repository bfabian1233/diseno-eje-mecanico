import numpy as np

from src.torque import calcular_torque
from src.reacciones import calcular_reacciones
from src.diagramas import calcular_diagramas, graficar_diagramas


print("\n DISEÑO DE EJE MECÁNICO \n")


# DATOS DE ENTRADA

potencia = float(input("Potencia transmitida [kW]: "))

rpm = float(input("Velocidad de giro [rpm]: "))

longitud = float(input("Longitud del eje [m]: "))


# CÁLCULO DEL TORQUE

torque = calcular_torque(potencia,rpm)

print(f"\nTorque del eje: {torque:.2f} N·m")


# ==================================================
# CARGAS EN DOS PLANOS
# ==================================================

Fy = float(
    input("\nFuerza vertical Fy [N]: ")
)

Fz = float(
    input("Fuerza horizontal Fz [N]: ")
)

posicion = float(
    input("Posición de la carga desde el apoyo A [m]: ")
)

cargas_y = [
    (posicion, -abs(Fy))
]

cargas_z = [
    (posicion, -abs(Fz))
]


# ==================================================
# REACCIONES
# ==================================================

RA_y, RB_y = calcular_reacciones(
    longitud,
    cargas_y
)

RA_z, RB_z = calcular_reacciones(
    longitud,
    cargas_z
)

print("\n=== REACCIONES PLANO Y ===")
print(f"RA_y: {RA_y:.2f} N")
print(f"RB_y: {RB_y:.2f} N")

print("\n=== REACCIONES PLANO Z ===")
print(f"RA_z: {RA_z:.2f} N")
print(f"RB_z: {RB_z:.2f} N")


# ==================================================
# DIAGRAMAS
# ==================================================

x, cortante_y, momento_y = calcular_diagramas(
    longitud,
    cargas_y,
    RA_y,
    RB_y
)

x, cortante_z, momento_z = calcular_diagramas(
    longitud,
    cargas_z,
    RA_z,
    RB_z
)


# ==================================================
# MOMENTO RESULTANTE
# ==================================================

momento_resultante = np.sqrt(
    momento_y**2 + momento_z**2
)

M_max = np.max(
    np.abs(momento_resultante)
)

print(
    f"\nMomento flector resultante máximo: "
    f"{M_max:.2f} N·m"
)
