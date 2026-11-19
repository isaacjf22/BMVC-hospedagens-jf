// Filtra os quartos da página inicial por status e por tipo.

let statusEscolhido = 'todos';

function aplicarFiltros() {
    const tipoEscolhido = document.getElementById('filtro-tipo').value;
    const quartos = document.querySelectorAll('.quarto');
    let visiveis = 0;

    quartos.forEach(function (quarto) {
        const statusOk = statusEscolhido === 'todos' || quarto.dataset.status === statusEscolhido;
        const tipoOk = tipoEscolhido === 'todos' || quarto.dataset.tipo === tipoEscolhido;
        const mostrar = statusOk && tipoOk;

        quarto.hidden = !mostrar;
        if (mostrar) {
            visiveis++;
        }
    });

    document.getElementById('contador').textContent =
        'Mostrando ' + visiveis + ' de ' + quartos.length + ' quartos';
    document.getElementById('vazio').hidden = visiveis > 0;
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.filtro').forEach(function (botao) {
        botao.addEventListener('click', function () {
            document.querySelector('.filtro.ativo').classList.remove('ativo');
            botao.classList.add('ativo');
            statusEscolhido = botao.dataset.status;
            aplicarFiltros();
        });
    });

    document.getElementById('filtro-tipo').addEventListener('change', aplicarFiltros);

    aplicarFiltros();
});
