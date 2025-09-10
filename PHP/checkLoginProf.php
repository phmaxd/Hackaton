<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

session_start();
header('Content-Type: application/json');

include 'conecta.php';

if (!empty($_SESSION['CPF'])) {
    $query = "SELECT Nome, Imagem FROM funcionarios WHERE CPF = ?";
    $stmt = $pdo->prepare($query);
    $stmt->execute([$_SESSION['CPF']]);
    $professor = $stmt->fetch(PDO::FETCH_ASSOC);

    echo json_encode([
        'loggedIn' => true,
        'nome' => $professor ? $professor['Nome'] : '',
        'foto' => $professor ? $professor['Imagem'] : ''
    ]);
} else {
    echo json_encode(['loggedIn' => false]);
}
