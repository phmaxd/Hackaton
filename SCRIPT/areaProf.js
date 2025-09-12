const salasTh = document.querySelectorAll(".salasTh")
const semestresTh = document.querySelectorAll(".semestresTh")
const seriesTh = document.querySelectorAll(".seriesTh")
let Ths = [salasTh, semestresTh, seriesTh]


  function bola() {
    event.preventDefault(); // Impede o envio padrão do formulário
    const rm = document.getElementById("rm").value.trim(); // Obtém o valor do campo RM
    const fileInput = document.getElementById('file-upload').files[0]; // Corrigido para id="file-upload"
    const file = fileInput[0];

    if (!rm || !file) {
        alert("preencha o RM e selecione a imagem!")
    return;
    }

    const formData = new formData();
    formData.append('rm', rm);
    formData.append('file', file);

    try {
        $.ajax({
            method: "POST",
            url: "../PHP/processar.php",
            data: formData,
        });
     const data = ajax.json();
     if (data.status === "success") {
        alert("Imagem enviada com sucesso!");
     }
     else {
        alert("Erro ao enviar a imagem.");
     }   
    } catch (error) {
      console.log('fudeu')  
    }
}


Ths.forEach(i => {

i.forEach(ii => {
    ii.addEventListener("click", function(){
        i.forEach(e => {
            e.style.color = "#636363"
        });
        ii.style.color = "#B00D0D"
})
});


})




        function deslogar() {
            if(confirm("Você tem certeza que dejesa sair de sua Conta?")){
            $.ajax({
                url: "../PHP/logout.php",
                type: "POST",
                dataType: "json",
                success: function(response) {
                    if (response.status === "success") {
                        window.location.href = "../HTML/index.html";
                    } else {
                        alert("Erro ao deslogar!");
                    }
                },
                error: function(xhr, status, error) {
                    console.error("Erro na requisição:", status, error);
                    alert("Ocorreu um erro ao tentar deslogar. Tente novamente.");
                }
            });
            }
        }