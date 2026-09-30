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
├── listado_tabla.html      Catálogo de productos en formato tabla (con filtro por categoría/ofertas)
├── listado_box.html        Catálogo de productos en formato box/tarjetas (con filtro por categoría/ofertas)
├── producto.html           Ficha de producto dinámica (lee ?id= de la URL)
├── comprar.html            Formulario de compra (incluye cupón de descuento)
├── inventario.html         Panel interno de inventario (módulo TP2, ver sección abajo)
├── styles.css              Hoja de estilos compartida por todas las páginas
├── products.js             Catálogo de productos — fuente única de datos (16 productos, 8 categorías)
├── stock.json              Datos de stock consumidos por app.js vía fetch() (simula un servidor)
├── cart.js                 Lógica del carrito (JS del lado del cliente, sin backend)
├── app.js                  Lógica del panel de inventario (fetch + addEventListener)
├── analisis-diseno.pdf     Documento de análisis y diseño (avance) para la entrega
├── build_pdf.py            Script que genera analisis-diseno.pdf (opcional, no se sube al repo)
└── README.md               Este archivo
```

## Decisiones de diseño (para el documento de análisis)

- **Paleta:** verde pino (`#16281C`) como color de marca/header, mustaza (`#E8A93B`) como acento de precios y CTA, tomate (`#C0472B`) para ofertas/stock bajo, sobre un fondo verde salvia muy claro (`#F1F4EC`).
- **Tipografía:** `Bitter` (serif, tipo cartel de almacén) para títulos, `Mulish` (sans-serif) para texto y componentes de interfaz.
- **Layout:** alineación mayormente a la izquierda, grillas de 4 columnas para categorías y productos, navegación fija (sticky) en la parte superior.
- **Componentes reutilizables:** `.btn`, `.product-card`, `table.products`, `.cat-card`, `.pay-option`, `.cart-list` — todos definidos en `styles.css` para mantener consistencia entre páginas.
- **Alcance:** maquetado en HTML/CSS (lo que se evalúa) + una capa de JavaScript del lado del cliente para que el flujo se sienta real: `products.js` centraliza el catálogo (16 productos en 8 categorías) como única fuente de datos, `producto.html` lee el producto a mostrar desde la URL (`?id=...`) en vez de tener contenido fijo, y `listado_tabla.html`/`listado_box.html` filtran de verdad por categoría (`?cat=...`) o por ofertas (`?filter=ofertas`) según el link que se haya clickeado. Los botones "Agregar" suman productos a un carrito guardado en el navegador (`localStorage`), `comprar.html` muestra ese carrito con sus totales, y el formulario valida los campos obligatorios y el pedido antes de confirmar. No hay backend ni base de datos — todo corre en el navegador.

## Módulo TP2 — Panel de inventario (`inventario.html` / `app.js`)

Segunda entrega sobre el mismo proyecto: enriquece el sitio con un módulo interno para el personal, cumpliendo el requisito transversal de JavaScript de la consigna.

- **Desacoplamiento:** ningún `onclick`/`onsubmit` en el HTML. Todos los listeners se agregan en `app.js` con `addEventListener()` (incluida delegación de eventos para los botones +/− generados dinámicamente).
- **Asincronía real:** el stock se consulta con `fetch()` + `async/await` contra `stock.json`, que simula la respuesta de un servidor.
- **Alerta de estado crítico:** cada producto cuya cantidad cae por debajo de su umbral se marca visualmente (`.stock-critico`, badge "⚠ Stock crítico") y se cuenta en un banner y en el resumen.
- **Fundamentación U1 — VSDM:** el mismo panel expone dos vistas según el rol elegido en un selector (Cliente / Empleado): la vista Cliente solo informa disponibilidad, la vista Empleado muestra cantidades exactas y controles para ajustar stock. Es una simulación en el cliente (sin login real) para argumentar el modelo de vistas separadas por rol de acceso; el detalle está documentado dentro de la propia página, al final de `inventario.html`.

## Cómo verlo

Abrir `index.html` en el navegador. La mayoría de las páginas no requieren servidor, pero `inventario.html` sí, porque `fetch()` a `stock.json` necesita `http://` (no `file://`) para no toparse con el mismo bloqueo de seguridad del navegador que ya documentamos para `localStorage`. Alcanza con levantar un servidor simple en la carpeta del proyecto (por ejemplo `python -m http.server 8000`) y abrir `http://localhost:8000`.
