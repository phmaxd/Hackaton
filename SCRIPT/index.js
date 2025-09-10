const telaInicial = document.getElementById("tela-inicial");
const loginAlunoDiv = document.getElementById("login-aluno");
const loginFuncDiv = document.getElementById("login-funcionario");

document.getElementById("btnAluno").addEventListener("click", function() {
    telaInicial.style.display = "none";
    loginAlunoDiv.style.display = "block";
});

document.getElementById("btnFuncionario").addEventListener("click", function() {
    telaInicial.style.display = "none";
    loginFuncDiv.style.display = "block";
});

function voltar() {
    loginAlunoDiv.style.display = "none";
    loginFuncDiv.style.display = "none";
    telaInicial.style.display = "block";
}

function loginAluno() {
    const rm = document.getElementById("rm").value.trim();
    const senha = document.getElementById("senha").value.trim();

    $.ajax({
        url: '../PHP/loginAluno.php', // URL do PHP
        type: 'POST',
        data: {
            rm: rm,
            senha: senha
        },
        dataType: 'json',
        success: function(response) {
            console.log(response); // Exibe a resposta real do servidor
            if (response.status == 'success') {
                alert('Usuário logado como ' + response.rm);
                window.location.href = '../HTML/AreaAluno.html';
            } else {
                alert(response.message || 'Erro ao tentar fazer login.');
            }
        },
        error: function(xhr, error) {
            console.error('Erro na requisição AJAX:', error);
            console.log(xhr.responseText); // Exibe a resposta completa da requisição para depuração
        }
    });
}

function loginFuncionario() {
    const CPF = document.getElementById("CPF").value.trim();
    const Senha = document.getElementById("SenhaFunc").value.trim();
    
    $.ajax({
        url: "../PHP/loginProf.php", // URL para o PHP do funcionário
        type: "POST",
        data: {
            CPF: CPF,
            senha: Senha
        },
        dataType: "json",
        success: function(response) {
            if (response.status === "success") {
                // Redireciona para o dashboard
                window.location.href = "AreaProf.html";
            } else {
                // Mostra mensagem de erro
                alert("CPF ou senha incorretos!");
                console.log(response);
            }
        },
        error: function(xhr, status, error) {
            console.error("Erro na requisição:", status, error);
            // Adicione aqui o tratamento de erro, como exibir mensagem ao usuário
        }
    });
}
