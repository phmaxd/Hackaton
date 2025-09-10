<?php
header('Content-Type: application/json; charset=utf-8');
include 'conecta.php';
session_start();
try {
    $rm = trim($_POST['rm']);
    $senha = trim($_POST['senha']);
    $stmt = $conn->prepare("SELECT * FROM alunos WHERE rm = :rm AND senha = :senha");
    $stmt->bindParam(':rm', $rm);
    $stmt->bindParam(':senha', $senha);
    $stmt->execute();
    if ($stmt->rowCount() > 0) {
        $_SESSION['rm'] = $rm;
        echo json_encode(["status" => "success"]); 
    } else {
        echo json_encode(["status" => "error"]);
    }
} catch (PDOException $e) {
    echo json_encode(["status" => "error", "message" => $e->getMessage()]);
}
