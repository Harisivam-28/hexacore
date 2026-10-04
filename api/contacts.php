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

// 1. Read .env file
function loadEnv($path) {
    if (!file_exists($path)) return [];
    $lines = file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    $env = [];
    foreach ($lines as $line) {
        $line = trim($line);
        if (strpos($line, '#') === 0) continue;
        if (strpos($line, '=') !== false) {
            list($key, $val) = explode('=', $line, 2);
            $env[trim($key)] = trim($val, "\" '");
        }
    }
    return $env;
}

$env = array_merge(
    loadEnv(__DIR__ . '/../.env'),
    loadEnv(__DIR__ . '/.env'),
    loadEnv($_SERVER['DOCUMENT_ROOT'] . '/.env')
);

$companyEmail = !empty($env['COMPANY_EMAIL']) ? $env['COMPANY_EMAIL'] : (!empty($env['MAIL_USER']) ? $env['MAIL_USER'] : 'info@hexacoreprecision.com');
$companyName  = !empty($env['COMPANY_NAME']) ? $env['COMPANY_NAME'] : 'Hexacore Precision Technologies';
$mailUser     = !empty($env['MAIL_USER']) ? $env['MAIL_USER'] : $companyEmail;
$mailPass     = !empty($env['MAIL_PASS']) ? $env['MAIL_PASS'] : '';
$mailHost     = !empty($env['MAIL_HOST']) ? $env['MAIL_HOST'] : 'smtp.hostinger.com';
$mailPort     = !empty($env['MAIL_PORT']) ? intval($env['MAIL_PORT']) : 465;

// 2. Parse input JSON
$input = json_decode(file_get_contents('php://input'), true);
if (!$input) {
    $input = $_POST;
}

$name    = isset($input['name']) ? trim($input['name']) : '';
$email   = isset($input['email']) ? trim($input['email']) : '';
$company = isset($input['company']) ? trim($input['company']) : '';
$phone   = isset($input['phone']) ? trim($input['phone']) : '';
$subject = isset($input['subject']) && !empty($input['subject']) ? trim($input['subject']) : (isset($input['service_required']) ? trim($input['service_required']) : 'General Enquiry');
$message = isset($input['message']) && !empty($input['message']) ? trim($input['message']) : (isset($input['machine_type']) ? trim($input['machine_type']) : '');

if (empty($name) || empty($email)) {
    http_response_code(400);
    echo json_encode(["error" => "Name and email are required."]);
    exit;
}

// 3. Helper to read multiline SMTP responses cleanly
function readSmtpResponse($socket) {
    $response = '';
    while ($line = fgets($socket, 512)) {
        $response .= $line;
        if (strlen($line) >= 4 && substr($line, 3, 1) === ' ') {
            break;
        }
    }
    return $response;
}

// 4. Helper to send authenticated SMTP mail via socket or fallback mail()
function sendMailSmtp($to, $subject, $bodyHtml, $fromEmail, $fromName, $replyTo, $host, $port, $user, $pass) {
    if (!empty($user) && !empty($pass)) {
        $context = stream_context_create([
            'ssl' => [
                'verify_peer' => false,
                'verify_peer_name' => false,
                'allow_self_signed' => true
            ]
        ]);
        
        $socketHost = ($port === 465) ? 'ssl://' . $host : $host;
        $socket = @stream_socket_client($socketHost . ':' . $port, $errno, $errstr, 10, STREAM_CLIENT_CONNECT, $context);
        
        if ($socket) {
            readSmtpResponse($socket);
            
            fputs($socket, "EHLO " . gethostname() . "\r\n");
            readSmtpResponse($socket);
            
            fputs($socket, "AUTH LOGIN\r\n");
            readSmtpResponse($socket);
            
            fputs($socket, base64_encode($user) . "\r\n");
            readSmtpResponse($socket);
            
            fputs($socket, base64_encode($pass) . "\r\n");
            $authRes = readSmtpResponse($socket);
            
            if (strpos($authRes, '235') !== false) {
                fputs($socket, "MAIL FROM: <$user>\r\n");
                readSmtpResponse($socket);
                
                fputs($socket, "RCPT TO: <$to>\r\n");
                readSmtpResponse($socket);
                
                fputs($socket, "DATA\r\n");
                readSmtpResponse($socket);
                
                $headers  = "From: \"$fromName\" <$user>\r\n";
                if (!empty($replyTo)) {
                    $headers .= "Reply-To: <$replyTo>\r\n";
                }
                $headers .= "To: <$to>\r\n";
                $headers .= "Subject: $subject\r\n";
                $headers .= "MIME-Version: 1.0\r\n";
                $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
                
                fputs($socket, $headers . "\r\n" . $bodyHtml . "\r\n.\r\n");
                $dataRes = readSmtpResponse($socket);
                fputs($socket, "QUIT\r\n");
                fclose($socket);
                
                if (strpos($dataRes, '250') !== false) {
                    return true;
                }
            } else {
                fclose($socket);
            }
        }
    }
    
    // Fallback to PHP native mail()
    $headers  = "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
    $headers .= "From: \"$fromName\" <$fromEmail>\r\n";
    if (!empty($replyTo)) {
        $headers .= "Reply-To: <$replyTo>\r\n";
    }
    return @mail($to, $subject, $bodyHtml, $headers);
}

