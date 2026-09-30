# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    ListFlowable, ListItem, PageBreak, HRFlowable
)

PINE = colors.HexColor("#16281C")
MUSTARD = colors.HexColor("#E8A93B")
TOMATO = colors.HexColor("#C0472B")
INK = colors.HexColor("#221F1A")
INK_SOFT = colors.HexColor("#5A5548")
LINE = colors.HexColor("#DCE0D2")
SAGE = colors.HexColor("#F1F4EC")

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name="CoverTitle", fontName="Helvetica-Bold", fontSize=27,
    leading=32, textColor=PINE, alignment=TA_CENTER, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="CoverSub", fontName="Helvetica", fontSize=13,
    leading=18, textColor=INK_SOFT, alignment=TA_CENTER, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="H1", fontName="Helvetica-Bold", fontSize=17,
    leading=21, textColor=PINE, spaceBefore=18, spaceAfter=10,
))
styles.add(ParagraphStyle(
    name="H2", fontName="Helvetica-Bold", fontSize=13,
    leading=17, textColor=PINE, spaceBefore=12, spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="Body", fontName="Helvetica", fontSize=10.3,
    leading=15.5, textColor=INK, alignment=TA_LEFT, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="BodyBold", parent=styles["Body"], fontName="Helvetica-Bold",
    textColor=PINE,
))
styles.add(ParagraphStyle(
    name="Small", fontName="Helvetica", fontSize=8.7,
    leading=12, textColor=INK_SOFT,
))
styles.add(ParagraphStyle(
    name="TableHead", fontName="Helvetica-Bold", fontSize=9.3,
    leading=12, textColor=colors.white,
))
styles.add(ParagraphStyle(
    name="TableCell", fontName="Helvetica", fontSize=9.3,
    leading=12.5, textColor=INK,
))
styles.add(ParagraphStyle(
    name="MyBullet", parent=styles["Body"], leftIndent=0, spaceAfter=4,
))

story = []

# ---------- Portada ----------
story.append(Spacer(1, 4.5 * cm))
story.append(Paragraph("MERCADO FRESCO", styles["CoverTitle"]))
story.append(Paragraph("Documento de Análisis y Diseño — Avance", styles["CoverSub"]))
story.append(Spacer(1, 0.6 * cm))
story.append(HRFlowable(width="40%", thickness=1.4, color=MUSTARD, hAlign="CENTER"))
story.append(Spacer(1, 1.2 * cm))
story.append(Paragraph("Tienda online de un supermercado / almacén de barrio", styles["CoverSub"]))
story.append(Spacer(1, 3.5 * cm))

cover_table = Table(
    [
        ["Materia", "Paradigmas y Lenguajes de Programación III"],
        ["Trabajo práctico", "Maquetado HTML5 / CSS3 — Frontend"],
        ["Integrantes", "Acosta, Leandro\nRomero Baylac, Santiago\nRomero Baylac, Tomas"],
        ["Grupo", "Grupo D"],
        ["Fecha", "02/09/2026"],
    ],
    colWidths=[4.2 * cm, 10.3 * cm],
)
cover_table.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("TEXTCOLOR", (0, 0), (0, -1), PINE),
    ("TEXTCOLOR", (1, 0), (1, -1), INK),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ("TOPPADDING", (0, 0), (-1, -1), 10),
    ("LINEBELOW", (0, 0), (-1, -1), 0.6, LINE),
]))
story.append(cover_table)
story.append(PageBreak())

