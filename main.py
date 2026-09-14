import math

potencia_kw = 10
rpm = 1750

potencia = potencia_kw * 1000

omega = 2 * math.pi * rpm / 60

torque = potencia / omega

print(f"Torque del eje: {torque:.2f} N·m")

