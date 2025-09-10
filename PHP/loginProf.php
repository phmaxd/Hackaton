<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

session_start();
header('Content-Type: application/json');
include 'conecta.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $CPF = isset($_POST['CPF']) ? trim($_POST['CPF']) : '';
    $senha = isset($_POST['senha']) ? trim($_POST['senha']) : '';

    if (empty($CPF) || empty($senha)) {
        echo json_encode(['status' => 'error', 'message' => 'CPF e senha obrigatórios.']);
        exit;
    }

    $query = "SELECT * FROM funcionarios WHERE CPF = ?";
    $stmt = $pdo->prepare($query);
    $stmt->execute([$CPF]);
    $professor = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($stmt->rowCount() > 0) {
        $_SESSION['CPF'] = $CPF;
        echo json_encode(['status' => 'success', 'CPF' => $CPF]);
    } else {
        echo json_encode(['status' => 'error', 'message' => 'Credenciais inválidas.']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Método inválido.']);
}
?>
