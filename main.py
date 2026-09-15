import numpy as np
import matplotlib.pyplot as plt

from src.torque import calcular_torque
from src.reacciones import calcular_reacciones
from src.diagramas import (
    calcular_diagramas,
    crear_grafica,
    guardar_grafica
)
from src.esfuerzos import (
    esfuerzo_flexion,
    esfuerzo_torsion,
    esfuerzo_von_mises,
    factor_seguridad,
    diametro_minimo,
    seleccionar_diametro_comercial
)
from src.materiales import cargar_materiales, seleccionar_material
from src.fatiga import (limite_fatiga_modificado,esfuerzos_fatiga,factor_seguridad_goodman)
from src.concentradores import calcular_factores_fatiga
from src.deflexion import (calcular_deflexion,graficar_deformada)


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

print("\n REACCIONES PLANO Y ")
print(f"RA_y: {RA_y:.2f} N")
print(f"RB_y: {RB_y:.2f} N")

print("\n REACCIONES PLANO Z")
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

# ==================================================
# GRÁFICAS DE CORTANTE Y MOMENTO
# ==================================================

# Cortante plano Y
fig_cortante_y = crear_grafica(
    x,
    cortante_y,
    "Diagrama de cortante - Plano Y",
    "Fuerza cortante Vy [N]"
)

guardar_grafica(
    fig_cortante_y,
    "cortante_y.png"
)


# Momento plano Y
fig_momento_y = crear_grafica(
    x,
    momento_y,
    "Diagrama de momento flector - Plano Y",
    "Momento My [N·m]"
)

guardar_grafica(
    fig_momento_y,
    "momento_y.png"
)


# Cortante plano Z
fig_cortante_z = crear_grafica(
    x,
    cortante_z,
    "Diagrama de cortante - Plano Z",
    "Fuerza cortante Vz [N]"
)

guardar_grafica(
    fig_cortante_z,
    "cortante_z.png"
)


# Momento plano Z
fig_momento_z = crear_grafica(
    x,
    momento_z,
    "Diagrama de momento flector - Plano Z",
    "Momento Mz [N·m]"
)

guardar_grafica(
    fig_momento_z,
    "momento_z.png"
)


# Momento flector resultante
fig_resultante = crear_grafica(
    x,
    momento_resultante,
    "Momento flector resultante",
    "Momento resultante [N·m]"
)

guardar_grafica(
    fig_resultante,
    "momento_resultante.png"
)

print(
    "\nDiagramas de cortante y momento "
    "guardados en la carpeta 'resultados'."
)

plt.show()

# ==================================================
# CONCENTRACIÓN DE ESFUERZOS
# ==================================================

print("\n=== GEOMETRÍA DE LA SECCIÓN CRÍTICA ===")

print("1. Eje liso")
print("2. Escalón")
print("3. Chavetero")

tipo_geometria = int(
    input("Seleccione el tipo de geometría: ")
)

if tipo_geometria == 1:

    Kt = 1.0
    Kts = 1.0
    q = 1.0
    qs = 1.0

elif tipo_geometria in [2, 3]:

    Kt = float(
        input("Ingrese Kt para flexión: ")
    )

    Kts = float(
        input("Ingrese Kts para torsión: ")
    )

    q = float(
        input(
            "Sensibilidad a la entalla q [0-1]: "
        )
    )

    qs = float(
        input(
            "Sensibilidad a la entalla qs [0-1]: "
        )
    )

else:

    raise ValueError(
        "Tipo de geometría no válido."
    )

Kf, Kfs = calcular_factores_fatiga(
    Kt,
    Kts,
    q,
    qs
)

print("\n=== FACTORES DE CONCENTRACIÓN ===")

print(f"Kt  = {Kt:.3f}")
print(f"Kts = {Kts:.3f}")

print(f"Kf  = {Kf:.3f}")
print(f"Kfs = {Kfs:.3f}")

