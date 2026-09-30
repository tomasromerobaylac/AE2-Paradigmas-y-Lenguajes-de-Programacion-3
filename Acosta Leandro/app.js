const formatoPrecio = new Intl.NumberFormat('es-AR');

async function consultarPrecio(productoId) {
  const respuesta = await fetch('precios.json');
  if (!respuesta.ok) throw new Error('No se pudo consultar la lista de precios');

  const productos = await respuesta.json();
  const producto = productos.find((item) => item.productoId === productoId);
  if (!producto || !Number.isFinite(producto.precioActualizado)) {
    throw new Error(`No hay un precio válido para ${productoId}`);
  }

  return producto.precioActualizado;
}

async function cargarFichaProducto() {
  const respuesta = await fetch('productos.json');
  if (!respuesta.ok) throw new Error('No se pudo cargar el catálogo');

  const productos = await respuesta.json();
  const productoId = new URLSearchParams(window.location.search).get('id') || 'tomate-perita';
  const producto = productos.find((item) => item.id === productoId);
  if (!producto) throw new Error(`No se encontró el producto ${productoId}`);

  document.title = `${producto.nombre} — Mercado Fresco`;
  document.querySelectorAll('[data-product-name]').forEach((elemento) => {
    elemento.textContent = producto.nombre;
  });
  document.querySelectorAll('[data-product-category]').forEach((elemento) => {
    elemento.textContent = producto.categoria;
  });
  document.querySelector('[data-product-description]').textContent = producto.descripcion;
  document.querySelectorAll('[data-product-emoji]').forEach((elemento) => {
    elemento.textContent = producto.emoji;
  });
  document.querySelectorAll('[data-product-unit]').forEach((elemento) => {
    elemento.textContent = producto.unidad;
  });

  const precioAnterior = document.querySelector('[data-product-old-price]');
  const badge = document.querySelector('[data-product-badge]');
  if (producto.precioAnterior) {
    precioAnterior.textContent = formatoPrecio.format(producto.precioAnterior);
    precioAnterior.style.display = '';
  } else {
    precioAnterior.style.display = 'none';
  }
  if (producto.badge) {
    badge.textContent = producto.badge;
    badge.style.display = '';
  } else {
    badge.style.display = 'none';
  }

  const botonAgregar = document.querySelector('[data-add-to-cart]');
  botonAgregar.dataset.id = producto.id;
  botonAgregar.dataset.name = producto.nombre;
  botonAgregar.dataset.price = producto.precio;
  botonAgregar.dataset.unit = producto.unidad;
  botonAgregar.dataset.emoji = producto.emoji;
  return botonAgregar;
}

function configurarContador() {
  const inputCantidad = document.querySelector('#input-cantidad');
  const subtotal = document.querySelector('#subtotal-producto');
  const precio = document.querySelector('#precio-unitario');
  const botonAgregar = document.querySelector('[data-add-to-cart]');

  if (!inputCantidad || !subtotal || !precio || !botonAgregar) return;

  let precioUnitario = Number(botonAgregar.dataset.price);

  function actualizarSubtotal() {
    const cantidad = Math.max(1, Number.parseInt(inputCantidad.value, 10) || 1);
    inputCantidad.value = cantidad;
    subtotal.textContent = formatoPrecio.format(cantidad * precioUnitario);
  }

  inputCantidad.addEventListener('input', actualizarSubtotal);

  cargarFichaProducto()
    .then((boton) => consultarPrecio(boton.dataset.id).then((nuevoPrecio) => ({ boton, nuevoPrecio })))
    .then(({ boton, nuevoPrecio }) => {
      precioUnitario = nuevoPrecio;
      precio.textContent = formatoPrecio.format(precioUnitario);
      boton.dataset.price = precioUnitario;
      actualizarSubtotal();
    })
    .catch((error) => {
      console.error('Error al cargar el precio actualizado:', error);
      actualizarSubtotal();
    });

  actualizarSubtotal();
}

document.addEventListener('DOMContentLoaded', configurarContador);
