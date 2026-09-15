import streamlit as st
import numpy as np

from src.torque import calcular_torque
from src.reacciones import calcular_reacciones

from src.diagramas import (
    calcular_diagramas,
    crear_grafica,
    guardar_grafica
)

from src.esfuerzos import (
    diametro_minimo,
    seleccionar_diametro_comercial,
    esfuerzo_flexion,
    esfuerzo_torsion,
    esfuerzo_von_mises,
    factor_seguridad
)


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Diseño de Eje Mecánico",
    layout="wide"
)

st.title("Diseño y análisis de eje mecánico")

st.write(
    "Herramienta para el dimensionamiento preliminar "
    "de ejes sometidos a flexión y torsión."
)


# ============================================================
# FORMULARIO DE ENTRADA
# ============================================================

with st.form("formulario_eje"):

    # --------------------------------------------------------
    # DATOS DE OPERACIÓN
    # --------------------------------------------------------

    st.header("1. Datos de operación")

    col1, col2, col3 = st.columns(3)

    with col1:

        potencia = st.number_input(
            "Potencia transmitida [kW]",
            min_value=0.1,
            value=10.0,
            key="potencia"
        )

    with col2:

        rpm = st.number_input(
            "Velocidad de giro [rpm]",
            min_value=1.0,
            value=1750.0,
            key="rpm"
        )

    with col3:

        longitud = st.number_input(
            "Longitud del eje [m]",
            min_value=0.1,
            value=1.0,
            key="longitud"
        )


    # --------------------------------------------------------
    # CARGAS
    # --------------------------------------------------------

    st.header("2. Cargas sobre el eje")

    col1, col2, col3 = st.columns(3)

    with col1:

        Fy = st.number_input(
            "Fuerza vertical Fy [N]",
            min_value=0.0,
            value=1000.0,
            key="Fy"
        )

    with col2:

        Fz = st.number_input(
            "Fuerza horizontal Fz [N]",
            min_value=0.0,
            value=500.0,
            key="Fz"
        )

    with col3:

        posicion = st.number_input(
            "Posición de la carga desde A [m]",
            min_value=0.0,
            max_value=float(longitud),
            value=min(0.4, float(longitud)),
            key="posicion"
        )


    # --------------------------------------------------------
    # MATERIAL Y SEGURIDAD
    # --------------------------------------------------------

    st.header("3. Material y criterio de diseño")

    col1, col2 = st.columns(2)

    with col1:

        Sy_MPa = st.number_input(
            "Límite de fluencia Sy [MPa]",
            min_value=1.0,
            value=530.0,
            key="Sy"
        )

    with col2:

        factor_seguridad_deseado = st.number_input(
            "Factor de seguridad deseado",
            min_value=1.0,
            value=2.0,
            key="factor_seguridad"
        )


    # --------------------------------------------------------
    # BOTÓN
    # --------------------------------------------------------

    calcular = st.form_submit_button(
        "Calcular eje"
    )


# ============================================================
# CÁLCULOS
# ============================================================

if calcular:

    # --------------------------------------------------------
    # TORQUE
    # --------------------------------------------------------

    torque = calcular_torque(
        potencia,
        rpm
    )


    # --------------------------------------------------------
    # CARGAS EN LOS DOS PLANOS
    # --------------------------------------------------------

    cargas_y = [
        (posicion, -abs(Fy))
    ]

    cargas_z = [
        (posicion, -abs(Fz))
    ]


    # --------------------------------------------------------
    # REACCIONES
    # --------------------------------------------------------

    RA_y, RB_y = calcular_reacciones(
        longitud,
        cargas_y
    )

    RA_z, RB_z = calcular_reacciones(
        longitud,
        cargas_z
    )


    # --------------------------------------------------------
    # DIAGRAMAS
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # MOMENTO RESULTANTE
    # --------------------------------------------------------

    momento_resultante = np.sqrt(
        momento_y**2
        + momento_z**2
    )

    indice_M_max = np.argmax(
        np.abs(momento_resultante)
    )

    M_max = np.abs(
        momento_resultante[indice_M_max]
    )

    posicion_M_max = x[
        indice_M_max
    ]


    # --------------------------------------------------------
    # DIMENSIONAMIENTO
    # --------------------------------------------------------

    Sy = Sy_MPa * 1e6

    d = diametro_minimo(
        M_max,
        torque,
        Sy,
        factor_seguridad_deseado
    )

    d_mm = d * 1000

    diametro_comercial = seleccionar_diametro_comercial(
        d_mm
    )

    d_comercial_m = (
        diametro_comercial / 1000
    )


    # --------------------------------------------------------
    # VERIFICACIÓN ESTÁTICA
    # --------------------------------------------------------

    sigma = esfuerzo_flexion(
        M_max,
        d_comercial_m
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


    # ========================================================
    # RESULTADOS
    # ========================================================

    st.header("4. Resultados principales")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Torque",
        f"{torque:.2f} N·m"
    )

    col2.metric(
        "Momento máximo",
        f"{M_max:.2f} N·m"
    )

    col3.metric(
        "Diámetro mínimo",
        f"{d_mm:.2f} mm"
    )

    col4.metric(
        "Diámetro comercial",
        f"{diametro_comercial:.0f} mm"
    )


    # ========================================================
    # REACCIONES
    # ========================================================

    st.header("5. Reacciones en los apoyos")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "RA - Plano Y",
        f"{RA_y:.2f} N"
    )

    col2.metric(
        "RB - Plano Y",
        f"{RB_y:.2f} N"
    )

    col3.metric(
        "RA - Plano Z",
        f"{RA_z:.2f} N"
    )

    col4.metric(
        "RB - Plano Z",
        f"{RB_z:.2f} N"
    )


    # ========================================================
    # SECCIÓN CRÍTICA
    # ========================================================

    st.subheader("Sección crítica")

    col1, col2 = st.columns(2)

    col1.metric(
        "Momento resultante máximo",
        f"{M_max:.2f} N·m"
    )

    col2.metric(
        "Posición",
        f"{posicion_M_max:.3f} m"
    )


    # ========================================================
    # CREACIÓN DE GRÁFICAS
    # ========================================================

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


    # ========================================================
    # MOSTRAR GRÁFICAS
    # ========================================================

    st.header("6. Diagramas del eje")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Cortante - Plano Y")

        st.pyplot(
            fig_cortante_y
        )

    with col2:

        st.subheader("Momento - Plano Y")

        st.pyplot(
            fig_momento_y
        )


    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Cortante - Plano Z")

        st.pyplot(
            fig_cortante_z
        )

    with col2:

        st.subheader("Momento - Plano Z")

        st.pyplot(
            fig_momento_z
        )


    st.subheader(
        "Momento flector resultante"
    )

    st.pyplot(
        fig_resultante
    )


    # ========================================================
    # VERIFICACIÓN ESTÁTICA
    # ========================================================

    st.header("7. Verificación estática")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Esfuerzo de flexión",
        f"{sigma / 1e6:.2f} MPa"
    )

    col2.metric(
        "Von Mises",
        f"{sigma_vm / 1e6:.2f} MPa"
    )

    col3.metric(
        "Factor de seguridad real",
        f"{n_real:.2f}"
    )


    if n_real >= factor_seguridad_deseado:

        st.success(
            "El eje cumple el factor de seguridad requerido."
        )

    else:

        st.error(
            "El eje NO cumple el factor de seguridad requerido."
        )


    st.success(
        "Los diagramas fueron guardados en la carpeta 'resultados'."
    )