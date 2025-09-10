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
    url: "../PHP/loginAluno.php",
    type: "POST",
    data: { rm, senha },
    dataType: "json",
    success: function(response) {
      if (response.status == "success") {
        // Redireciona para dashboard
        window.location.href = "AreaAluno.html";
      } else {
        // Mostra mensagem de erro
        alert("RM ou senha incorretos!");
        console.log(response);
      }
    },
    error: function(xhr, status, error) {
      console.error("Erro na requisição:", status, error);
      // Adicione aqui o tratamento de erro, como exibir mensagem ao usuário
    }
  });
}

function loginFuncionario() {
const CPF = document.getElementById("CPF").value.trim();
const Senha = document.getElementById("SenhaFunc").value.trim();
  $.ajax({
    url: "../PHP/loginProf.php",
    type: "POST",
    data: { CPF, Senha },
    dataType: "json",
    success: function(response) {
      if (response.status == "success") {
        // Redireciona para dashboard
        alert("Login realizado com sucesso!");
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
