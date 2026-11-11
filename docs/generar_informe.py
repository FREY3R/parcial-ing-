"""Genera el informe PDF del Parcial 3 con reportlab.

Uso: python docs/generar_informe.py
Salida: Informe_Parcial3_0182410093.pdf
"""

import os

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    LongTable,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    TableStyle,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "Informe_Parcial3_0182410093.pdf")

FONT, FONT_B, FONT_I, FONT_M = "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Courier"
try:
    pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Bold", "C:/Windows/Fonts/arialbd.ttf"))
    pdfmetrics.registerFont(TTFont("Arial-Italic", "C:/Windows/Fonts/ariali.ttf"))
    pdfmetrics.registerFont(TTFont("Consolas", "C:/Windows/Fonts/consola.ttf"))
    FONT, FONT_B, FONT_I, FONT_M = "Arial", "Arial-Bold", "Arial-Italic", "Consolas"
except Exception:
    pass

AZUL = colors.HexColor("#1e40af")
GRIS = colors.HexColor("#6b7280")
GRIS_CLARO = colors.HexColor("#f3f4f6")
BORDE = colors.HexColor("#9ca3af")

ss = getSampleStyleSheet()
ST = {
    "Title": ParagraphStyle("Title", parent=ss["Title"], fontName=FONT_B, fontSize=24,
                            leading=29, alignment=TA_CENTER, textColor=AZUL, spaceAfter=8),
    "Subtitle": ParagraphStyle("Subtitle", parent=ss["Normal"], fontName=FONT, fontSize=14,
                               leading=18, alignment=TA_CENTER, textColor=GRIS, spaceAfter=6),
    "H1": ParagraphStyle("H1", parent=ss["Heading1"], fontName=FONT_B, fontSize=15,
                         leading=19, textColor=AZUL, spaceBefore=10, spaceAfter=6),
    "H2": ParagraphStyle("H2", parent=ss["Heading2"], fontName=FONT_B, fontSize=11.5,
                         leading=15, textColor=colors.HexColor("#111827"), spaceBefore=8,
                         spaceAfter=4),
    "Body": ParagraphStyle("Body", parent=ss["BodyText"], fontName=FONT, fontSize=9.5,
                           leading=13, alignment=TA_JUSTIFY, spaceAfter=5),
    "Bullet": ParagraphStyle("Bullet", parent=ss["BodyText"], fontName=FONT, fontSize=9.5,
                             leading=13, leftIndent=12, bulletIndent=2, spaceAfter=3),
    "Note": ParagraphStyle("Note", parent=ss["BodyText"], fontName=FONT_I, fontSize=8.5,
                           leading=11.5, textColor=colors.HexColor("#374151"),
                           backColor=colors.HexColor("#eff6ff"), borderPadding=5,
                           spaceBefore=3, spaceAfter=7),
    "Code": ParagraphStyle("Code", parent=ss["Code"], fontName=FONT_M, fontSize=7.6,
                           leading=10, backColor=GRIS_CLARO, borderPadding=5,
                           spaceBefore=3, spaceAfter=7),
    "Cell": ParagraphStyle("Cell", fontName=FONT, fontSize=7.2, leading=9),
    "CellH": ParagraphStyle("CellH", fontName=FONT_B, fontSize=7.2, leading=9,
                            textColor=colors.white),
}

story = []


def P(texto, estilo="Body"):
    story.append(Paragraph(texto, ST[estilo]))


def H1(texto):
    story.append(Paragraph(texto, ST["H1"]))


def H2(texto):
    story.append(Paragraph(texto, ST["H2"]))


def B(texto):
    story.append(Paragraph("• " + texto, ST["Bullet"]))


def NOTE(texto):
    story.append(Paragraph(texto, ST["Note"]))


def CODE(texto):
    story.append(Preformatted(texto, ST["Code"]))


def esc(valor):
    return (str(valor).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def T(datos, anchos, tam=7.2, cabecera=True):
    filas = []
    for i, fila in enumerate(datos):
        celdas = []
        for valor in fila:
            estilo = ST["CellH"] if (cabecera and i == 0) else ST["Cell"]
            celdas.append(Paragraph(esc(valor), estilo))
        filas.append(celdas)
    tabla = LongTable(filas, colWidths=anchos, repeatRows=1 if cabecera else 0)
    comandos = [
        ("GRID", (0, 0), (-1, -1), 0.4, BORDE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]
    if cabecera:
        comandos += [
            ("BACKGROUND", (0, 0), (-1, 0), AZUL),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, GRIS_CLARO]),
        ]
    tabla.setStyle(TableStyle(comandos))
    return tabla


def IMG(ruta, max_w=17 * cm, max_h=21 * cm):
    ruta = os.path.join(BASE, ruta)
    with PILImage.open(ruta) as im:
        w, h = im.size
    escala = min(max_w / w, max_h / h)
    return Image(ruta, width=w * escala, height=h * escala)


