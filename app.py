"""
SIAP - Sistema Inteligente de Atención a la Diversidad Pedagógica
==================================================================

Aplicación Streamlit que apoya a docentes en la identificación de
estilos y ritmos de aprendizaje de sus estudiantes, y les recomienda
estrategias pedagógicas diferenciadas, generando un plan de atención
a la diversidad exportable.

Ejecutar con:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from src.recomendador import (
    PREGUNTAS_VAK,
    RITMOS_APRENDIZAJE,
    NECESIDADES_ESPECIFICAS,
    calcular_estilo_dominante,
    generar_plan_atencion,
    plan_a_texto,
)
from src.utils import cargar_estudiantes, guardar_estudiantes, agregar_estudiante

RUTA_CSV = "data/estudiantes.csv"

st.set_page_config(
    page_title="SIAP - Atención a la Diversidad Pedagógica",
    page_icon="🎓",
    layout="wide",
)

if "estudiantes" not in st.session_state:
    st.session_state.estudiantes = cargar_estudiantes(RUTA_CSV)

# ---------------------------------------------------------------------------
# Barra lateral de navegación
# ---------------------------------------------------------------------------
st.sidebar.title("🎓 SIAP")
st.sidebar.caption("Sistema Inteligente de Atención a la Diversidad Pedagógica")
seccion = st.sidebar.radio(
    "Navegación",
    [
        "🏠 Inicio",
        "📝 Diagnóstico de estudiante",
        "📋 Recomendaciones y plan",
        "📊 Dashboard del aula",
        "📚 Estudiantes registrados",
    ],
)

# ---------------------------------------------------------------------------
# Sección: Inicio
# ---------------------------------------------------------------------------
if seccion == "🏠 Inicio":
    st.image("assets/banner_siap.png", use_container_width=True)
    st.title("🎓 SIAP: Sistema Inteligente de Atención a la Diversidad Pedagógica")
    st.markdown(
        """
### El problema

En un mismo salón de clases conviven estudiantes con **estilos de
aprendizaje distintos** (visual, auditivo, kinestésico), **ritmos de
aprendizaje diferentes** y, en muchos casos, **necesidades
específicas** que requieren ajustes pedagógicos. Atender esta
diversidad de forma individual es una tarea compleja y demandante
para cualquier docente, especialmente en grupos numerosos.

### La solución

**SIAP** es una herramienta de apoyo docente que:

1. Aplica un breve **cuestionario de estilo de aprendizaje** (modelo VAK)
   a cada estudiante.
2. Registra su **ritmo de aprendizaje** y **necesidades específicas**.
3. Genera automáticamente un **plan de atención a la diversidad**
   pedagógica con estrategias concretas y personalizadas.
4. Ofrece un **dashboard** con la diversidad de todo el grupo, para
   planificar actividades diferenciadas a nivel de aula.

