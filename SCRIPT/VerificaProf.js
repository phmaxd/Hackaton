window.onload = function () {
    $.ajax({
        url: '../PHP/checkLoginProf.php',
        type: 'GET',
        dataType: 'json',
        success: function (response) {
            if (response.loggedIn === true) {
                document.getElementById('nomeProf').textContent = response.nome || 'Sem nome';
                if (response.foto) {
                    document.getElementById('fotoProf').src = response.foto; // base64
                } else {
                    document.getElementById('fotoProf').src = '../Uploads/sem-foto.png'; // caminho de fallback
                }
            } else {
                window.location.href = '../HTML/index.html'; // redireciona se não estiver logado
            }
        },
        error: function (xhr, status, error) {
            alert('Erro na resposta do servidor!');
            console.error('Erro na requisição AJAX:', error);
            console.log(xhr.responseText); // mostra erro detalhado no console
        }
    });
};
