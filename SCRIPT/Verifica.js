window.onload = function() {
    $.ajax({
        url: '../PHP/checkLogin.php',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            if (response.loggedIn === true) {
                document.getElementById('nomeAluno').textContent = response.nome || 'Sem nome';
                if (response.foto) {
    document.getElementById('fotoAluno').src = response.foto; // já é base64 com data URI
} else {
    document.getElementById('fotoAluno').src = '../imagens/sem-foto.png'; // fallback
}
            } else {
                window.location.href = '../HTML/index.html';
            }
        },
        error: function(xhr, status, error) {
            alert('Erro na resposta do servidor!');
            console.error('Erro na requisição AJAX:', error);
            console.log(xhr.responseText); // Veja o erro real aqui
        }
    });
};