def pie(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d1d5db"))
    canvas.line(2 * cm, 1.55 * cm, A4[0] - 2 * cm, 1.55 * cm)
    canvas.setFont(FONT, 7)
    canvas.setFillColor(GRIS)
    canvas.drawString(2 * cm, 1.1 * cm,
                      "Parcial 3 · Ingeniería de Software I — Yerfreth Mejía Sierra (0182410093)")
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f"Página {doc.page}")
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Portada
# ---------------------------------------------------------------------------
story.append(Spacer(1, 2.2 * cm))
story.append(Paragraph("Parcial 3 · Ingeniería de Software I", ST["Title"]))
story.append(Paragraph("Sistema de cálculo de costos de envío", ST["Subtitle"]))
story.append(Spacer(1, 1.2 * cm))
info = [
    ["Estudiante", "Yerfreth Mejía Sierra"],
    ["Código", "0182410093"],
    ["Programa", "Ingeniería de Sistemas"],
    ["Universidad", "Universidad de La Guajira"],
    ["Grupo", "B1"],
    ["Repositorio", "https://github.com/FREY3R/parcial-ing-.git"],
    ["Versiones", "v1.0.0 · v2.0.0 · v2.1.0"],
    ["Fecha", "11 de noviembre de 2026"],
]
story.append(T(info, [4 * cm, 12 * cm], tam=9, cabecera=False))
story.append(Spacer(1, 1.0 * cm))
P("Este informe documenta el análisis, diseño de pruebas, corrección, "
  "refactorización y gestión del cambio de un sistema de cálculo de costos de "
  "envío, particularizado con los parámetros del código 0182410093. Todo el "
  "trabajo está versionado en GitHub con ramas por defecto y tags SemVer.")
story.append(Spacer(1, 0.4 * cm))
H2("Resultados principales")
resultados = [
    ["Indicador", "v1.0.0", "v2.0.0", "v2.1.0"],
    ["Pruebas", "36 (14 pasan)", "43 (43 pasan)", "55 (55 pasan)"],
    ["Cobertura", "96,6 % sentencias", "100 % sent. y ramas", "100 % sent. y ramas"],
    ["Complejidad máxima", "15", "3", "3"],
    ["Complejidad promedio", "15,0", "1,76", "1,76"],
    ["Defectos abiertos", "7", "0", "0"],
]
story.append(T(resultados, [5.4 * cm, 3.8 * cm, 4.0 * cm, 3.8 * cm], tam=8))
story.append(PageBreak())

# ---------------------------------------------------------------------------
# 1. Introducción
# ---------------------------------------------------------------------------
H1("1. Introducción y objetivos")
P("El parcial pide aplicar el proceso de ingeniería de software sobre un "
  "programa heredado que calcula el costo de un envío. El programa original "
  "contiene defectos respecto a una especificación propia, construida a partir "
  "de los últimos seis dígitos del código estudiantil. El trabajo cubre el "
  "ciclo completo: requisitos, pruebas, detección de defectos, corrección, "
  "refactorización, configuración y gestión del cambio.")
H2("Objetivos")
B("Particularizar los requisitos R1–R8 con el código 0182410093.")
B("Diseñar casos de caja negra (particiones, límites, decisión) y de caja blanca (grafo, complejidad, caminos).")
B("Construir una suite que evidencie los fallos del heredado y sirva de regresión.")
B("Documentar y corregir siete defectos con TDD y ramas independientes.")
B("Refactorizar el código y versionarlo con SemVer.")
B("Aplicar el cambio CAMBIO=1 solicitado en la Parte 8.")
H2("Alcance")
P("El sistema es una función de cálculo (`calc`) con validaciones y una API "
  "pública mínima. No incluye interfaz gráfica, base de datos ni servicios "
  "externos. La salida es un entero en pesos, múltiplo de 100.")

# ---------------------------------------------------------------------------
# 2. Parámetros
# ---------------------------------------------------------------------------
H1("2. Parámetros de la especificación")
P("Los últimos seis dígitos del código son 4, 1, 0, 0, 9 y 3. Las paridades "
  "determinan cuatro decisiones: D par incluye L1, E impar aplica el finde "
  "después de los descuentos, B impar aplica ambos descuentos y F impar exige "
  "error para cupón inexistente.")
params = [
    ["Símbolo", "Valor", "Regla"],
    ["PMAX", "50 kg", "Peso máximo; 50 es válido, 50,01 no"],
    ["L1", "3 kg", "Límite del tramo 1, incluido por D par"],
    ["L2", "10 kg", "Límite del tramo 2, incluido"],
    ["RR", "15 %", "Recargo de zona rural"],
    ["RN", "40 %", "Recargo de zona nacional"],
    ["V", "15 %", "Descuento cliente VIP"],
    ["S", "2000", "Recargo de fin de semana"],
    ["CAMBIO", "1", "Cliente empresarial 12 % y sin zona si peso > L2"],
]
story.append(T(params, [3 * cm, 3 * cm, 11 * cm], tam=8))

