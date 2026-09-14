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


# CARGA SOBRE EL EJE

fuerza = float(input("\nFuerza vertical aplicada [N]: "))

posicion = float(input("Posición de la fuerza desde el apoyo A [m]: "))


# Fuerza hacia abajo = negativa

cargas = [(posicion, -abs(fuerza))]


# REACCIONES

RA, RB = calcular_reacciones(longitud,cargas)

print("\n REACCIONES EN LOS APOYOS ")

print(f"Reacción en A: {RA:.2f} N")

print(f"Reacción en B: {RB:.2f} N")


# DIAGRAMAS

x, cortante, momento = calcular_diagramas(longitud,cargas,RA,RB)


# MOMENTO MÁXIMO

momento_maximo = max(abs(momento))

print(f"\nMomento flector máximo: "f"{momento_maximo:.2f} N·m")


# GENERAR Y GUARDAR GRÁFICAS

graficar_diagramas(x,cortante,momento)

print("\nGráficas guardadas en la carpeta 'resultados'.")