# ---------- 1. Introducción ----------
story.append(Paragraph("1. Descripción del proyecto", styles["H1"]))
story.append(Paragraph(
    "Mercado Fresco es la propuesta de tienda online de un supermercado / almacén de barrio. "
    "El proyecto original planteaba una aplicación de gestión de stock; se reformuló el enfoque "
    "hacia la experiencia del cliente final que navega el catálogo y realiza un pedido de compra, "
    "que es el flujo que exige esta entrega. El dominio (productos, categorías, precios, stock) "
    "se mantiene: lo que cambia es el punto de vista, desde el back-office hacia el mostrador digital.",
    styles["Body"],
))
story.append(Paragraph(
    "En esta primera etapa se resuelve el maquetado en HTML5 y CSS3 de las pantallas principales "
    "del flujo de compra, sin lógica de servidor. La interacción de agregar productos al carrito y "
    "completar el pedido está resuelta con JavaScript del lado del cliente (sin backend), a modo de "
    "prueba de concepto del flujo completo.",
    styles["Body"],
))

story.append(Paragraph("1.1 Objetivo general", styles["H2"]))
story.append(Paragraph(
    "Permitir que un cliente consulte el catálogo de productos de un supermercado de barrio, vea el "
    "detalle de un producto puntual y genere un pedido de compra indicando sus datos de contacto, "
    "dirección de entrega y medio de pago.",
    styles["Body"],
))

# ---------- 2. RF ----------
story.append(Paragraph("2. Requerimiento funcional (RF) resuelto", styles["H1"]))
story.append(Paragraph(
    "<b>RF-01 — Consulta de catálogo y generación de pedido de compra.</b> El sistema debe permitir "
    "al cliente consultar el catálogo de productos disponibles (en formato tabla y en formato de "
    "tarjetas), acceder a la ficha detallada de un producto en particular, y completar un formulario "
    "de compra indicando: nombre del cliente, dirección, teléfono, e-mail, medio de pago y el listado "
    "de productos elegidos con sus cantidades y totales.",
    styles["Body"],
))

story.append(Paragraph("2.1 Criterios de aceptación", styles["H2"]))
criterios = [
    "El cliente puede ver todos los productos en una tabla, con nombre, categoría, unidad, precio y stock.",
    "El cliente puede ver los mismos productos en formato de tarjetas (box), con imagen/ícono, nombre y precio.",
    "El cliente puede acceder a la ficha de un producto puntual con su descripción, precio, stock y selector de cantidad.",
    "El cliente puede agregar productos a un pedido y ver el resumen actualizado (subtotal, envío y total).",
    "El cliente puede completar el formulario de compra con nombre, dirección, teléfono, e-mail y medio de pago, y confirmar el pedido.",
    "El formulario valida que los campos obligatorios estén completos y que el pedido no esté vacío antes de confirmar.",
]
story.append(ListFlowable(
    [ListItem(Paragraph(c, styles["MyBullet"]), leftIndent=12) for c in criterios],
    bulletType="bullet", start="•", bulletColor=MUSTARD.clone() if hasattr(MUSTARD, "clone") else MUSTARD,
))

# ---------- 3. Actores ----------
story.append(Paragraph("3. Actores", styles["H1"]))
actor_data = [
    [Paragraph("Actor", styles["TableHead"]), Paragraph("Descripción", styles["TableHead"])],
    [Paragraph("Cliente", styles["TableCell"]), Paragraph(
        "Persona que navega el sitio, consulta productos y genera un pedido de compra.", styles["TableCell"])],
    [Paragraph("Sistema (frontend)", styles["TableCell"]), Paragraph(
        "Presenta el catálogo, calcula subtotales/totales y valida el formulario en el navegador, "
        "sin conexión a un servidor en esta etapa.", styles["TableCell"])],
]
actor_table = Table(actor_data, colWidths=[4 * cm, 10.5 * cm])
actor_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PINE),
    ("BACKGROUND", (0, 1), (-1, -1), colors.white),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [SAGE, colors.white]),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(actor_table)