# ---------------------------------------------------------------------------
# 3. Requisitos
# ---------------------------------------------------------------------------
H1("3. Requisitos R1–R8")
reqs = [
    ["ID", "Requisito", "Regla"],
    ["R1", "Validación del peso", "0 < peso <= 50; si no, ValueError('peso inválido')"],
    ["R2", "Zona y día", "zona en {urbana, rural, nacional}; día entero en [1, 7]"],
    ["R3", "Tramos de peso", "<=3: 6000; <=10: 9000; >10: 9000 + 800·(peso-10)"],
    ["R4", "Recargo por zona", "urbana 0 %; rural +15 %; nacional +40 %"],
    ["R5", "Fin de semana", "día 6 o 7 suma 2000; por E impar, después de descuentos"],
    ["R6", "Descuentos", "frecuente 5 %; vip 15 %; cupón ENVIO10 10 %; por B impar, ambos"],
    ["R7", "Cupón inexistente", "si no es None ni ENVIO10, ValueError; None es válido"],
    ["R8", "Mínimo y redondeo", "mínimo 5000; half-up al múltiplo de 100"],
]
story.append(T(reqs, [1.2 * cm, 4.2 * cm, 11.6 * cm], tam=7.8))
NOTE("Orden oficial: validar, costo base, recargo de zona, descuentos de cliente "
     "y cupón, recargo de fin de semana, mínimo y redondeo half-up.")

# ---------------------------------------------------------------------------
# 4. Plan de pruebas
# ---------------------------------------------------------------------------
H1("4. Plan de pruebas")
P("La estrategia combina pruebas unitarias y de integración. Los valores "
  "esperados se calcularon de forma independiente con aritmética Decimal en "
  "`docs/referencia_calculo.py`; en ningún caso se obtuvieron ejecutando el "
  "código heredado.")
H2("Técnicas aplicadas")
B("Partición de equivalencia para peso, zona, cliente, día y cupón.")
B("Análisis de valores límite en 0, L1, L2, PMAX y sus vecinos.")
B("Tabla de decisión para combinaciones de zona, cliente, cupón y día.")
B("Cobertura de caminos del grafo de flujo (15 caminos independientes).")
B("Pruebas de integración para mínimo, redondeo y CAMBIO=1.")
H2("Entorno")
P("Windows 11, Python 3.13.5, pytest 9.2.0, pytest-cov 7.1.0, coverage 7.17.2, "
  "matplotlib 3.11.2, Pillow 13.0.0, reportlab 5.1.0 y radon. Control de "
  "versiones con Git 2.56.0 y repositorio en GitHub.")
H2("Criterios de entrada y salida")
P("Entrada: especificación R1–R8 aprobada y calculadora de referencia. Salida: "
  "55 pruebas en verde, 100 % de cobertura de sentencias y ramas, y evidencia "
  "en texto y PNG.")