// 5. Construct HTML Shell
function buildEmailHtml($title, $body) {
    return '<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>' . htmlspecialchars($title) . '</title>
  <style>
    body { margin: 0; padding: 0; background: #f0f2f5; font-family: Arial, sans-serif; }
    .wrapper { max-width: 620px; margin: 30px auto; background: #ffffff; }
    .header  { background: #0B1F3A; padding: 28px 36px; border-bottom: 3px solid #F47B20; }
    .brand-name { color: #ffffff; font-size: 18px; font-weight: 800; }
    .body { padding: 36px; color: #1e2d42; }
    .title { font-size: 20px; font-weight: 700; color: #0B1F3A; border-bottom: 2px solid #F47B20; padding-bottom: 10px; margin-bottom: 20px; }
    .field { margin-bottom: 14px; }
    .field .label { font-size: 10px; font-weight: 700; text-transform: uppercase; color: #8296b0; }
    .field .value { font-size: 14px; color: #1e2d42; background: #f6f8fb; padding: 8px 12px; border-left: 3px solid #F47B20; margin-top: 4px; }
    .message-box { background: #f6f8fb; border-left: 3px solid #F47B20; padding: 14px; margin-top: 6px; font-size: 14px; white-space: pre-wrap; }
    .footer { background: #071527; padding: 18px; text-align: center; color: #4a5e7a; font-size: 11px; }
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="header"><div class="brand-name">HEXACORE PRECISION TECHNOLOGIES</div></div>
    <div class="body">' . $body . '</div>
    <div class="footer"><p>Hexacore Precision Technologies</p></div>
  </div>
</body>
</html>';
}

// 6. Send notification email to Company
$adminBody = '
  <div class="title">New Contact Submission</div>
  <div class="field"><div class="label">Full Name</div><div class="value">' . htmlspecialchars($name) . '</div></div>
  <div class="field"><div class="label">Company</div><div class="value">' . htmlspecialchars($company ? $company : '—') . '</div></div>
  <div class="field"><div class="label">Email Address</div><div class="value">' . htmlspecialchars($email) . '</div></div>
  <div class="field"><div class="label">Phone</div><div class="value">' . htmlspecialchars($phone ? $phone : '—') . '</div></div>
  <div class="field"><div class="label">Subject</div><div class="value">' . htmlspecialchars($subject) . '</div></div>
  <div class="field"><div class="label">Message / Requirement</div><div class="message-box">' . htmlspecialchars($message) . '</div></div>
';
$adminHtml = buildEmailHtml('New Contact Submission', $adminBody);

sendMailSmtp($companyEmail, "[Contact] $subject — $name", $adminHtml, $mailUser, $companyName, $email, $mailHost, $mailPort, $mailUser, $mailPass);

if ($companyEmail !== 'ceo@hexacoreprecision.com') {
    sendMailSmtp('ceo@hexacoreprecision.com', "[Contact] $subject — $name", $adminHtml, $mailUser, $companyName, $email, $mailHost, $mailPort, $mailUser, $mailPass);
}

// 7. Send auto-reply to user
$userBody = '
  <div class="title">Thank You, ' . htmlspecialchars(explode(' ', $name)[0]) . '</div>
  <p>We have received your enquiry and our engineering team will review it shortly. You can expect a response within one business day.</p>
  <div class="field"><div class="label">Your Subject</div><div class="value">' . htmlspecialchars($subject) . '</div></div>
  <div class="field"><div class="label">Your Message</div><div class="message-box">' . htmlspecialchars($message) . '</div></div>
';
$userHtml = buildEmailHtml('We received your message', $userBody);

@sendMailSmtp($email, "We received your message — Hexacore Precision Technologies", $userHtml, $mailUser, $companyName, $companyEmail, $mailHost, $mailPort, $mailUser, $mailPass);

// 8. Return 201 Created Response
http_response_code(201);
echo json_encode([
    "success" => true,
    "message" => "Your message has been received. We will respond within one business day."
]);
