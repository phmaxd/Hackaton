<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

session_start();
header('Content-Type: application/json');

include 'conecta.php';

if (!empty($_SESSION['rm'])) {
    $query = "SELECT Nome, Imagem FROM alunos WHERE rm = ?";
    $stmt = $pdo->prepare($query);
    $stmt->execute([$_SESSION['rm']]);
    $aluno = $stmt->fetch(PDO::FETCH_ASSOC);

    echo json_encode([
        'loggedIn' => true,
        'nome' => $aluno ? $aluno['Nome'] : '',
        'foto' => $aluno ? $aluno['Imagem'] : ''
    ]);
} else {
    echo json_encode(['loggedIn' => false]);
}
exit;