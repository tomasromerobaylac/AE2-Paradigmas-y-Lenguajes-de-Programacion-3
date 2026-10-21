<?php
/**
 * api/perfil.php — Endpoint privado protegido
 * ------------------------------------------------
 * Este es el servicio elegido para proteger contra accesos no
 * autorizados: devuelve los datos de la cuenta del cliente logueado.
 * El frontend (auth.js) lo consulta en cada página para saber si hay
 * una sesión activa y decidir qué mostrar en el header del sitio.
 */
session_start();
header('Content-Type: application/json; charset=utf-8');

// Guardián de sesión: sin sesión activa, no hay datos — 401 Unauthorized.
if (!isset($_SESSION['usuario_id'])) {
    http_response_code(401);
    echo json_encode(["estado" => "error", "mensaje" => "Acceso no autorizado. Iniciá sesión."]);
    exit;
}

http_response_code(200);
echo json_encode([
    "estado" => "exito",
    "data"   => [
        "id"     => $_SESSION['usuario_id'],
        "nombre" => $_SESSION['usuario_nombre'],
        "email"  => $_SESSION['usuario_email'],
        "rol"    => $_SESSION['usuario_rol'],
    ],
], JSON_UNESCAPED_UNICODE);
