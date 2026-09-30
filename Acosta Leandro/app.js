// Variable global para mantener el precio
let precioActual = 0;

// 1. Función Asíncrona para obtener el precio vía HTTP (fetch)
async function consultarPrecio() {
  try {
    const respuesta = await fetch('precios.json');
    if (!respuesta.ok) throw new Error("Error en la red");
    
    const datos = await respuesta.json();
    precioActual = datos.precioActualizado;
    
    // Inyectamos el precio unitario en el DOM al cargar
    document.getElementById('precio-unitario').textContent = precioActual.toLocaleString();
    actualizarSubtotal();
    
  } catch (error) {
    console.error("Error al obtener precios:", error);
  }
}

// 2. Función para actualizar el subtotal mutando el DOM
function actualizarSubtotal() {
  const cantidad = parseInt(document.getElementById('input-cantidad').value);
  const subtotal = cantidad * precioActual;
  
  document.getElementById('subtotal-producto').textContent = subtotal.toLocaleString();
}

// 3. Controladores de Eventos (Event Listeners desacoplados)
function configurarContadores() {
  const btnIncrementar = document.getElementById('btn-incrementar');
  const btnDecrementar = document.getElementById('btn-decrementar');
  const inputCantidad = document.getElementById('input-cantidad');

  btnIncrementar.addEventListener('click', () => {
    let cant = parseInt(inputCantidad.value);
    inputCantidad.value = cant + 1;
    actualizarSubtotal();
  });

  btnDecrementar.addEventListener('click', () => {
    let cant = parseInt(inputCantidad.value);
    if (cant > 1) { // Evita cantidades negativas o cero
      inputCantidad.value = cant - 1;
      actualizarSubtotal();
    }
  });
}

// 4. Inicialización al cargar la ventana
window.addEventListener('load', () => {
  consultarPrecio();
  configurarContadores();
});
