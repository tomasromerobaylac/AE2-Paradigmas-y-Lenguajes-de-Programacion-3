<?php
/**
 * api/registro.php — Alta de cuenta de cliente
 * -----------------------------------------------
 * Recibe JSON, hashea la contraseña con BCRYPT y la guarda en MySQL
 * mediante una consulta preparada (PDO), para evitar inyección SQL.
 */
header('Content-Type: application/json; charset=utf-8');
require_once '../config/conexion.php';

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405); // Method Not Allowed
    echo json_encode(["estado" => "error", "mensaje" => "Método no permitido."]);
    exit;
}

// Lectura del JSON entrante en el cuerpo de la petición HTTP
$input = json_decode(file_get_contents('php://input'), true);

// htmlspecialchars: evita que el nombre quede guardado con HTML/JS
// embebido (protección XSS adicional a la que hace el frontend con
// textContent al mostrarlo).
$nombre   = htmlspecialchars(trim($input['nombre'] ?? ''), ENT_QUOTES, 'UTF-8');
$email    = trim($input['email'] ?? '');
$password = $input['password'] ?? '';

if (empty($nombre) || empty($email) || empty($password)) {
    http_response_code(400); // Bad Request
    echo json_encode(["estado" => "error", "mensaje" => "Todos los campos son obligatorios."]);
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(["estado" => "error", "mensaje" => "El correo electrónico no es válido."]);
    exit;
}

if (strlen($password) < 6) {
    http_response_code(400);
    echo json_encode(["estado" => "error", "mensaje" => "La contraseña debe tener al menos 6 caracteres."]);
    exit;
}

// Cifrado BCRYPT de la contraseña — nunca se guarda en texto plano.
$passwordHash = password_hash($password, PASSWORD_BCRYPT);

try {
    $sql = "INSERT INTO usuarios (nombre, email, password) VALUES (:nombre, :email, :pass)";
    $stmt = $pdo->prepare($sql);
    $stmt->execute([
        'nombre' => $nombre,
        'email'  => $email,
        'pass'   => $passwordHash,
    ]);

    http_response_code(201); // Created
    echo json_encode(["estado" => "exito", "mensaje" => "Cuenta creada correctamente."]);

} catch (PDOException $e) {
    if ($e->getCode() == 23000) {
        http_response_code(409); // Conflict (email duplicado)
        echo json_encode(["estado" => "error", "mensaje" => "Ya existe una cuenta con ese correo electrónico."]);
    } else {
        http_response_code(500);
        echo json_encode(["estado" => "error", "mensaje" => "Error interno al registrar la cuenta."]);
    }
}