# ---------- 4. Mapa de navegación ----------
story.append(Paragraph("4. Mapa de navegación", styles["H1"]))
story.append(Paragraph(
    "Las cinco pantallas se enlazan entre sí mediante un menú de navegación fijo, presente en todas "
    "las páginas:",
    styles["Body"],
))
nav_flow = [
    "index.html (Portada) → listado_tabla.html / listado_box.html (catálogo)",
    "listado_tabla.html / listado_box.html → producto.html (ficha de un producto)",
    "producto.html → comprar.html (formulario de compra, con el producto ya agregado)",
    "comprar.html → confirmación de pedido (dentro de la misma pantalla)",
]
story.append(ListFlowable(
    [ListItem(Paragraph(c, styles["MyBullet"]), leftIndent=12) for c in nav_flow],
    bulletType="bullet", start="•",
))

# ---------- 5. Pantallas ----------
story.append(Paragraph("5. Diseño de pantallas", styles["H1"]))

pantallas = [
    ("index.html — Portada principal",
     "Presenta la propuesta del supermercado: mensaje principal (hero), franja de ofertas, grilla de "
     "categorías (frutas y verduras, lácteos, carnicería, panadería, limpieza, almacén, bebidas, kiosco) "
     "y una selección de productos destacados con acceso directo a agregarlos al pedido."),
    ("listado_tabla.html — Catálogo en tabla",
     "Lista completa de productos en una tabla con columnas: producto, categoría, unidad, precio y stock "
     "disponible, con indicador visual cuando el stock es bajo. Cada fila permite agregar el producto "
     "al pedido o ver su ficha."),
    ("listado_box.html — Catálogo en grilla (box)",
     "Los mismos productos que en la tabla, presentados como tarjetas con ícono, categoría, nombre, "
     "unidad de venta, precio y botón para agregar al pedido. Pensada para una navegación más visual."),
    ("producto.html — Ficha de producto",
     "Detalle de un producto puntual: imagen, categoría, descripción, precio (con descuento cuando "
     "corresponde), stock disponible, origen, selector de cantidad y botón para agregarlo al pedido "
     "y continuar hacia el formulario de compra."),
    ("comprar.html — Formulario de compra",
     "Formulario con los datos exigidos por la consigna (nombre, dirección, teléfono, e-mail, medio de "
     "pago) y un resumen del pedido con el listado de productos agregados, cantidades, subtotal, envío "
     "y total. Valida los campos obligatorios y muestra una confirmación al enviar."),
]
for titulo, desc in pantallas:
    story.append(Paragraph(titulo, styles["H2"]))
    story.append(Paragraph(desc, styles["Body"]))

# ---------- 6. Diseño visual ----------
story.append(Paragraph("6. Decisiones de diseño visual", styles["H1"]))

story.append(Paragraph("6.1 Paleta de colores", styles["H2"]))
paleta_data = [
    [Paragraph("Color", styles["TableHead"]), Paragraph("Uso", styles["TableHead"]), Paragraph("Hex", styles["TableHead"])],
    [Paragraph("Verde pino", styles["TableCell"]), Paragraph("Marca, encabezado, botones principales", styles["TableCell"]), Paragraph("#16281C", styles["TableCell"])],
    [Paragraph("Mustaza", styles["TableCell"]), Paragraph("Precios, llamados a la acción (CTA)", styles["TableCell"]), Paragraph("#E8A93B", styles["TableCell"])],
    [Paragraph("Tomate", styles["TableCell"]), Paragraph("Ofertas, alertas de stock bajo", styles["TableCell"]), Paragraph("#C0472B", styles["TableCell"])],
    [Paragraph("Verde salvia claro", styles["TableCell"]), Paragraph("Fondo general de la página", styles["TableCell"]), Paragraph("#F1F4EC", styles["TableCell"])],
]
paleta_table = Table(paleta_data, colWidths=[4 * cm, 7.2 * cm, 3.3 * cm])
paleta_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [SAGE, colors.white]),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(paleta_table)

story.append(Paragraph("6.2 Tipografía", styles["H2"]))
story.append(Paragraph(
    "<b>Bitter</b> (serif, estilo cartel de almacén) para títulos y <b>Mulish</b> (sans-serif) para "
    "texto de cuerpo y componentes de interfaz, con el fin de transmitir un carácter cercano a un "
    "comercio de barrio sin perder legibilidad en pantalla.",
    styles["Body"],
))

