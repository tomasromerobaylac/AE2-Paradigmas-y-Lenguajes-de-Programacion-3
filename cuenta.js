/**
 * cuenta.js — Lógica de la página "Mi cuenta" (cuenta.html)
 * -------------------------------------------------------------
 * Maneja las pestañas login/registro, el envío de ambos formularios
 * contra la API en PHP, el botón de cerrar sesión y el panel privado
 * que se muestra cuando ya hay una sesión activa (avisada por auth.js
 * a través del evento "mercado:auth").
 *
 * Todo dato que llega del servidor se escribe con .textContent, nunca
 * con innerHTML, para evitar XSS.
 */
(function () {
  "use strict";

  function mostrarTab(tab) {
    const vistaLogin = document.querySelector("#vista-login");
    const vistaRegistro = document.querySelector("#vista-registro");
    const vistaPanel = document.querySelector("#vista-panel");
    const tabs = document.querySelector("#cuenta-tabs");
    const btnLogin = document.querySelector("#tab-login");
    const btnRegistro = document.querySelector("#tab-registro");

    tabs.style.display = "";
    vistaPanel.style.display = "none";
    vistaLogin.style.display = tab === "login" ? "" : "none";
    vistaRegistro.style.display = tab === "registro" ? "" : "none";

    btnLogin.classList.toggle("btn-mustard", tab === "login");
    btnLogin.classList.toggle("btn-outline", tab !== "login");
    btnRegistro.classList.toggle("btn-mustard", tab === "registro");
    btnRegistro.classList.toggle("btn-outline", tab !== "registro");
  }

  function mostrarPanel(usuario) {
    document.querySelector("#cuenta-tabs").style.display = "none";
    document.querySelector("#vista-login").style.display = "none";
    document.querySelector("#vista-registro").style.display = "none";

    const panel = document.querySelector("#vista-panel");
    panel.style.display = "";

    // .textContent: el nombre/email vienen del servidor, se muestran
    // como texto plano, nunca como HTML.
    document.querySelector("#panel-nombre").textContent = usuario.nombre;
    document.querySelector("#panel-email").textContent = usuario.email;
    document.querySelector("#panel-rol").textContent =
      usuario.rol === "empleado" ? "Empleado" : "Cliente";
  }

  function mostrarMensaje(el, texto, tipo) {
    el.textContent = texto;
    el.style.display = "";
    el.classList.remove("mensaje-error", "mensaje-exito");
    if (tipo === "error") el.classList.add("mensaje-error");
    if (tipo === "exito") el.classList.add("mensaje-exito");
  }

  async function manejarLogin(evento) {
    evento.preventDefault();
    const msg = document.querySelector("#msg-login");
    mostrarMensaje(msg, "Verificando credenciales…", null);

    const payload = {
      email: document.querySelector("#login-email").value.trim(),
      password: document.querySelector("#login-pass").value,
    };

    try {
      const respuesta = await fetch("api/login.php", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const datos = await respuesta.json();

      if (respuesta.ok && datos.estado === "exito") {
        msg.style.display = "none";
        mostrarPanel(datos.usuario);
        // Avisa a auth.js (y a cualquier otro listener) que ahora hay
        // sesión activa, así el header se actualiza sin recargar.
        document.dispatchEvent(new CustomEvent("mercado:auth", { detail: datos.usuario }));
      } else {
        mostrarMensaje(msg, datos.mensaje || "Correo o contraseña incorrectos.", "error");
      }
    } catch (error) {
      mostrarMensaje(msg, "No se pudo conectar con el servidor.", "error");
    }
  }

  async function manejarRegistro(evento) {
    evento.preventDefault();
    const msg = document.querySelector("#msg-registro");
    mostrarMensaje(msg, "Creando la cuenta…", null);

    const payload = {
      nombre: document.querySelector("#reg-nombre").value.trim(),
      email: document.querySelector("#reg-email").value.trim(),
      password: document.querySelector("#reg-pass").value,
    };

    try {
      const respuesta = await fetch("api/registro.php", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const datos = await respuesta.json();

      if (respuesta.ok && datos.estado === "exito") {
        mostrarMensaje(msg, "¡Cuenta creada! Ya podés iniciar sesión.", "exito");
        document.querySelector("#form-registro").reset();
        setTimeout(() => mostrarTab("login"), 1200);
      } else {
        mostrarMensaje(msg, datos.mensaje || "No se pudo crear la cuenta.", "error");
      }
    } catch (error) {
      mostrarMensaje(msg, "No se pudo conectar con el servidor.", "error");
    }
  }

  async function manejarLogout() {
    try {
      await fetch("api/logout.php", { method: "POST" });
    } catch (error) {
      console.error("No se pudo cerrar la sesión en el servidor:", error);
    }
    window.location.reload();
  }

  function inicializar() {
    document.querySelector("#tab-login").addEventListener("click", () => mostrarTab("login"));
    document.querySelector("#tab-registro").addEventListener("click", () => mostrarTab("registro"));

    document.querySelector("#form-login").addEventListener("submit", manejarLogin);
    document.querySelector("#form-registro").addEventListener("submit", manejarRegistro);
    document.querySelector("#btn-logout").addEventListener("click", manejarLogout);

    // auth.js dispara este evento apenas sabe si hay sesión activa.
    // Si la hay, mostramos directamente el panel en vez de los tabs.
    document.addEventListener("mercado:auth", (evento) => {
      if (evento.detail) mostrarPanel(evento.detail);
    });
  }

  document.addEventListener("DOMContentLoaded", inicializar);
})();
