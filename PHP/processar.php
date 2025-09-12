<?php

header('Content-Type: application/json; charset=utf-8');

$rm = $_POST['rm'] ?? '';

if(!$rm || !isset($_FILES['image'])) {
    echo json_encode(['status' => 'error', 'message' => 'Parâmetros inválidos.']);
    exit;
}

$uploadDir = 'uploads/';
if(!file_exists($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

$filename = basename($_FILES['image']['name']);
$filepath = $uploadDir . $filename;
move_uploaded_file($_FILES['image']['tmp_name'], $filepath);

$outputJson = $uploadDir . 'data_' . time() . '.json';
exec("python3 ../PYTHON/gpei.py" . escapeshellarg($filepath) . " " . escapeshellarg($outputJson));

if(file_exists($outputJson))
{
    $data = json_decode(file_get_contents($outputJson), true);

    if($data && json_last_error() === JSON_ERROR_NONE){
        $pdo = new PDO('mysql:host=localhost;dbname=hackaton', 'root', '');
        $stmt = $pdo->prepare("INSERT INTO alunos (id, nome, rm, senha, imagem, acertos, erros, nota) VALUES (?,?,?,?,?,?,?,?)");
        $stmt->execute([
            $rm,
            $data['nome'] ?? null,
            $data['rm'] ?? null,
            $data['senha'] ?? null,
            $data['imagem'] ?? null,
            $data['acertos'] ?? null,
            $data['erros'] ?? null,
            $data['nota']?? null
        ]);

        echo json_encode(['status' => 'ok', 'msg' => 'Resultado salvo com sucesso!']);
    }else{
        echo json_encode(['error' => 'error ao ler JSON']);

    }
}    else{
        echo json_encode(['error' => 'JSON do python não encontrado']);
    }
