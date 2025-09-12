<?php
// Definir as configurações do banco de dados
$servername = "localhost";
$username = "root";   // Usuário do banco de dados
$password = "";       // Senha do banco de dados
$dbname = "hackaton"; // Nome correto do banco de dados

// Criar a conexão com o banco de dados
$conn = new mysqli($servername, $username, $password, $dbname);

// Verificar se houve erro na conexão
if ($conn->connect_error) {
    die("Conexão falhou: " . $conn->connect_error); // Exibe erro caso a conexão falhe
}

// Verificar se o formulário foi enviado
if (isset($_POST['submit'])) {
    // Verificar se o arquivo foi enviado
    if (isset($_FILES['gabarito']) && $_FILES['gabarito']['error'] == 0) {
        
        // Obter o RM do formulário
        $rm = $_POST['rm'];

        // Obter as informações do arquivo
        $file_name = $_FILES['gabarito']['name'];
        $file_tmp = $_FILES['gabarito']['tmp_name'];
        $file_size = $_FILES['gabarito']['size'];
        $file_error = $_FILES['gabarito']['error'];
        
        // Definir a pasta onde as imagens serão salvas
        $upload_dir = "uploads/";

        // Verificar se o arquivo é uma imagem válida
        $file_ext = strtolower(pathinfo($file_name, PATHINFO_EXTENSION));
        $allowed_extensions = array('jpg', 'jpeg', 'png', 'gif');
        
        if (in_array($file_ext, $allowed_extensions)) {
            // Gerar um nome único para o arquivo
            $new_file_name = uniqid() . "." . $file_ext;

            // Mover o arquivo para o diretório de upload
            if (move_uploaded_file($file_tmp, $upload_dir . $new_file_name)) {
                // Salvar informações no banco de dados
                $sql = "INSERT INTO uploads (rm, image_name) VALUES ('$rm', '$new_file_name')";
                
                if ($conn->query($sql) === TRUE) {
                    echo "Arquivo enviado com sucesso!";
                } else {
                    echo "Erro ao salvar no banco de dados: " . $conn->error;
                }
            } else {
                echo "Erro ao mover o arquivo para o servidor.";
            }
        } else {
            echo "Tipo de arquivo não permitido. Apenas imagens são permitidas.";
        }
    } else {
        echo "Erro no upload do arquivo.";
    }
}

// Fechar a conexão com o banco de dados
$conn->close();
?>
