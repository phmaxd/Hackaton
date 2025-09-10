const profButton = document.getElementById("profButton");
const alunButton = document.getElementById("alunButton");
const formContainer = document.getElementById("formContainer");

alunButton.addEventListener("click", function(){
    this.style.color = "red";
    profButton.style.color = "black";
    formContainer.style.animation = "lado"

        formContainer.style.transform = "translate(-150vh, -50%)"

      // depois de 0.5s (tempo da transição), remove a classe
      // pra ele voltar
      setTimeout(() => {
    formContainer.innerHTML = `
                    <span id="formTitulo">
                    <h1>ALUNO</h1>
                </span>
                <span id="imgUserContent">
                    <img id="imgUser" src="../SRC/ICONS/userBola.png" alt="">
                </span>
                <span id="labelForm">
                    <p>Insira os Dados</p>
                </span>
                <span id="rmContent">
                    <i class="fa-solid fa-user"></i>
                    <input type="text" value="" placeholder="INSIRA SEU RM" id="rmInput">
                </span>
                <span id="senhaContent">
                    <i class="fa-solid fa-lock"></i>
                    <input type="password" value="" placeholder="INSIRA SUA SENHA" id="senhaInput">
                </span>
                <span id="entrarContent">
                    <input type="button" id="entrarButton" value="ENTRAR">
                </span>`; 

        formContainer.style.transform = "translate(-50%, -50%)"
      }, 500); // 0.5 segundos

})

profButton.addEventListener("click", function(){
    this.style.color = "red";
    alunButton.style.color = "black";
    formContainer.style.transform = "translate(-150vh, -50%)"
          setTimeout(() => {
    formContainer.innerHTML = `
                    <span id="formTitulo">
                    <h1>FUNCIONÁRIO</h1>
                </span>
                <span id="imgUserContent">
                    <img id="imgUser" src="../SRC/ICONS/userBola.png" alt="">
                </span>
                <span id="labelForm">
                    <p>Insira os Dados</p>
                </span>
                <span id="rmContent">
                    <i class="fa-solid fa-user"></i>
                    <input type="text" value="" placeholder="INSIRA SEU CPF" id="rmInput">
                </span>
                <span id="senhaContent">
                    <i class="fa-solid fa-lock"></i>
                    <input type="password" value="" placeholder="INSIRA SUA SENHA" id="senhaInput">
                </span>
                <span id="entrarContent">
                    <input type="button" id="entrarButton" value="ENTRAR">
                </span>`; 


        formContainer.style.transform = "translate(-50%, -50%)"
      }, 500); // 0.5 segundos


})



