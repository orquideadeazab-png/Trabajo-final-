# 🎓 SIAP — Sistema Inteligente de Atención a la Diversidad Pedagógica

Proyecto final del laboratorio de programación en Python. Aplicación
web construida con **Streamlit** que apoya a docentes en la
identificación de estilos y ritmos de aprendizaje de sus estudiantes,
y les recomienda estrategias pedagógicas diferenciadas.

> Desarrollado en **Antigravity** (entorno de desarrollo asistido por IA).

---

## 📌 Descripción

En un mismo salón conviven estudiantes con estilos de aprendizaje
distintos (visual, auditivo, kinestésico), ritmos diferentes y, en
ocasiones, necesidades específicas que requieren ajustes pedagógicos.
**SIAP** centraliza el diagnóstico de cada estudiante y traduce
automáticamente ese perfil en un **plan de atención a la diversidad**
con estrategias concretas, además de un dashboard con la diversidad
de todo el grupo.

## 🎯 Objetivo

Desarrollar una aplicación funcional que, a partir de un cuestionario
sencillo, genere recomendaciones pedagógicas personalizadas por
estudiante y una visión agregada del aula, facilitando la
planificación de clases inclusivas y diferenciadas.

## ⚙️ Funcionalidades principales

- **Diagnóstico de estilo de aprendizaje (modelo VAK):** cuestionario
  de 5 preguntas que calcula el porcentaje Visual / Auditivo /
  Kinestésico y el estilo dominante de cada estudiante.
- **Registro de ritmo de aprendizaje y necesidades específicas.**
- **Motor de recomendaciones basado en reglas:** genera estrategias
  pedagógicas según estilo, ritmo y necesidad del estudiante.
- **Plan de atención descargable** en formato `.txt` por estudiante.
- **Dashboard del aula:** gráficos interactivos (Plotly) con la
  distribución de estilos, ritmos y necesidades del grupo completo.
- **Registro histórico de estudiantes** exportable en `.csv`.

## 🛠️ Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje base |
| Streamlit | Framework de la interfaz web |
| Pandas | Manejo y persistencia de datos |
| Plotly Express | Visualizaciones interactivas |
| Jupyter Notebook | Documentación y sustentación técnica |
| Antigravity | Entorno de desarrollo |

### ¿Por qué Streamlit?

Se eligió Streamlit porque permite construir interfaces web
interactivas usando **solo Python**, sin necesidad de HTML/CSS/JS,
con un ciclo de desarrollo muy rápido (ideal para un prototipo
funcional de laboratorio), amplio soporte de componentes para
formularios y gráficos, y despliegue gratuito e inmediato en
**Streamlit Community Cloud**.

## 📂 Estructura del proyecto

```
siap_project/
├── app.py                     # Aplicación principal de Streamlit
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Este archivo
├── .streamlit/config.toml     # Tema visual de la app
├── assets/                    # Ilustraciones propias (banner, íconos VAK y de ritmo)
│   ├── banner_siap.png
│   ├── icon_visual.png
│   ├── icon_auditivo.png
│   ├── icon_kinestesico.png
│   ├── ritmo_rapido.png
│   ├── ritmo_moderado.png
│   └── ritmo_lento.png
├── data/
│   └── estudiantes.csv        # Datos de ejemplo / persistencia
├── src/
│   ├── recomendador.py        # Cuestionario VAK y motor de recomendaciones
│   └── utils.py                # Carga/guardado de datos
├── notebooks/
│   └── SIAP_documentacion.ipynb  # Cuaderno de sustentación del proyecto
└── docs/
    └── EVIDENCIA_ANTIGRAVITY.md   # Evidencia del uso de Antigravity
```

## ▶️ Instrucciones de ejecución

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd siap_project
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`.

### 4. Abrir el cuaderno de documentación

```bash
jupyter notebook notebooks/SIAP_documentacion.ipynb
```

## 🌐 Despliegue

> Reemplazar con el enlace real una vez desplegado en
> [Streamlit Community Cloud](https://streamlit.io/cloud):
>
> **Enlace de la app en producción:** `<PENDIENTE_DE_COMPLETAR>`

## 🎥 Video de sustentación

> **Enlace al video:** `<PENDIENTE_DE_COMPLETAR>`

## 👤 Autor

Proyecto final — Laboratorio de programación en Python.
