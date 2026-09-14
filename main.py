import math

potencia_kw = float(input("Potencia transmitida [kW]: "))
rpm = float(input("Velocidad de giro [rpm]: "))
longitud = float(input("Longitud del eje [m]: "))

potencia = potencia_kw * 1000

omega = 2 * math.pi * rpm / 60

torque = potencia / omega

print(f"Torque del eje: {torque:.2f} N·m")

