<?php
// Diretórios para uploads e resultados
$uploadDir = __DIR__ . '/uploads/';
$resultDir = __DIR__ . '/resultados/';

// Criar diretórios se não existirem
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0755, true);
}
if (!is_dir($resultDir)) {
    mkdir($resultDir, 0755, true);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_FILES['imagem']) || $_FILES['imagem']['error'] !== UPLOAD_ERR_OK) {
        die('Erro no upload da imagem.');
    }

    $fileTmpPath = $_FILES['imagem']['tmp_name'];
    $fileName = basename($_FILES['imagem']['name']);
    $fileExt = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));

    // Validar extensão (exemplo: jpg, jpeg, png, gif)
    $allowedExts = ['jpg', 'jpeg', 'png', 'gif'];
    if (!in_array($fileExt, $allowedExts)) {
        die('Tipo de arquivo não permitido. Envie uma imagem JPG, PNG ou GIF.');
    }

    // Gerar nome único para evitar sobrescrever
    $newFileName = uniqid('img_', true) . '.' . $fileExt;
    $destPath = $uploadDir . $newFileName;

    if (!move_uploaded_file($fileTmpPath, $destPath)) {
        die('Erro ao salvar o arquivo no servidor.');
    }

    // Caminho do arquivo JSON de saída
    $jsonFileName = uniqid('result_', true) . '.json';
    $jsonFilePath = $resultDir . $jsonFileName;

    // Comando para chamar o script Python
    // Ajuste o caminho do python3 e do script gpey.py conforme seu ambiente
    $pythonPath = 'python3'; // ou caminho absoluto, ex: /usr/bin/python3
    $scriptPath = __DIR__ . '/gpey.py';

    // Escapar argumentos para segurança
    $cmd = escapeshellcmd("$pythonPath $scriptPath \"$destPath\" \"$jsonFilePath\"");

    // Executar o comando e capturar saída e código de retorno
    exec($cmd . ' 2>&1', $output, $return_var);

    if ($return_var !== 0) {
        echo "Erro ao executar o script Python:<br>";
        echo nl2br(htmlspecialchars(implode("\n", $output)));
        exit;
    }

    // Ler o JSON gerado
    if (!file_exists($jsonFilePath)) {
        die('Arquivo JSON de resultado não encontrado.');
    }

    $jsonContent = file_get_contents($jsonFilePath);
    $resultData = json_decode($jsonContent, true);

    if ($resultData === null) {
        die('Erro ao decodificar o JSON de resultado.');
    }

    // Mostrar resultado (exemplo simples)
    echo "<h2>Resultado do processamento</h2>";
    echo "<pre>" . htmlspecialchars(json_encode($resultData, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE)) . "</pre>";

    // Opcional: mostrar a imagem enviada
    $imgUrl = 'uploads/' . $newFileName;
    echo "<h3>Imagem enviada:</h3>";
    echo "<img src=\"$imgUrl\" alt=\"Imagem enviada\" style=\"max-width:400px; height:auto;\" />";
} else {
    echo "Método inválido.";
}
?>
