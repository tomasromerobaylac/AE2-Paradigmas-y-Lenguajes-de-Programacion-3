document.addEventListener("DOMContentLoaded", () => {
  let catalogo = [];

  const inputBuscador = document.getElementById("input-buscador");
  const contenedorGrid = document.getElementById("box-grid-container") || document.querySelector(".box-grid");

  const params = new URLSearchParams(window.location.search);
  const catSlug = params.get("cat");
  const onlyOffers = params.get("filter") === "ofertas";

  async function cargarCatalogo() {
    try {
      const respuesta = await fetch("./productos.json");
      if (!respuesta.ok) {
        throw new Error(`Error HTTP: ${respuesta.status}`);
      }
      catalogo = await respuesta.json();

      let productosAFiltrar = catalogo;
      if (catSlug) {
        productosAFiltrar = productosAFiltrar.filter((p) => p.categorySlug === catSlug);
      }
      if (onlyOffers) {
        productosAFiltrar = productosAFiltrar.filter((p) => p.discount === true);
      }

      renderizarTarjetas(productosAFiltrar);
    } catch (error) {
      console.error("Fallo al cargar el catálogo:", error);
      if (contenedorGrid) {
        contenedorGrid.innerHTML = `
          <p style="grid-column: 1 / -1; padding: 24px 4px; color: var(--ink-soft, #666);">
            No se pudieron cargar los productos en este momento.
          </p>
        `;
      }
    }
  }

  function renderizarTarjetas(productos) {
    if (!contenedorGrid) return;

    contenedorGrid.innerHTML = "";

    if (productos.length === 0) {
      contenedorGrid.innerHTML = `
        <p style="grid-column: 1 / -1; padding: 24px 4px; color: var(--ink-soft, #666);">
          No se encontraron productos que coincidan con la búsqueda.
        </p>
      `;
      return;
    }

    productos.forEach((item) => {
      let badgeHtml = "";
      if (item.discount) {
        badgeHtml = '<span class="badge">-15%</span>';
      } else if (item.stockLevel === "low") {
        badgeHtml = '<span class="badge">Poco stock</span>';
      }

      const unidadTexto = item.unit === "un." ? "Unidad" : `Precio por ${item.unit}`;

      const card = document.createElement("div");
      card.className = "product-card";
      card.dataset.cat = item.categorySlug;
      card.dataset.discount = item.discount ? "true" : "false";

      card.innerHTML = `
        <div class="thumb">${badgeHtml}${item.emoji}</div>
        <div class="body">
          <span class="cat">${item.category}</span>
          <h3><a href="producto.html?id=${item.id}">${item.name}</a></h3>
          <span class="unit">${unidadTexto}</span>
          <div class="row">
            <span class="price">$${item.price.toLocaleString("es-AR")}</span>
            <button 
              type="button" 
              class="btn" 
              data-add-to-cart 
              data-id="${item.id}" 
              data-name="${item.name}" 
              data-price="${item.price}" 
              data-unit="${item.unit}" 
              data-emoji="${item.emoji}">
              Agregar
            </button>
          </div>
        </div>
      `;

      contenedorGrid.appendChild(card);
    });
  }

  if (inputBuscador) {
    inputBuscador.addEventListener("input", (e) => {
      const termino = e.target.value.toLowerCase().trim();

      const filtrados = catalogo.filter((producto) => {
        const coincideNombre = producto.name.toLowerCase().includes(termino);
        const coincideCategoria = producto.category.toLowerCase().includes(termino);
        const coincideUrlCat = !catSlug || producto.categorySlug === catSlug;
        const coincideUrlOferta = !onlyOffers || producto.discount === true;

        return (coincideNombre || coincideCategoria) && coincideUrlCat && coincideUrlOferta;
      });

      renderizarTarjetas(filtrados);
    });
  }

  cargarCatalogo();
});