# ---------------------------------------------------------------------------
# 5. Caja negra
# ---------------------------------------------------------------------------
H1("5. Caja negra")
H2("5.1 Particiones de equivalencia")
particiones = [
    ["Entrada", "Clases válidas e inválidas"],
    ["Peso", "inválida <= 0; válida (0, 3]; válida (3, 10]; válida (10, 50]; inválida > 50"],
    ["Zona", "urbana; rural; nacional; inválida (cualquier otra, incluso mayúsculas)"],
    ["Cliente", "ninguno; frecuente; vip; empresarial (v2.1.0); desconocido"],
    ["Día", "entre semana 1–5; sábado 6; domingo 7; inválido 0, 8 o no entero"],
    ["Cupón", "None; ENVIO10; inválido (OTRO, ENVIO20, etc.)"],
]
story.append(T(particiones, [3.2 * cm, 13.8 * cm], tam=8))
H2("5.2 Valores límite")
limites = [
    ["Variable", "Valores probados"],
    ["Peso", "0 (inválido), 0,01 (válido), 3 (válido), 3,01 (siguiente tramo), 10 (válido), 10,1 (proporcional), 50 (válido), 50,01 (inválido)"],
    ["L1", "3 incluido: paga 6000; 3,01 paga 9000"],
    ["L2", "10 incluido: paga 9000; 10,1 paga 9000 + 80"],
    ["PMAX", "50 paga 41000; 51 lanza error"],
    ["Día", "1 y 5 sin recargo; 6 y 7 con 2000; 0, 8 y 6,5 error"],
]
story.append(T(limites, [2.8 * cm, 14.2 * cm], tam=8))
H2("5.3 Matriz de 33 casos")
casos = [
    ["ID", "Req.", "Peso", "Zona", "Cliente", "Día", "Cupón", "Esperado", "Técnica"],
    ["C01", "R3", "2", "urbana", "ninguno", "3", "-", "$6.000", "PE tramo 1"],
    ["C02", "R3", "3", "urbana", "ninguno", "3", "-", "$6.000", "VL L1 incluido"],
    ["C03", "R3", "4", "urbana", "ninguno", "3", "-", "$9.000", "PE tramo 2"],
    ["C04", "R3", "10", "urbana", "ninguno", "3", "-", "$9.000", "VL L2 incluido"],
    ["C05", "R3", "11", "urbana", "ninguno", "3", "-", "$9.800", "VL L2+1"],
    ["C06", "R3", "12,5", "urbana", "ninguno", "3", "-", "$11.000", "PE tramo 3"],
    ["C07", "R4, R8", "5", "rural", "ninguno", "3", "-", "$10.400", "PE zona + half-up"],
    ["C08", "R4", "5", "nacional", "ninguno", "3", "-", "$12.600", "PE zona"],
    ["C09", "R4", "5", "urbana", "ninguno", "3", "-", "$9.000", "PE sin recargo"],
    ["C10", "R6, R8", "5", "urbana", "frecuente", "3", "-", "$8.600", "PE cliente + half-up"],
    ["C11", "R6", "5", "urbana", "vip", "3", "-", "$7.700", "PE cliente"],
    ["C12", "R6", "5", "urbana", "ninguno", "3", "ENVIO10", "$8.100", "PE cupón"],
    ["C13", "R6", "5", "urbana", "vip", "3", "ENVIO10", "$6.900", "TD ambos (B impar)"],
    ["C14", "R6", "5", "urbana", "frecuente", "3", "ENVIO10", "$7.700", "TD ambos (B impar)"],
    ["C15", "R5", "5", "urbana", "ninguno", "6", "-", "$11.000", "VL sábado"],
    ["C16", "R5", "5", "urbana", "ninguno", "7", "-", "$11.000", "VL domingo"],
    ["C17", "R5, E", "5", "urbana", "vip", "6", "-", "$9.700", "TD orden finde"],
    ["C18", "R5, E", "5", "urbana", "vip", "6", "ENVIO10", "$8.900", "TD orden + ambos"],
    ["C19", "R7", "5", "urbana", "ninguno", "3", "OTRO", "ValueError", "PE cupón inválido"],
    ["C20", "R7", "5", "urbana", "ninguno", "3", "ENVIO20", "ValueError", "PE cupón inválido"],
    ["C21", "R1", "0", "urbana", "ninguno", "3", "-", "ValueError", "VL peso 0"],
    ["C22", "R1", "-1", "urbana", "ninguno", "3", "-", "ValueError", "PE peso inválido"],
    ["C23", "R1", "51", "urbana", "ninguno", "3", "-", "ValueError", "VL PMAX+1"],
    ["C24", "R1, R3", "50", "urbana", "ninguno", "3", "-", "$41.000", "VL PMAX válido"],
    ["C25", "R2", "5", "express", "ninguno", "3", "-", "ValueError", "PE zona inválida"],
    ["C26", "R2", "5", "Urbana", "ninguno", "3", "-", "ValueError", "PE capitalización"],
    ["C27", "R2", "5", "urbana", "ninguno", "0", "-", "ValueError", "VL día 0"],
    ["C28", "R2", "5", "urbana", "ninguno", "8", "-", "ValueError", "VL día 8"],
    ["C29", "R2", "5", "urbana", "ninguno", "6,5", "-", "ValueError", "Día no entero"],
    ["C30", "R8", "2", "urbana", "vip", "3", "ENVIO10", "$5.000", "Mínimo"],
    ["C31", "R3, R8", "10,1", "urbana", "ninguno", "3", "-", "$9.100", "Proporcional + half-up"],
    ["C32", "R5, R6", "2", "rural", "frecuente", "6", "ENVIO10", "$7.900", "Integración"],
    ["C33", "R3, R4", "10,1", "nacional", "ninguno", "3", "-", "$12.700", "Integración"],
]
story.append(T(casos, [1.0 * cm, 1.5 * cm, 1.2 * cm, 1.8 * cm, 2.2 * cm, 0.9 * cm,
                       2.1 * cm, 2.4 * cm, 3.9 * cm], tam=6.4))
NOTE("Con CAMBIO=1 (Parte 8), C33 pasa a $9.100 porque el peso supera L2 y no se "
     "cobra recargo de zona. El resto de la matriz conserva sus valores.")

