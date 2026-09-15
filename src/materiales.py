import csv


def cargar_materiales():

    materiales = []

    with open(
        "data/materiales.csv",
        mode="r",
        encoding="utf-8"
    ) as archivo:

        lector = csv.DictReader(archivo)

        for fila in lector:

            material = {
                "Material": fila["Material"],
                "Condicion": fila["Condicion"],
                "Sy_MPa": float(fila["Sy_MPa"]),
                "Sut_MPa": float(fila["Sut_MPa"]),
                "E_GPa": float(fila["E_GPa"]),
                "Fuente": fila["Fuente"]
            }

            materiales.append(material)

    return materiales

def seleccionar_material(materiales):

    print("\n=== SELECCIÓN DE MATERIAL ===")

    for i, material in enumerate(materiales, start=1):

        print(
            f"{i}. {material['Material']} "
            f"- Sy = {material['Sy_MPa']} MPa"
        )

    opcion = int(
        input("\nSeleccione un material (1. AISI 1020 - Sy = 350.0 MPa 2. AISI 1045 - Sy = 530.0 MPa 3. AISI 4140 - Sy = 655.0 MPa): ")
    )

    if opcion < 1 or opcion > len(materiales):
        raise ValueError(
            "Selección de material no válida."
        )

    return materiales[opcion - 1]