# ==================================================
# MOMENTO EN LA SECCIÓN CRÍTICA
# ==================================================

if tipo_geometria in [2, 3]:

    posicion_concentrador = float(
        input(
            "\nPosición del escalón/chavetero desde A [m]: "
        )
    )

    if (
        posicion_concentrador < 0
        or posicion_concentrador > longitud
    ):
        raise ValueError(
            "La posición del concentrador debe estar "
            "dentro de la longitud del eje."
        )

    M_concentrador = np.interp(
        posicion_concentrador,
        x,
        momento_resultante
    )

    print(
        f"Momento en la sección con concentrador: "
        f"{M_concentrador:.2f} N·m"
    )

    M_diseno = abs(M_concentrador)

else:

    # Para un eje liso usamos el momento máximo global
    M_diseno = M_max

# ==================================================
# DIMENSIONAMIENTO DEL EJE
# ==================================================

# ==================================================
# SELECCIÓN DEL MATERIAL
# ==================================================

materiales = cargar_materiales()

material = seleccionar_material(
    materiales
)

Sy_MPa = material["Sy_MPa"]
Sut_MPa = material["Sut_MPa"]
E_GPa = material["E_GPa"]

print(
    f"\nMaterial seleccionado: "
    f"{material['Material']}"
)

print(
    f"Condición: "
    f"{material['Condicion']}"
)

print(
    f"Sy = {Sy_MPa:.2f} MPa"
)

print(
    f"Sut = {Sut_MPa:.2f} MPa"
)

print(
    f"E = {E_GPa:.2f} GPa"
)

n = float(
    input("Factor de seguridad deseado: ")
)

# Convertir MPa a Pa
Sy = Sy_MPa * 1e6

d = diametro_minimo(
    M_diseno,
    torque,
    Sy,
    n,
    Kt,
    Kts
)

d_mm = d * 1000

print(
    f"\nDiámetro mínimo calculado: "
    f"{d_mm:.2f} mm"
)

diametro_comercial = seleccionar_diametro_comercial(
    d_mm
)

print(
    f"Diámetro comercial recomendado: "
    f"{diametro_comercial:.0f} mm"
)

# ==================================================
# VERIFICACIÓN DEL DIÁMETRO COMERCIAL
# ==================================================

d_comercial_m = diametro_comercial / 1000

sigma = esfuerzo_flexion(
    M_diseno,
    d_comercial_m,
    Kt
)

tau = esfuerzo_torsion(
    torque,
    d_comercial_m
)

sigma_vm = esfuerzo_von_mises(
    sigma,
    tau
)

n_real = factor_seguridad(
    Sy,
    sigma_vm
)

print("\nVERIFICACIÓN DEL DIÁMETRO COMERCIAL")

print(
    f"Esfuerzo de flexión: "
    f"{sigma / 1e6:.2f} MPa"
)

print(
    f"Esfuerzo cortante por torsión: "
    f"{tau / 1e6:.2f} MPa"
)

print(
    f"Esfuerzo equivalente de Von Mises: "
    f"{sigma_vm / 1e6:.2f} MPa"
)

print(
    f"Factor de seguridad real: "
    f"{n_real:.2f}"
)

# ==================================================
# ANÁLISIS DE DEFLEXIÓN
# ==================================================

print("\n ANÁLISIS DE DEFLEXIÓN")

E = E_GPa * 1e9

d_deflexion = diametro_comercial / 1000

pendiente_y, deflexion_y = calcular_deflexion(
    x,
    momento_y,
    E,
    d_deflexion
)

pendiente_z, deflexion_z = calcular_deflexion(
    x,
    momento_z,
    E,
    d_deflexion
)

deflexion_resultante = np.sqrt(
    deflexion_y**2
    + deflexion_z**2
)

pendiente_resultante = np.sqrt(
    pendiente_y**2
    + pendiente_z**2
)