H2("5.4 Cálculos paso a paso")
P("<b>C07 — 5 kg, rural, ninguno, día 3:</b> base 9000; zona rural 9000 × 1,15 = "
  "10350; sin descuentos; sin finde; mínimo no aplica; 10350 / 100 = 103,5 → "
  "half-up 104 → <b>$10.400</b>.")
P("<b>C13 — 5 kg, urbana, vip, ENVIO10, día 3:</b> base 9000; zona urbana 9000; "
  "vip 9000 × 0,85 = 7650; cupón 7650 × 0,90 = 6885; sin finde; mínimo no; "
  "68,85 → 69 → <b>$6.900</b>.")
P("<b>C30 — 2 kg, urbana, vip, ENVIO10, día 3:</b> base 6000; vip 5100; cupón "
  "4590; mínimo 5000; redondeo <b>$5.000</b>.")
P("<b>C33 con CAMBIO=1 — 10,1 kg, nacional, ninguno, día 3:</b> base 9000 + "
  "0,1 × 800 = 9080; peso > L2 → sin recargo de zona; sin descuentos; 90,8 → 91 "
  "→ <b>$9.100</b>.")

# ---------------------------------------------------------------------------
# 6. Caja blanca
# ---------------------------------------------------------------------------
story.append(PageBreak())
H1("6. Caja blanca")
P("Se construyó el grafo de flujo del heredado descomponiendo el `or` de la "
  "validación de peso en dos predicados, P1a y P1b, que es la convención de "
  "McCabe para cortocircuito y la que usa radon.")
conteo = [
    ["Elemento", "Cantidad"],
    ["Nodos (N)", "30"],
    ["Aristas (E)", "43"],
    ["Predicados", "14 (P1a, P1b, P2–P13)"],
    ["Regiones", "15 (incluye la exterior)"],
    ["Complejidad (E - N + 2)", "43 - 30 + 2 = 15"],
    ["Complejidad (predicados + 1)", "14 + 1 = 15"],
    ["Complejidad (regiones)", "15"],
    ["radon sobre calc (v1.0.0)", "C (15)"],
]
story.append(T(conteo, [6.5 * cm, 10.5 * cm], tam=8))
NOTE("Las tres formas coinciden en M=15 y con radon. Si se modelara P1 como un "
     "solo nodo compuesto, el conteo bajaría a 14 en las tres formas; se adopta "
     "la descomposición por ser la convención estándar.")
H2("6.1 Grafo de flujo")
story.append(IMG("evidence/grafo_flujo.png", max_w=15.5 * cm, max_h=20.5 * cm))
story.append(PageBreak())
H2("6.2 Caminos independientes y caso por camino")
caminos = [
    ["CP", "Decisiones", "Caso", "Esperado"],
    ["CP01", "P1a F, P1b F, P2 T, P4 T, P7 F, P8 F, P9 F, P10 F, P12 F, P13 F", "C01", "$6.000"],
    ["CP02", "P1a T", "C21", "ValueError"],
    ["CP03", "P1a F, P1b T", "C23", "ValueError"],
    ["CP04", "P2 F, P3 T", "C03", "$9.000"],
    ["CP05", "P2 F, P3 F", "C05", "$9.800"],
    ["CP06", "P4 F, P5 T", "C07", "$10.400"],
    ["CP07", "P5 F, P6 T", "C08", "$12.600"],
    ["CP08", "P6 F", "C25", "ValueError (spec)"],
    ["CP09", "P7 T", "C15", "$11.000"],
    ["CP10", "P8 T", "C10", "$8.600"],
    ["CP11", "P9 T", "C11", "$7.700"],
    ["CP12", "P10 T, P11 T", "C12", "$8.100"],
    ["CP13", "P11 F", "C19", "ValueError (spec)"],
    ["CP14", "P12 T", "C30", "$5.000"],
    ["CP15", "P13 T (flag)", "sonda", "imprime y retorna"],
]
story.append(T(caminos, [1.4 * cm, 10.4 * cm, 1.6 * cm, 3.6 * cm], tam=7.2))
P("Los caminos CP08 y CP13 existen solo en el heredado porque faltan las "
  "validaciones de zona y cupón (DEF-01 y DEF-05). Tras la corrección, esos "
  "caminos desaparecen y los casos verifican el error en la validación.")

