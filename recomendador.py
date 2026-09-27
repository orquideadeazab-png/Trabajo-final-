"""
Módulo de recomendación pedagógica de SIAP.

Contiene la lógica para:
1. Calcular el perfil de estilo de aprendizaje (modelo VAK: Visual,
   Auditivo, Kinestésico) a partir de las respuestas de un cuestionario.
2. Recomendar estrategias, recursos y ajustes pedagógicos según el
   estilo dominante, el ritmo de aprendizaje y las necesidades
   específicas declaradas del estudiante.

Se implementa como un sistema experto basado en reglas (sin
dependencias externas de IA), pensado para ser extendido en el futuro
con modelos de machine learning si el proyecto crece.
"""

from __future__ import annotations
from typing import Dict, List

# ---------------------------------------------------------------------------
# 1. Cuestionario de estilo de aprendizaje (modelo VAK)
# ---------------------------------------------------------------------------

PREGUNTAS_VAK: List[Dict] = [
    {
        "pregunta": "Cuando aprendo algo nuevo, prefiero...",
        "opciones": {
            "V": "Ver diagramas, imágenes o videos explicativos",
            "A": "Escuchar una explicación oral o un audio",
            "K": "Practicar directamente haciendo o manipulando algo",
        },
    },
    {
        "pregunta": "Para recordar una instrucción, me ayuda más...",
        "opciones": {
            "V": "Leerla escrita o verla representada gráficamente",
            "A": "Que me la repitan en voz alta",
            "K": "Ensayarla con movimiento o con las manos",
        },
    },
    {
        "pregunta": "En clase me distraigo menos cuando...",
        "opciones": {
            "V": "Hay apoyos visuales (carteles, colores, esquemas)",
            "A": "El docente explica con un tono de voz dinámico",
            "K": "Puedo moverme, tocar materiales o hacer actividades",
        },
    },
    {
        "pregunta": "Cuando resuelvo un problema difícil, suelo...",
        "opciones": {
            "V": "Dibujar un esquema o mapa mental",
            "A": "Hablarlo en voz alta o discutirlo con alguien",
            "K": "Probar distintas soluciones de forma práctica",
        },
    },
    {
        "pregunta": "Mi forma favorita de estudiar es...",
        "opciones": {
            "V": "Con resúmenes visuales, colores y subrayados",
            "A": "Escuchando grabaciones o explicando en voz alta",
            "K": "Con ejercicios prácticos, juegos o experimentos",
        },
    },
]

RITMOS_APRENDIZAJE = ["Rápido", "Moderado", "Necesita más tiempo y repaso"]

NECESIDADES_ESPECIFICAS = [
    "Ninguna reportada",
    "Dificultad de atención / concentración",
    "Dificultad lectoescritura (ej. dislexia)",
    "Dificultad de procesamiento matemático (ej. discalculia)",
    "Barrera de comunicación / lenguaje",
    "Condición motriz",
    "Altas capacidades / requiere mayor reto",
]


def calcular_estilo_dominante(respuestas: List[str]) -> Dict[str, float]:
    """
    Calcula el porcentaje de cada estilo (V, A, K) a partir de una lista
    de respuestas ("V", "A" o "K"), una por cada pregunta respondida.
    Devuelve un diccionario con el porcentaje de cada estilo y el
    estilo dominante.
    """
    total = len(respuestas) or 1
    conteo = {"V": 0, "A": 0, "K": 0}
    for r in respuestas:
        if r in conteo:
            conteo[r] += 1

    porcentajes = {k: round((v / total) * 100, 1) for k, v in conteo.items()}
    dominante = max(porcentajes, key=porcentajes.get)
    porcentajes["dominante"] = dominante
    return porcentajes


# ---------------------------------------------------------------------------
# 2. Base de conocimiento de estrategias pedagógicas
# ---------------------------------------------------------------------------

ESTRATEGIAS_POR_ESTILO = {
    "V": [
        "Usar mapas mentales, infografías y organizadores gráficos.",
        "Apoyar las explicaciones con videos, imágenes y presentaciones.",
        "Emplear código de colores para organizar contenidos e ideas clave.",
        "Entregar guías escritas con esquemas antes de cada tema.",
    ],
    "A": [
        "Explicar los contenidos en voz alta y fomentar el debate en clase.",
        "Usar podcasts, grabaciones o lectura en voz alta como apoyo.",
        "Permitir que el estudiante explique lo aprendido oralmente.",
        "Incorporar canciones, rimas o mnemotecnias auditivas.",
    ],
    "K": [
        "Diseñar actividades prácticas, manipulativas o experimentales.",
        "Usar juegos de rol, simulaciones o estaciones de trabajo rotativas.",
        "Permitir pausas activas y aprendizaje en movimiento.",
        "Asociar conceptos abstractos con objetos físicos o gestos.",
    ],
}

