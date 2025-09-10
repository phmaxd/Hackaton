<?php
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
