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

    if ($aluno) {
        $foto = '';
        if ($aluno['Imagem']) {
            $base64 = base64_encode($aluno['Imagem']);
            // Supondo que a imagem é jpeg, ajuste se for png ou outro formato
            $foto = 'data:image/jpeg;base64,' . $base64;
        }

        echo json_encode([
            'loggedIn' => true,
            'nome' => $aluno['Nome'],
            'foto' => $foto
        ]);
    } else {
        echo json_encode(['loggedIn' => false]);
    }
} else {
    echo json_encode(['loggedIn' => false]);
}
exit;
