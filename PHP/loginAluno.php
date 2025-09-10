<?php
session_start(); // Inicia a sessão
header('Content-Type: application/json');
include 'conecta.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $rm = isset($_POST['rm']) ? trim($_POST['rm']) : '';
    $senha = isset($_POST['senha']) ? trim($_POST['senha']) : '';

    if (empty($rm) || empty($senha)) {
        echo json_encode(['status' => 'error', 'message' => 'RM e senha obrigatórios.']);
        exit;
    }

    $query = "SELECT * FROM alunos WHERE rm = ? AND senha = ?";
    $stmt = $pdo->prepare($query);
    $stmt->execute([$rm, $senha]);

    if ($stmt->rowCount() > 0) {
        $_SESSION['rm'] = $rm; // Salva RM na sessão
        echo json_encode(['status' => 'success', 'rm' => $rm]);
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Credenciais inválidas.']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Método inválido.']);
}
?>
