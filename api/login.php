<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type, Authorization");
header("Access-Control-Allow-Methods: POST, OPTIONS");
header("Content-Type: application/json; charset=UTF-8");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(["error" => "Method not allowed"]);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
if (!$input) {
    $input = $_POST;
}

$username = isset($input['username']) ? trim($input['username']) : '';
$password = isset($input['password']) ? trim($input['password']) : '';

if (empty($username) || empty($password)) {
    http_response_code(400);
    echo json_encode(["error" => "Username and password required"]);
    exit;
}

// Valid Admin Credentials
$validUsernames = ['admin', 'hexacoreprecision'];
$validPasswords = ['hexacore2026', 'Hexacore@2026'];

if (in_array($username, $validUsernames, true) && in_array($password, $validPasswords, true)) {
    // Generate valid JWT token structure
    $header  = rtrim(strtr(base64_encode(json_encode(['alg' => 'HS256', 'typ' => 'JWT'])), '+/', '-_'), '=');
    $payload = rtrim(strtr(base64_encode(json_encode([
        'id' => 1,
        'username' => $username,
        'exp' => time() + (8 * 3600)
    ])), '+/', '-_'), '=');
    $signature = rtrim(strtr(base64_encode(hash_hmac('sha256', "$header.$payload", 'hexacore_secret_2026', true)), '+/', '-_'), '=');
    
    $token = "$header.$payload.$signature";

    echo json_encode([
        "token" => $token,
        "username" => $username
    ]);
    exit;
}

http_response_code(401);
echo json_encode(["error" => "Invalid credentials"]);
