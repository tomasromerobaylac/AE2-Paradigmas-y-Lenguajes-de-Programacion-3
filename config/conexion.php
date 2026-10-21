<?php
/**
 * config/conexion.php — Conexión PDO a MySQL (Mercado Fresco)
 * -------------------------------------------------------------
 * Cambiar $user/$pass según la configuración local de MySQL
 * (en XAMPP por defecto es user="root", pass="").
 */
$host    = 'localhost';
$db      = 'mercado_fresco';
$user    = 'root';
$pass    = '';
$charset = 'utf8mb4';

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

try {
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (\PDOException $e) {
    http_response_code(500);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(["estado" => "error", "mensaje" => "Error de conexión con la base de datos."]);
    exit;
}
