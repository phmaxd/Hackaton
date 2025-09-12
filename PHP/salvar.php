<?php

$conn = new mysqli('localhost', 'root', '', 'hackaton');

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$input = json_decode(file_get_contents('php://input'), true);

$nota = (int)$input['nota'];
$acertos = (int)$input['acertos'];
$erros = (int)$input['erros'];

$sql = "INSERT INTO resultados (nota, acertos, erros) VALUES ($nota, $acertos, $erros)";

if ($conn->query($sql) === TRUE) {
    echo json_encode(['message' => 'Data saved successfully']);
} else {
    echo json_encode(['error' => 'Error: ' . $conn->error]);
}