# ---------------------------------------------------------------------------
# 7. Defectos
# ---------------------------------------------------------------------------
H1("7. Defectos detectados")
defectos = [
    ["ID", "Título", "Req.", "Severidad", "Prioridad"],
    ["DEF-01", "No valida zonas desconocidas", "R2", "Alta", "Alta"],
    ["DEF-02", "No valida el día (fuera de 1–7 o no entero)", "R2", "Alta", "Alta"],
    ["DEF-03", "El fin de semana usa d > 6 y excluye el sábado", "R5", "Alta", "Alta"],
    ["DEF-04", "Recargo de fin de semana antes de los descuentos", "R5 (E impar)", "Alta", "Media"],
    ["DEF-05", "Ignora cupones inexistentes en vez de lanzar error", "R7 (F impar)", "Media", "Alta"],
    ["DEF-06", "Trunca con int() en vez de redondear half-up", "R8", "Alta", "Alta"],
    ["DEF-07", "Mensaje de peso inválido sin tilde", "R1", "Baja", "Baja"],
]
story.append(T(defectos, [1.6 * cm, 8.2 * cm, 2.2 * cm, 2.5 * cm, 2.5 * cm], tam=7.6))
P("Total: 7 defectos (5 de severidad alta, 1 media y 1 baja). La densidad es "
  "7 / 41 líneas ≈ 17,1 defectos por 100 líneas, o 7 / 29 sentencias ≈ 24,1 por "
  "100 sentencias. La suite inicial tenía 36 pruebas: 14 pasaban y 22 fallaban.")
H2("7.1 Ejemplo: DEF-04")
P("El heredado aplica el recargo de fin de semana antes de los descuentos. Con "
  "E impar, el orden correcto es descuentos y luego finde. Para 5 kg, urbana, "
  "ninguno, domingo, ENVIO10:")
CODE("Heredado: 9000 + 2000 = 11000; 11000 * 0.90 = 9900\n"
     "Esperado:  9000 * 0.90 = 8100; 8100 + 2000 = 10100")
P("El caso C18 y la prueba `test_def04_orden_finde.py` fijan el comportamiento "
  "correcto y evitan la regresión.")
H2("7.2 Falsos positivos descartados")
P("Se revisó y descartó: PMAX=50 (coincide con la especificación), el límite "
  "del tramo 1, la aplicación de ambos descuentos y la precisión de float (no "
  "se encontraron diferencias en los casos probados). Solo se reportan los "
  "siete defectos reales.")

# ---------------------------------------------------------------------------
# 8. Correcciones y TDD
# ---------------------------------------------------------------------------
H1("8. Correcciones con TDD")
P("Cada defecto se corrigió en su propia rama, con dos commits: una prueba que "
  "reproduce el fallo (rojo) y la corrección que la pone en verde. Después se "
  "integró a main con merge --no-ff para conservar la trazabilidad.")
ramas = [
    ["Defecto", "Rama", "Contenido"],
    ["DEF-01", "fix/DEF-01", "Prueba de zona inválida + validación"],
    ["DEF-02", "fix/DEF-02", "Prueba de día inválido + validación"],
    ["DEF-03", "fix/DEF-03", "Sábado con recargo (d >= 6)"],
    ["DEF-04", "fix/DEF-04", "Finde después de descuentos"],
    ["DEF-05", "fix/DEF-05", "Cupón inexistente lanza error"],
    ["DEF-06", "fix/DEF-06", "Redondeo half-up con Decimal"],
    ["DEF-07", "fix/DEF-07", "Mensaje 'peso inválido' con tilde"],
]
story.append(T(ramas, [1.8 * cm, 3.6 * cm, 11.6 * cm], tam=8))
P("Resultado: 43/43 pruebas en verde y 100 % de cobertura de sentencias y "
  "ramas en v2.0.0. La evidencia roja del heredado y la verde del refactor "
  "están en `evidence/`.")

# ---------------------------------------------------------------------------
# 9. Refactorización
# ---------------------------------------------------------------------------
story.append(PageBreak())
H1("9. Refactorización (v2.0.0)")
P("Se identificaron trece malos olores. La tabla resume los principales y la "
  "técnica aplicada.")