Usa el menú de la izquierda para comenzar con el diagnóstico de un
estudiante.
        """
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("Estudiantes registrados", len(st.session_state.estudiantes))
    if len(st.session_state.estudiantes) > 0:
        estilo_top = (
            st.session_state.estudiantes["estilo_dominante"].mode().iloc[0]
        )
        col2.metric("Estilo más frecuente", estilo_top)
        necesidad_reportadas = (
            st.session_state.estudiantes["necesidad"] != "Ninguna reportada"
        ).sum()
        col3.metric("Con necesidad específica", int(necesidad_reportadas))

# ---------------------------------------------------------------------------
# Sección: Diagnóstico de estudiante
# ---------------------------------------------------------------------------
elif seccion == "📝 Diagnóstico de estudiante":
    st.title("📝 Diagnóstico de estilo de aprendizaje")

    ic1, ic2, ic3 = st.columns(3)
    ic1.image("assets/icon_visual.png", caption="Visual", width=80)
    ic2.image("assets/icon_auditivo.png", caption="Auditivo", width=80)
    ic3.image("assets/icon_kinestesico.png", caption="Kinestésico", width=80)

    with st.form("form_diagnostico"):
        nombre = st.text_input("Nombre del estudiante")
        grado = st.text_input("Grado / curso")

        st.subheader("Cuestionario de estilo de aprendizaje (VAK)")
        respuestas = []
        for i, item in enumerate(PREGUNTAS_VAK):
            opcion = st.radio(
                f"{i + 1}. {item['pregunta']}",
                options=list(item["opciones"].keys()),
                format_func=lambda k, item=item: item["opciones"][k],
                key=f"pregunta_{i}",
            )
            respuestas.append(opcion)

        st.subheader("Otros factores")
        ic_r1, ic_r2, ic_r3 = st.columns(3)
        ic_r1.image("assets/ritmo_rapido.png", caption="Rápido", width=70)
        ic_r2.image("assets/ritmo_moderado.png", caption="Moderado", width=70)
        ic_r3.image("assets/ritmo_lento.png", caption="Necesita más tiempo", width=70)
        ritmo = st.selectbox("Ritmo de aprendizaje observado", RITMOS_APRENDIZAJE)
        necesidad = st.selectbox(
            "Necesidad específica reportada", NECESIDADES_ESPECIFICAS
        )

        enviado = st.form_submit_button("Calcular perfil y guardar")

    if enviado:
        if not nombre:
            st.error("Por favor ingresa el nombre del estudiante.")
        else:
            perfil = calcular_estilo_dominante(respuestas)
            registro = {
                "nombre": nombre,
                "grado": grado,
                "pct_visual": perfil["V"],
                "pct_auditivo": perfil["A"],
                "pct_kinestesico": perfil["K"],
                "estilo_dominante": perfil["dominante"],
                "ritmo": ritmo,
                "necesidad": necesidad,
            }
            st.session_state.estudiantes = agregar_estudiante(
                st.session_state.estudiantes, registro
            )
            guardar_estudiantes(st.session_state.estudiantes, RUTA_CSV)
            st.session_state["ultimo_perfil"] = registro
            st.success(f"Perfil de {nombre} calculado y guardado ✅")

            nombres_estilo = {"V": "Visual", "A": "Auditivo", "K": "Kinestésico"}
            st.write(
                f"**Estilo dominante:** {nombres_estilo[perfil['dominante']]} "
                f"(Visual {perfil['V']}% · Auditivo {perfil['A']}% · "
                f"Kinestésico {perfil['K']}%)"
            )
            st.info(
                "Ve a la sección **📋 Recomendaciones y plan** para generar "
                "el plan de atención de este estudiante."
            )

# ---------------------------------------------------------------------------
# Sección: Recomendaciones y plan
# ---------------------------------------------------------------------------
elif seccion == "📋 Recomendaciones y plan":
    st.title("📋 Recomendaciones y plan de atención")

    df = st.session_state.estudiantes
    if df.empty:
        st.warning(
            "Aún no hay estudiantes registrados. Ve primero a "
            "**📝 Diagnóstico de estudiante**."
        )
    else:
        nombre_sel = st.selectbox("Selecciona un estudiante", df["nombre"].tolist())
        fila = df[df["nombre"] == nombre_sel].iloc[-1]

        perfil_vak = {
            "V": fila["pct_visual"],
            "A": fila["pct_auditivo"],
            "K": fila["pct_kinestesico"],
            "dominante": fila["estilo_dominante"],
        }

        plan = generar_plan_atencion(
            nombre=fila["nombre"],
            perfil_vak=perfil_vak,
            ritmo=fila["ritmo"],
            necesidad=fila["necesidad"],
        )

        st.subheader(f"Estrategias recomendadas para {fila['nombre']}")
        st.markdown("**Según su estilo de aprendizaje dominante:**")
        for e in plan["estrategias_estilo"]:
            st.markdown(f"- {e}")

        st.markdown("**Según su ritmo de aprendizaje:**")
        for e in plan["ajustes_ritmo"]:
            st.markdown(f"- {e}")

        if plan["ajustes_necesidad"]:
            st.markdown("**Según su necesidad específica:**")
            for e in plan["ajustes_necesidad"]:
                st.markdown(f"- {e}")

        texto_plan = plan_a_texto(plan)
        st.download_button(
            "⬇️ Descargar plan de atención (.txt)",
            data=texto_plan,
            file_name=f"plan_atencion_{fila['nombre'].replace(' ', '_')}.txt",
        )

# ---------------------------------------------------------------------------
# Sección: Dashboard del aula
# ---------------------------------------------------------------------------
elif seccion == "📊 Dashboard del aula":
    st.title("📊 Dashboard de diversidad del aula")

    df = st.session_state.estudiantes
    if df.empty:
        st.warning("Aún no hay estudiantes registrados para mostrar estadísticas.")
    else:
        ic1, ic2, ic3 = st.columns(3)
        ic1.image("assets/icon_visual.png", caption="Visual", width=90)
        ic2.image("assets/icon_auditivo.png", caption="Auditivo", width=90)
        ic3.image("assets/icon_kinestesico.png", caption="Kinestésico", width=90)

        col1, col2 = st.columns(2)

        with col1:
            conteo_estilo = df["estilo_dominante"].value_counts().reset_index()
            conteo_estilo.columns = ["estilo", "cantidad"]
            nombres = {"V": "Visual", "A": "Auditivo", "K": "Kinestésico"}
            conteo_estilo["estilo"] = conteo_estilo["estilo"].map(nombres)
            fig1 = px.pie(
                conteo_estilo,
                names="estilo",
                values="cantidad",
                title="Distribución de estilos de aprendizaje",
            )
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            ir1, ir2, ir3 = st.columns(3)
            ir1.image("assets/ritmo_rapido.png", width=55)
            ir2.image("assets/ritmo_moderado.png", width=55)
            ir3.image("assets/ritmo_lento.png", width=55)
            conteo_ritmo = df["ritmo"].value_counts().reset_index()
            conteo_ritmo.columns = ["ritmo", "cantidad"]
            fig2 = px.bar(
                conteo_ritmo,
                x="ritmo",
                y="cantidad",
                title="Ritmos de aprendizaje en el grupo",
            )
            st.plotly_chart(fig2, use_container_width=True)

        conteo_necesidad = df["necesidad"].value_counts().reset_index()
        conteo_necesidad.columns = ["necesidad", "cantidad"]
        fig3 = px.bar(
            conteo_necesidad,
            x="cantidad",
            y="necesidad",
            orientation="h",
            title="Necesidades específicas reportadas en el grupo",
        )
        st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------------------------
# Sección: Estudiantes registrados
# ---------------------------------------------------------------------------
elif seccion == "📚 Estudiantes registrados":
    st.title("📚 Estudiantes registrados")
    df = st.session_state.estudiantes
    if df.empty:
        st.info("No hay estudiantes registrados todavía.")
    else:
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "⬇️ Descargar registro completo (.csv)",
            data=df.to_csv(index=False),
            file_name="estudiantes_siap.csv",
        )