story.append(Paragraph("6.3 Layout", styles["H2"]))
story.append(Paragraph(
    "Alineación mayormente a la izquierda, grillas de 4 columnas para categorías y productos "
    "(2 columnas en tablets, 1-2 en celulares), navegación superior fija (sticky) presente en las "
    "cinco pantallas, y componentes reutilizables (botones, tarjetas de producto, tabla de catálogo, "
    "tarjetas de resumen) definidos una sola vez en la hoja de estilos compartida.",
    styles["Body"],
))

# ---------- 7. Tecnología ----------
story.append(Paragraph("7. Tecnologías utilizadas", styles["H1"]))
tec_data = [
    [Paragraph("Tecnología", styles["TableHead"]), Paragraph("Uso en el proyecto", styles["TableHead"])],
    [Paragraph("HTML5", styles["TableCell"]), Paragraph("Estructura semántica de las 5 pantallas.", styles["TableCell"])],
    [Paragraph("CSS3", styles["TableCell"]), Paragraph("Estilos, layout con Grid/Flexbox y diseño responsive, en una hoja compartida (styles.css).", styles["TableCell"])],
    [Paragraph("JavaScript (vanilla)", styles["TableCell"]), Paragraph("Carrito de compras en el navegador (localStorage), validación del formulario y actualización dinámica de totales. No hay backend ni base de datos en esta etapa.", styles["TableCell"])],
]
tec_table = Table(tec_data, colWidths=[4.2 * cm, 10.3 * cm])
tec_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PINE),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [SAGE, colors.white]),
    ("GRID", (0, 0), (-1, -1), 0.5, LINE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(tec_table)

# ---------- 8. Estructura de archivos ----------
story.append(Paragraph("8. Estructura del repositorio", styles["H1"]))
estructura = """mercado-fresco/
├── index.html            Portada principal
├── listado_tabla.html    Catálogo de productos en formato tabla
├── listado_box.html      Catálogo de productos en formato box / tarjetas
├── producto.html         Ficha de un producto en particular
├── comprar.html          Formulario de compra
├── styles.css            Hoja de estilos compartida
├── cart.js               Lógica del carrito (cliente, sin backend)
└── README.md             Notas técnicas del proyecto"""
story.append(Paragraph(estructura.replace("\n", "<br/>").replace(" ", "&nbsp;"), styles["Small"]))

# ---------- 9. Próximos pasos ----------
story.append(Paragraph("9. Próximos pasos", styles["H1"]))
proximos = [
    "Incorporar más requerimientos funcionales del proyecto original (por ejemplo, gestión de stock desde un panel administrativo).",
    "Definir el modelo de datos (productos, categorías, pedidos) para una futura conexión a backend.",
    "Sumar validaciones adicionales y manejo de errores en el formulario de compra.",
    "Evaluar la incorporación de imágenes reales de producto en reemplazo de los íconos utilizados en este avance.",
]
story.append(ListFlowable(
    [ListItem(Paragraph(c, styles["MyBullet"]), leftIndent=12) for c in proximos],
    bulletType="bullet", start="•",
))

story.append(Spacer(1, 0.6 * cm))
story.append(HRFlowable(width="100%", thickness=0.6, color=LINE))
story.append(Spacer(1, 0.3 * cm))
story.append(Paragraph(
    "Documento de avance — Paradigmas y Lenguajes de Programación III. Se evalúa el maquetado en HTML y CSS.",
    styles["Small"],
))

doc = SimpleDocTemplate(
    "analisis-diseno.pdf", pagesize=A4,
    leftMargin=2.2 * cm, rightMargin=2.2 * cm,
    topMargin=2 * cm, bottomMargin=2 * cm,
    title="Mercado Fresco - Analisis y Diseno",
)
doc.build(story)
print("PDF generado")
