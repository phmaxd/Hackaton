<?php
<<<<<<< HEAD
header('Content-Type: application/json; charset=utf-8');
include 'conecta.php';
session_start();
try {
    $CPF = trim($_POST['CPF']);
    $Senha = trim($_POST['Senha']);
    $stmt = $conn->prepare("SELECT * FROM funcionarios WHERE CPF = :CPF AND Senha = :Senha");
    $stmt->bindParam(':CPF', $CPF);
    $stmt->bindParam(':Senha', $Senha);
    $stmt->execute();
    if ($stmt->rowCount() > 0) {
        $_SESSION['CPF'] = $CPF;
        echo json_encode(["status" => "success"]);
    } else {
        echo json_encode(["status" => "error"]);
    }
} catch (PDOException $e) {
    echo json_encode(["status" => "error", "message" => $e->getMessage()]);
}
=======
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

    try {
        $query = "SELECT * FROM funcionarios WHERE CPF = ? AND senha = ?";
        $stmt = $pdo->prepare($query);
        $stmt->execute([$CPF, $senha]);
        $professor = $stmt->fetch(PDO::FETCH_ASSOC);
        if ($professor) {
            $_SESSION['CPF'] = $CPF;
            echo json_encode([
                'status' => 'success',
                'loggedIn' => true,
                'CPF' => $CPF,
                'Nome' => $professor['Nome'],
                'Foto' => $professor['Imagem']
            ]);
        } else {
            echo json_encode(['status' => 'error', 'message' => 'Credenciais inválidas.']);
        }
    } catch (Exception $e) {
        echo json_encode(['status' => 'error', 'message' => 'Erro no servidor.']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'Método inválido.']);
}
?>
>>>>>>> funcionou