olores = [
    ["#", "Mal olor", "Refactor aplicado"],
    ["1", "Números mágicos", "Constantes nombradas para tarifas, recargos y mínimo"],
    ["2", "Nombres crípticos (p, z, c, d, cup, t)", "Nombres descriptivos"],
    ["3", "Argumento bandera (flag)", "Se elimina; calc es pura y no imprime"],
    ["4", "Sentencia inútil (t = t)", "Se elimina"],
    ["5", "Comparación cup != None", "Se usa is not None"],
    ["6", "Cadena de if/elif para zonas y descuentos", "Patrón Strategy"],
    ["7", "Función larga con múltiples responsabilidades", "Se divide en funciones pequeñas"],
    ["8", "E/S mezclada con lógica (print)", "La impresión pasa al llamador"],
    ["9", "Estado global mutable (CONFIG)", "Constantes inmutables y parámetros"],
    ["10", "Fórmula de descuento duplicada", "Helper y estrategias"],
    ["11", "Falta de tipos y documentación", "Type hints y docstrings"],
    ["12", "Redondeo por truncamiento", "Decimal + ROUND_HALF_UP"],
    ["13", "Error genérico y mensaje ambiguo", "ErrorEnvio con mensaje específico"],
]
story.append(T(olores, [0.8 * cm, 7.4 * cm, 8.8 * cm], tam=7.4))
H2("9.1 Diagrama de clases")
story.append(IMG("evidence/uml_clases.png", max_w=16.5 * cm, max_h=12 * cm))
H2("9.2 Métricas antes y después")
metricas = [
    ["Métrica", "v1.0.0", "v2.0.0", "Variación"],
    ["Complejidad máxima por bloque", "15", "3", "-80 %"],
    ["Complejidad promedio", "15,0", "1,76", "-88 %"],
    ["Bloques (funciones/clases/métodos)", "1", "25", "+24"],
    ["SLOC", "37", "129", "+92"],
    ["Líneas físicas", "41", "197", "+156"],
    ["Cobertura de sentencias", "96 %", "100 %", "+4 pp"],
    ["Pruebas", "36 (14 pasan)", "43 (43 pasan)", "+7"],
    ["Globales mutables", "CONFIG (7 claves)", "0", "-7"],
    ["API pública", "calc(..., flag)", "calc(...)", "sin flag"],
]
story.append(T(metricas, [6.2 * cm, 3.6 * cm, 3.8 * cm, 3.4 * cm], tam=7.8))
P("El SLOC sube porque el diseño explícito cuesta líneas, pero cada bloque es "
  "mucho más simple: el máximo baja de 15 a 3 y el promedio de 15,0 a 1,76. La "
  "deuda se paga en volumen, no en complejidad.")

# ---------------------------------------------------------------------------
# 10. Configuración
# ---------------------------------------------------------------------------
H1("10. Gestión de la configuración")
P("Los parámetros viven como constantes de módulo, sin estado global mutable, "
  "sin archivos .env y sin secretos. La documentación y la calculadora de "
  "referencia repiten los mismos valores; la suite los verifica.")
config = [
    ["Parámetro", "v1.0.0", "v2.0.0", "v2.1.0"],
    ["PMAX", "50 literal", "PMAX = 50", "PMAX = 50"],
    ["L1 / L2", "CONFIG", "constantes", "constantes"],
    ["RR / RN", "CONFIG", "constantes", "constantes"],
    ["Descuento frecuente", "0.05 literal", "DESC_FRECUENTE", "DESC_FRECUENTE"],
    ["Descuento cupón", "0.10 literal", "DESC_CUPON", "DESC_CUPON"],
    ["Mínimo", "5000 literal", "COSTO_MINIMO", "COSTO_MINIMO"],
    ["Redondeo", "int(t/100)*100", "half-up", "half-up"],
    ["CAMBIO", "no existe", "no aplica", "CAMBIO = 1"],
    ["Cliente empresarial", "no existe", "no existe", "12 % y sin zona > L2"],
]
story.append(T(config, [4.2 * cm, 3.8 * cm, 4.2 * cm, 4.8 * cm], tam=7.8))
P("Procedimiento ante un cambio de parámetro: editar la constante, actualizar "
  "docs/00 y la calculadora de referencia, ajustar las pruebas, ejecutar la "
  "suite con cobertura, registrar en CHANGELOG y crear el tag SemVer.")

# ---------------------------------------------------------------------------
# 11. Cambio CAMBIO=1
# ---------------------------------------------------------------------------
H1("11. Gestión del cambio: CAMBIO=1")
P("El cambio solicitado en la Parte 8 se implementó en la rama "
  "feature/cambio-1 y se entregó en v2.1.0. Tiene dos reglas: cliente "
  "empresarial con 12 % de descuento y exención del recargo de zona cuando el "
  "peso supera L2.")
H2("11.1 Decisiones de interpretación")
B("El 12 % se aplica después del recargo de zona y antes del cupón.")
B("El finde se suma después de los descuentos, como exige E impar.")
B("'Peso > L2' es estricto: en 10 kg exactos sí se cobra recargo de zona.")
B("La exención de zona aplica a todos los clientes, no solo al empresarial.")
B("El mínimo de 5000 se aplica al final, antes del redondeo.")
H2("11.2 Casos nuevos")
nuevos = [
    ["Caso", "Entrada", "Cálculo", "Esperado"],
    ["C33", "10,1 · nacional · ninguno", "base 9080; sin zona", "$9.100"],
    ["C34", "5 · urbana · empresarial", "9000 × 0,88", "$7.900"],
    ["C35", "5 · urbana · empresarial · ENVIO10", "7920 × 0,90", "$7.100"],
    ["C36", "5 · rural · empresarial · sábado", "9000 × 1,15 × 0,88 + 2000", "$11.100"],
    ["C37", "11 · rural · empresarial", "sin zona: 9800 × 0,88", "$8.600"],
    ["C38", "11 · nacional · ninguno", "sin zona: 9800", "$9.800"],
    ["C39", "10 · nacional · ninguno", "9000 × 1,40 (L2 exacto)", "$12.600"],
    ["C40", "10,1 · rural · ninguno", "sin zona: 9080", "$9.100"],
    ["C41", "5 · urbana · empresarial · sábado", "7920 + 2000", "$9.900"],
    ["C42", "2 · urbana · empresarial · ENVIO10", "4752 → mínimo", "$5.000"],
]
story.append(T(nuevos, [1.4 * cm, 6.6 * cm, 5.8 * cm, 3.2 * cm], tam=7.4))
P("Resultado: 55/55 pruebas en verde y 100 % de cobertura. El cambio no rompe "
  "la firma de calc; solo agrega un valor válido de cliente y modifica los "
  "casos con peso > L2 en zona rural o nacional.")

