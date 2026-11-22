// Interações das páginas de gerenciamento de quartos.
// O servidor valida tudo de novo: o JS só deixa o uso mais confortável.

// 1. Confirmação antes de excluir um quarto
// O "ouvinte" fica no documento (delegação de eventos), então vale também
// para as linhas que chegam depois, em tempo real, pelo realtime.js.
function prepararExclusao() {
    document.addEventListener('submit', function (evento) {
        const form = evento.target;
        if (!form.classList.contains('form-excluir')) return;
        const numero = form.dataset.numero;
        if (!confirm('Excluir o quarto ' + numero + '? Essa ação não pode ser desfeita.')) {
            evento.preventDefault();
        }
    });
}

// 2. Busca na tabela por número, tipo ou status, com contador
function prepararBusca() {
    const campo = document.getElementById('busca');
    if (!campo) return;

    const contador = document.getElementById('contador-busca');
    const semResultado = document.getElementById('sem-resultado');

    function filtrar() {
        // As linhas são buscadas de novo a cada vez, porque o tempo real
        // pode ter adicionado ou removido alguma.
        const linhas = document.querySelectorAll('.tabela-quartos tbody tr');
        const termo = campo.value.trim().toLowerCase();
        let visiveis = 0;
        linhas.forEach(function (linha) {
            const combina = linha.textContent.toLowerCase().includes(termo);
            linha.hidden = !combina;
            if (combina) visiveis++;
        });
        contador.textContent = 'Mostrando ' + visiveis + ' de ' + linhas.length + ' quartos';
        if (semResultado) semResultado.hidden = visiveis > 0 || linhas.length === 0;
    }

    campo.addEventListener('input', filtrar);
    window.atualizarBusca = filtrar;  // usado pelo realtime.js
    filtrar();
}

// 3. Aviso de sucesso que some sozinho depois de alguns segundos
function esconderAviso() {
    const aviso = document.getElementById('aviso');
    if (!aviso) return;
    setTimeout(function () {
        aviso.classList.add('sumindo');
        setTimeout(function () { aviso.remove(); }, 600);
    }, 4000);
}

// 4. Validação do formulário antes de enviar (mesmas regras do Model)
function prepararFormulario() {
    const form = document.getElementById('form-quarto');
    if (!form) return;

    const caixaErros = document.getElementById('erros-form');

    form.addEventListener('submit', function (evento) {
        const erros = [];
        form.querySelectorAll('.invalido').forEach(function (c) {
            c.classList.remove('invalido');
        });

        function marcar(nome, mensagem) {
            form.elements[nome].classList.add('invalido');
            erros.push(mensagem);
        }

        const numero = Number(form.elements.numero.value);
        if (!Number.isInteger(numero) || numero <= 0) {
            marcar('numero', 'O número do quarto deve ser um inteiro maior que zero.');
        }
        if (form.elements.tipo.value === '') {
            marcar('tipo', 'Escolha um tipo de quarto.');
        }
        const capacidade = Number(form.elements.capacidade.value);
        if (!Number.isInteger(capacidade) || capacidade < 1 || capacidade > 10) {
            marcar('capacidade', 'A capacidade deve ficar entre 1 e 10 pessoas.');
        }
        const diaria = Number(form.elements.diaria.value.replace(',', '.'));
        if (form.elements.diaria.value.trim() === '' || isNaN(diaria) || diaria <= 0) {
            marcar('diaria', 'O valor da diária deve ser maior que zero.');
        }

        if (erros.length > 0) {
            evento.preventDefault();
            caixaErros.innerHTML = erros.join('<br>');
            caixaErros.hidden = false;
        }
    });
}

prepararExclusao();
prepararBusca();
esconderAviso();
prepararFormulario();