indice_deflexion_max = np.argmax(
    deflexion_resultante
)

deflexion_max = deflexion_resultante[
    indice_deflexion_max
]

posicion_deflexion_max = x[
    indice_deflexion_max
]

pendiente_max = np.max(
    pendiente_resultante
)

print(
    f"Deflexión máxima: "
    f"{deflexion_max * 1000:.4f} mm"
)

print(
    f"Posición de deflexión máxima: "
    f"{posicion_deflexion_max:.4f} m"
)

print(
    f"Pendiente máxima: "
    f"{pendiente_max:.6f} rad"
)

graficar_deformada(
    x,
    deflexion_resultante
)

# ==================================================
# ANÁLISIS DE FATIGA
# ==================================================

print("\nANÁLISIS DE FATIGA")

print("\nAcabado superficial:")
print("1. Rectificado")
print("2. Maquinado")
print("3. Laminado en caliente")
print("4. Forjado")

opcion_acabado = int(
    input("Seleccione acabado: ")
)

acabados = {
    1: "rectificado",
    2: "maquinado",
    3: "laminado",
    4: "forjado"
}

if opcion_acabado not in acabados:
    raise ValueError(
        "Opción de acabado no válida."
    )

acabado = acabados[
    opcion_acabado
]

print("\nConfiabilidad:")
print("1. 90 %")
print("2. 95 %")
print("3. 99 %")
print("4. 99.9 %")

opcion_conf = int(
    input("Seleccione confiabilidad: ")
)

confiabilidades = {
    1: 90,
    2: 95,
    3: 99,
    4: 99.9
}

if opcion_conf not in confiabilidades:
    raise ValueError(
        "Opción de confiabilidad no válida."
    )

confiabilidad = confiabilidades[
    opcion_conf
]


fatiga_material = limite_fatiga_modificado(
    Sut_MPa,
    diametro_comercial,
    acabado,
    confiabilidad
)

Se = fatiga_material["Se"]

print("\n FACTORES DE MARIN")

print(
    f"Se' = "
    f"{fatiga_material['Se_prime']:.2f} MPa"
)

print(
    f"ka = "
    f"{fatiga_material['ka']:.3f}"
)

print(
    f"kb = "
    f"{fatiga_material['kb']:.3f}"
)

print(
    f"ke = "
    f"{fatiga_material['ke']:.3f}"
)

print(
    f"Se corregido = "
    f"{Se:.2f} MPa"
)

fatiga_esfuerzos = esfuerzos_fatiga(
    M_diseno,
    torque,
    d_comercial_m,
    Kf,
    Kfs
)

print("\nESFUERZOS DE FATIGA")

print(
    f"σa = "
    f"{fatiga_esfuerzos['sigma_a']:.2f} MPa"
)

print(
    f"σm = "
    f"{fatiga_esfuerzos['sigma_m']:.2f} MPa"
)

print(
    f"τa = "
    f"{fatiga_esfuerzos['tau_a']:.2f} MPa"
)

print(
    f"τm = "
    f"{fatiga_esfuerzos['tau_m']:.2f} MPa"
)

print(
    f"σa equivalente = "
    f"{fatiga_esfuerzos['sigma_a_eq']:.2f} MPa"
)

print(
    f"σm equivalente = "
    f"{fatiga_esfuerzos['sigma_m_eq']:.2f} MPa"
)

n_fatiga = factor_seguridad_goodman(
    fatiga_esfuerzos["sigma_a_eq"],
    fatiga_esfuerzos["sigma_m_eq"],
    Se,
    Sut_MPa
)

print("\n RESULTADO DE FATIGA")

print(
    f"Factor de seguridad Goodman: "
    f"{n_fatiga:.2f}"
)

if n_fatiga >= n:
    print(
        "El eje cumple el criterio de fatiga."
    )
else:
    print(
        "ADVERTENCIA: "
        "el eje NO cumple el criterio de fatiga."
    )


