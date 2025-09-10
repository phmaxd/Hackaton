window.onload = function() {
    $.ajax({
        url: '../PHP/checkLoginProf.php',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            if (response.loggedIn === true) {
                document.getElementById('nomeProf').textContent = response.nome || 'Sem nome';
                if (response.foto) {
                    document.getElementById('fotoProf').src = '../' + response.foto;
                } else {
                    document.getElementById('fotoProf').src = '../imagens/sem-foto.png';
                }
            } else {
                window.location.href = '../HTML/index.html';
            }
        },
        error: function(xhr, status, error) {
            alert('Erro na resposta do servidor!');
            console.error('Erro na requisição AJAX:', error);
        }
    });
};