AJUSTES_POR_RITMO = {
    "Rápido": [
        "Ofrecer retos de profundización o proyectos de investigación adicionales.",
        "Asignar rol de mentor de pares en actividades colaborativas.",
    ],
    "Moderado": [
        "Mantener la secuencia estándar de actividades con seguimiento periódico.",
        "Alternar trabajo individual y colaborativo para consolidar contenidos.",
    ],
    "Necesita más tiempo y repaso": [
        "Fragmentar la instrucción en pasos más pequeños y dar tiempo extra.",
        "Reforzar con repaso espaciado y retroalimentación frecuente.",
        "Usar ejemplos resueltos paso a paso antes de la práctica autónoma.",
    ],
}

AJUSTES_POR_NECESIDAD = {
    "Ninguna reportada": [],
    "Dificultad de atención / concentración": [
        "Ubicar al estudiante cerca del docente y lejos de distractores.",
        "Dividir las tareas en bloques cortos con pausas programadas.",
    ],
    "Dificultad lectoescritura (ej. dislexia)": [
        "Usar tipografías y espaciados de fácil lectura, y dar más tiempo para leer.",
        "Permitir respuestas orales como alternativa a la escritura.",
    ],
    "Dificultad de procesamiento matemático (ej. discalculia)": [
        "Apoyar los cálculos con material concreto y representaciones visuales.",
        "Permitir uso de calculadora o tablas de apoyo en ejercicios no evaluativos.",
    ],
    "Barrera de comunicación / lenguaje": [
        "Usar pictogramas, gestos de apoyo y lenguaje simplificado.",
        "Verificar comprensión con preguntas cortas y frecuentes.",
    ],
    "Condición motriz": [
        "Adaptar materiales y espacios para facilitar la manipulación y el acceso.",
        "Ofrecer alternativas tecnológicas de bajo esfuerzo motriz.",
    ],
    "Altas capacidades / requiere mayor reto": [
        "Compactar el currículo y ofrecer proyectos de enriquecimiento.",
        "Fomentar el pensamiento crítico con preguntas abiertas de alto nivel.",
    ],
}


def generar_plan_atencion(
    nombre: str,
    perfil_vak: Dict[str, float],
    ritmo: str,
    necesidad: str,
) -> Dict[str, List[str]]:
    """
    Genera el plan de atención a la diversidad pedagógica para un
    estudiante, combinando estrategias por estilo dominante, ajustes
    por ritmo de aprendizaje y ajustes por necesidad específica.
    """
    dominante = perfil_vak.get("dominante", "V")

    plan = {
        "estudiante": nombre,
        "estilo_dominante": dominante,
        "ritmo": ritmo,
        "necesidad": necesidad,
        "estrategias_estilo": ESTRATEGIAS_POR_ESTILO.get(dominante, []),
        "ajustes_ritmo": AJUSTES_POR_RITMO.get(ritmo, []),
        "ajustes_necesidad": AJUSTES_POR_NECESIDAD.get(necesidad, []),
    }
    return plan


def plan_a_texto(plan: Dict) -> str:
    """Convierte el plan de atención en un texto legible y exportable."""
    nombres_estilo = {"V": "Visual", "A": "Auditivo", "K": "Kinestésico"}
    lineas = [
        f"PLAN DE ATENCIÓN A LA DIVERSIDAD PEDAGÓGICA",
        f"Estudiante: {plan['estudiante']}",
        f"Estilo de aprendizaje dominante: {nombres_estilo.get(plan['estilo_dominante'], plan['estilo_dominante'])}",
        f"Ritmo de aprendizaje: {plan['ritmo']}",
        f"Necesidad específica: {plan['necesidad']}",
        "",
        "Estrategias sugeridas según el estilo de aprendizaje:",
    ]
    lineas += [f"  - {e}" for e in plan["estrategias_estilo"]]
    lineas.append("")
    lineas.append("Ajustes según el ritmo de aprendizaje:")
    lineas += [f"  - {e}" for e in plan["ajustes_ritmo"]]
    if plan["ajustes_necesidad"]:
        lineas.append("")
        lineas.append("Ajustes según la necesidad específica reportada:")
        lineas += [f"  - {e}" for e in plan["ajustes_necesidad"]]
    return "\n".join(lineas)
