<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

session_start();
header('Content-Type: application/json');

require_once 'conecta.php';

$response = ['loggedIn' => false];

try {
    if (!empty($_SESSION['CPF'])) {
        $query = "SELECT Nome, Imagem FROM funcionarios WHERE CPF = ?";
        $stmt = $pdo->prepare($query);
        $stmt->execute([$_SESSION['CPF']]);
        $professor = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($professor) {
            $Imagem = '';
            if ($professor['Imagem']) {
                $Imagem = 'data:image/jpeg;base64,' . base64_encode($professor['Imagem']);
            }
            $response = [
                'loggedIn' => true,
                'nome' => $professor['Nome'],
                'foto' => $Imagem
            ];
        }
    }
} catch (Exception $e) {
    $response['error'] = $e->getMessage();
}

echo json_encode($response);
exit;
