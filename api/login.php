<?php
/**
 * api/login.php — Autenticación de cliente
 * -------------------------------------------
 * Valida credenciales con password_verify() contra el hash BCRYPT
 * guardado en MySQL, y si son correctas abre una sesión de servidor.
 */
header('Content-Type: application/json; charset=utf-8');
require_once '../config/conexion.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(["estado" => "error", "mensaje" => "Método no permitido."]);
    exit;
}

$input    = json_decode(file_get_contents('php://input'), true);
$email    = trim($input['email'] ?? '');
$password = $input['password'] ?? '';

if (empty($email) || empty($password)) {
    http_response_code(400);
    echo json_encode(["estado" => "error", "mensaje" => "Ingresá tu correo y tu contraseña."]);
    exit;
}

try {
    $stmt = $pdo->prepare('SELECT id, nombre, email, password, rol FROM usuarios WHERE email = :email');
    $stmt->execute(['email' => $email]);
    $usuario = $stmt->fetch();

    if ($usuario && password_verify($password, $usuario['password'])) {
        // Iniciamos la sesión del lado del servidor.
        session_start();
        // Regenera el ID de sesión al autenticar, para prevenir
        // ataques de fijación de sesión (session fixation).
        session_regenerate_id(true);

        $_SESSION['usuario_id']     = $usuario['id'];
        $_SESSION['usuario_nombre'] = $usuario['nombre'];
        $_SESSION['usuario_email']  = $usuario['email'];
        $_SESSION['usuario_rol']    = $usuario['rol'];

        http_response_code(200);
        echo json_encode([
            "estado"  => "exito",
            "mensaje" => "Sesión iniciada correctamente.",
            "usuario" => [
                "nombre" => $usuario['nombre'],
                "email"  => $usuario['email'],
                "rol"    => $usuario['rol'],
            ],
        ]);
    } else {
        http_response_code(401); // Unauthorized
        echo json_encode(["estado" => "error", "mensaje" => "Correo o contraseña incorrectos."]);
    }
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(["estado" => "error", "mensaje" => "Error interno del servidor."]);
}
