# Mercado Fresco — Tienda online de supermercado de barrio

Proyecto para la materia **Paradigmas y Lenguajes de Programación III**.
Entregable: maquetado en HTML5 + CSS3 (sin frameworks) del flujo de compra de un supermercado de barrio.

## Requerimiento funcional (RF) resuelto

**RF-01 — Consulta de catálogo y generación de pedido de compra.**
El cliente debe poder consultar el catálogo de productos del supermercado (en formato tabla o en formato de tarjetas), acceder a la ficha detallada de un producto puntual, y completar un formulario para generar un pedido de compra con sus datos de contacto, dirección de entrega, medio de pago y el listado de productos elegidos.

### Alcance de la pantalla `comprar.html`
Datos solicitados según consigna:
- Nombre del cliente
- Dirección
- Teléfono
- E-mail
- Medio de pago (efectivo / tarjeta / transferencia)
- Listado de productos del pedido (resumen con cantidades y totales)

## Estructura de archivos

```
mercado-fresco/
├── index.html              Portada principal
├── listado_tabla.html      Catálogo de productos en formato tabla
├── listado_box.html        Catálogo de productos en formato box/tarjetas
├── producto.html           Ficha de un producto en particular
├── comprar.html            Formulario de compra
├── styles.css              Hoja de estilos compartida por todas las páginas
├── cart.js                 Lógica del carrito (JS del lado del cliente, sin backend)
├── analisis-diseno.pdf     Documento de análisis y diseño (avance) para la entrega
├── build_pdf.py            Script que genera analisis-diseno.pdf (opcional, no se sube al repo)
└── README.md               Este archivo
```

## Decisiones de diseño (para el documento de análisis)

- **Paleta:** verde pino (`#16281C`) como color de marca/header, mustaza (`#E8A93B`) como acento de precios y CTA, tomate (`#C0472B`) para ofertas/stock bajo, sobre un fondo verde salvia muy claro (`#F1F4EC`).
- **Tipografía:** `Bitter` (serif, tipo cartel de almacén) para títulos, `Mulish` (sans-serif) para texto y componentes de interfaz.
- **Layout:** alineación mayormente a la izquierda, grillas de 4 columnas para categorías y productos, navegación fija (sticky) en la parte superior.
- **Componentes reutilizables:** `.btn`, `.product-card`, `table.products`, `.cat-card`, `.pay-option`, `.cart-list` — todos definidos en `styles.css` para mantener consistencia entre páginas.
- **Alcance:** maquetado en HTML/CSS (lo que se evalúa) + una capa de JavaScript del lado del cliente para que el flujo se sienta real: los botones "Agregar" suman productos a un carrito guardado en el navegador (`localStorage`), `comprar.html` muestra ese carrito con sus totales, y el formulario valida los campos obligatorios y el pedido antes de confirmar. No hay backend ni base de datos — todo corre en el navegador.

## Cómo verlo

Abrir `index.html` en el navegador. No requiere servidor ni instalación.