# ---------------------------------------------------------------------------
# 12. Evidencias
# ---------------------------------------------------------------------------
story.append(PageBreak())
H1("12. Evidencias")
H2("12.1 Heredado v1.0.0: 36 pruebas, 14 pasan y 22 fallan")
story.append(IMG("evidence/v1.0.0_pytest.png", max_w=16.5 * cm, max_h=9 * cm))
H2("12.2 Versión final v2.1.0: 55 pruebas en verde y 100 % de cobertura")
story.append(IMG("evidence/v2.1.0_pytest.png", max_w=16.5 * cm, max_h=7 * cm))
P("Los archivos de texto y las imágenes completas están en `evidence/`. El "
  "repositorio conserva las ramas, los merges --no-ff y los tags v1.0.0, v2.0.0 "
  "y v2.1.0.")

# ---------------------------------------------------------------------------
# 13. Conclusiones
# ---------------------------------------------------------------------------
H1("13. Conclusiones")
B("Se construyó una especificación verificable y se derivaron 33 casos de caja negra y 15 caminos de caja blanca.")
B("La suite inicial evidenció 7 defectos reales; la densidad fue 17,1 por 100 líneas.")
B("Las correcciones con TDD y ramas independientes dejaron 43 pruebas en verde en v2.0.0.")
B("El refactor redujo la complejidad máxima de 15 a 3 y la promedio de 15,0 a 1,76, con 100 % de cobertura.")
B("La gestión del cambio CAMBIO=1 se integró sin romper la API y elevó la suite a 55 pruebas.")
B("La trazabilidad se apoya en ramas, merges --no-ff, tags SemVer, CHANGELOG y evidencias.")
H2("Trabajo futuro")
B("Validar el nombre del cliente (hoy un valor desconocido se trata como 'ninguno').")
B("Leer CAMBIO de configuración externa si el cliente lo requiere.")
B("Agregar pruebas de mutación o de propiedades para complementar la cobertura.")

# ---------------------------------------------------------------------------
# 14. Anexos
# ---------------------------------------------------------------------------
H1("14. Anexos")
H2("14.1 Repositorio y versiones")
P("Repositorio: https://github.com/FREY3R/parcial-ing-.git")
P("Tags: v1.0.0 (heredado), v2.0.0 (correcciones + refactor), v2.1.0 (CAMBIO=1).")
H2("14.2 Comandos de verificación")
CODE("python -m pytest -q\n"
     "python -m pytest -q --cov=envios --cov-branch --cov-report=term-missing\n"
     "python -m radon cc envios.py -s -a\n"
     "python docs/grafo_flujo.py\n"
     "python docs/uml_clases.py\n"
     "python docs/render_evidencia.py evidence/v2.1.0_pytest.txt evidence/v2.1.0_pytest.png\n"
     "python docs/generar_informe.py")
H2("14.3 Estructura del repositorio")
CODE("envios.py                  Implementación v2.1.0\n"
     "tests/test_envios.py       Suite principal (55 pruebas)\n"
     "tests/test_def01..07_*.py  Regresiones TDD por defecto\n"
     "docs/00..08_*.md           Documentación del parcial\n"
     "docs/referencia_calculo.py Calculadora Decimal independiente\n"
     "docs/grafo_flujo.py        Genera el grafo de flujo\n"
     "docs/uml_clases.py         Genera el UML de clases\n"
     "docs/render_evidencia.py   Convierte salidas de pytest a PNG\n"
     "docs/generar_informe.py    Genera este PDF\n"
     "evidence/                  Evidencias txt y png\n"
     "CHANGELOG.md               Historial de versiones\n"
     "README.md                  Guía de uso\n"
     "SUSTENTACION.md            Guion de la exposición")
P("Fin del informe.", "Note")


def main():
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.9 * cm,
        title="Informe Parcial 3 — 0182410093",
        author="Yerfreth Mejía Sierra",
        subject="Ingeniería de Software I — Parcial 3",
    )
    doc.build(story, onFirstPage=pie, onLaterPages=pie)
    print(f"PDF generado: {OUT}")


if __name__ == "__main__":
    main()
