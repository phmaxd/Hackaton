const textos = [
    "Agilize a rotina de criação de provas com nosso sistema <br> prático e inteligente",
    "Professores podem divulgar gabaritos de forma rápida, precisa e <br> automatizada, economizando tempo e reduzindo erros.",
    "Mais eficiência para você, mais resultados para seus alunos!"
];

const carousel = document.getElementById('carouselExample');
const texto = document.getElementById('carousel-text');

carousel.addEventListener('slid.bs.carousel', function (event) {
    const index = event.to; // índice do slide ativo
    texto.innerHTML = `<strong>${textos[index]}</strong>`;
});