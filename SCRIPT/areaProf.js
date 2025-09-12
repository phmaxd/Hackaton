const salasTh = document.querySelectorAll(".salasTh")
const semestresTh = document.querySelectorAll(".semestresTh")
const seriesTh = document.querySelectorAll(".seriesTh")
let Ths = [salasTh, semestresTh, seriesTh]


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

        function trastejo(card) {
            if(card === 'provaCard') {
                document.getElementById("provaP").style.borderTop = "dashed #636363 0.5vh";
            } else if(card === 'gabaritoCard') {
                document.getElementById("gabaritoP").style.borderTop = "dashed #636363 0.5vh";
            }
        }
        function  sairTrastejo(card) {
            if(card === 'provaCard') {
                document.getElementById("provaP").style.borderTop = "solid #636363 0.5vh";
            } else if(card === 'gabaritoCard') {
                document.getElementById("gabaritoP").style.borderTop = "solid #636363 0.5vh";
            }
        }

        function mudarTela(){
            window.location = "ElaborarProvas.html"
        }
        function mudarTelaCorrecoes(){
            window.location = "SubirImg.html"
        }
        function mudarTelaAreaProf(){
            window.location = "AreaProf.html"
        }
        