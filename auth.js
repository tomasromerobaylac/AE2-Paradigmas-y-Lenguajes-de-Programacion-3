/**
 * auth.js — Estado de sesión compartido por todas las páginas
 * --------------------------------------------------------------
 * Al cargar cualquier página del sitio, consulta el endpoint privado
 * api/perfil.php para saber si hay una sesión activa (cookie de PHP) y
 * actualiza el header ("Mi cuenta" vs. "Hola, <nombre> · Cerrar sesión").
 *
 * Seguridad: todo lo que viene del servidor (nombre, email, rol) se
 * escribe en el DOM con .textContent, nunca con innerHTML, para que un
 * nombre de usuario malicioso no pueda inyectar HTML/JS (XSS).
 */
(function () {
  "use strict";

  /**
   * Consulta el endpoint privado. Si hay sesión activa devuelve los
   * datos del usuario; si no (401) devuelve null, sin tratarlo como un
   * error real: "no logueado" es un estado normal, no una falla.
   */
  async function consultarSesion() {
    try {
      const respuesta = await fetch("api/perfil.php", {
        method: "GET",
        headers: { Accept: "application/json" },
      });
      const datos = await respuesta.json();
      if (respuesta.ok && datos.estado === "exito") {
        return datos.data;
      }
      return null;
    } catch (error) {
      console.error("No se pudo consultar el estado de sesión:", error);
      return null;
    }
  }

  async function cerrarSesion() {
    try {
      await fetch("api/logout.php", { method: "POST" });
    } catch (error) {
      console.error("No se pudo cerrar la sesión en el servidor:", error);
    }
    window.location.href = "index.html";
  }

  /**
   * Dibuja el bloque de cuenta en el header. Usa createElement +
   * textContent en vez de armar un string de HTML, así ningún dato de
   * usuario puede terminar interpretado como markup.
   */
  function renderEstadoHeader(usuario) {
    const contenedor = document.querySelector("#auth-status");
    if (!contenedor) return;

    contenedor.textContent = "";

    if (usuario) {
      const saludo = document.createElement("span");
      saludo.className = "auth-saludo";
      saludo.textContent = "Hola, " + usuario.nombre;

      const separador = document.createTextNode(" · ");

      const btnSalir = document.createElement("button");
      btnSalir.type = "button";
      btnSalir.className = "btn-logout-link";
      btnSalir.textContent = "Cerrar sesión";
      btnSalir.addEventListener("click", cerrarSesion);

      contenedor.appendChild(saludo);
      contenedor.appendChild(separador);
      contenedor.appendChild(btnSalir);
    } else {
      const link = document.createElement("a");
      link.href = "cuenta.html";
      link.textContent = "Mi cuenta";
      contenedor.appendChild(link);
    }
  }

  async function inicializar() {
    const usuario = await consultarSesion();
    renderEstadoHeader(usuario);
    // Avisa a scripts de la propia página (como cuenta.js) que ya se
    // sabe si hay sesión activa, sin que cada uno tenga que repetir el
    // fetch a api/perfil.php.
    document.dispatchEvent(new CustomEvent("mercado:auth", { detail: usuario }));
  }

  // API mínima reutilizable por otros scripts de la página.
  window.MercadoAuth = { consultarSesion, cerrarSesion };

  document.addEventListener("DOMContentLoaded", inicializar);
})();
