// Nível IV: atualização da tabela de quartos em tempo real (WebSocket).
// O servidor avisa quando um quarto é criado, editado ou excluído em
// qualquer aba; aqui a tabela é atualizada sem recarregar a página.
// Este arquivo só EXIBE as mudanças: quem grava são as rotas POST.

(function () {
    const tabela = document.querySelector('.tabela-quartos');
    if (!tabela || typeof io === 'undefined') return;

    const corpo = tabela.querySelector('tbody');
    const indicador = document.getElementById('conexao');
    const semQuartos = document.getElementById('sem-quartos');
    const notificacoes = document.getElementById('notificacoes');

    // io() conecta no mesmo servidor da página e envia o cookie de sessão.
    const socket = io();

    // ------------------------------------------------------------------
    // Indicador de conexão

    function mostrarEstado(classe, texto) {
        indicador.className = 'conexao ' + classe;
        indicador.textContent = texto;
    }

    socket.on('connect', function () {
        mostrarEstado('conectado', 'Tempo real: conectado');
    });
    socket.on('disconnect', function () {
        mostrarEstado('reconectando', 'Reconectando…');
    });
    socket.on('connect_error', function () {
        // Ex.: servidor desligado ou sessão encerrada (login recusado).
        mostrarEstado('desconectado', 'Tempo real: sem conexão');
    });

    // ------------------------------------------------------------------
    // Eventos enviados pelo servidor (classe Realtime)

    socket.on('quarto_criado', function (quarto) {
        if (buscarLinha(quarto.numero)) return;  // a linha já existe
        inserirOrdenado(criarLinha(quarto));
        destacar(buscarLinha(quarto.numero));
        notificar('Quarto ' + quarto.numero + ' cadastrado.');
        atualizarTela();
    });

    socket.on('quarto_atualizado', function (dados) {
        const antiga = buscarLinha(dados.numero_original);
        if (antiga) antiga.remove();
        inserirOrdenado(criarLinha(dados.quarto));
        destacar(buscarLinha(dados.quarto.numero));
        notificar('Quarto ' + dados.quarto.numero + ' atualizado ('
                  + dados.quarto.rotulo_status + ').');
        atualizarTela();
    });

    socket.on('quarto_excluido', function (dados) {
        const linha = buscarLinha(dados.numero);
        if (!linha) return;
        linha.classList.add('saindo');  // animação antes de sumir
        setTimeout(function () {
            linha.remove();
            atualizarTela();
        }, 600);
        notificar('Quarto ' + dados.numero + ' excluído.');
    });

    // ------------------------------------------------------------------
    // Auxiliares de DOM

    function buscarLinha(numero) {
        return corpo.querySelector('tr[data-numero="' + numero + '"]');
    }

    // Cria a <td> com textContent (nunca innerHTML com dados recebidos).
    function celula(rotulo, texto) {
        const td = document.createElement('td');
        td.dataset.rotulo = rotulo;
        td.textContent = texto;
        return td;
    }

    // Monta uma linha igual às que o quartos.tpl gera no servidor.
    function criarLinha(quarto) {
        const tr = document.createElement('tr');
        tr.dataset.numero = quarto.numero;

        tr.appendChild(celula('Número', quarto.numero));
        tr.appendChild(celula('Tipo', quarto.tipo));
        tr.appendChild(celula('Capacidade', quarto.capacidade + ' pessoa(s)'));
        tr.appendChild(celula('Diária', 'R$ ' + Number(quarto.diaria).toFixed(2)));

        const tdStatus = celula('Status', '');
        const selo = document.createElement('span');
        selo.className = 'selo ' + quarto.status;
        selo.textContent = quarto.rotulo_status;
        tdStatus.appendChild(selo);
        tr.appendChild(tdStatus);

        const tdAcoes = document.createElement('td');
        tdAcoes.className = 'acoes';
        const editar = document.createElement('a');
        editar.href = '/quartos/' + quarto.numero + '/editar';
        editar.className = 'botao';
        editar.textContent = 'Editar';
        const form = document.createElement('form');
        form.action = '/quartos/' + quarto.numero + '/excluir';
        form.method = 'post';
        form.className = 'form-excluir';
        form.dataset.numero = quarto.numero;
        const excluir = document.createElement('button');
        excluir.type = 'submit';
        excluir.className = 'botao perigo';
        excluir.textContent = 'Excluir';
        form.appendChild(excluir);
        tdAcoes.appendChild(editar);
        tdAcoes.appendChild(form);
        tr.appendChild(tdAcoes);
        return tr;
    }

    // Mantém a tabela ordenada pelo número do quarto, como no servidor.
    function inserirOrdenado(nova) {
        const numero = Number(nova.dataset.numero);
        const depois = Array.from(corpo.rows).find(function (linha) {
            return Number(linha.dataset.numero) > numero;
        });
        corpo.insertBefore(nova, depois || null);
    }

    // Destaque visual breve na linha que mudou.
    function destacar(linha) {
        linha.classList.add('mudou');
        setTimeout(function () { linha.classList.remove('mudou'); }, 2500);
    }

    // Aviso flutuante que some sozinho.
    function notificar(texto) {
        const aviso = document.createElement('p');
        aviso.className = 'notificacao';
        aviso.textContent = texto;
        notificacoes.appendChild(aviso);
        setTimeout(function () { aviso.remove(); }, 5000);
    }

    // Mostra/esconde a tabela vazia e reaplica a busca do gestao.js.
    function atualizarTela() {
        const vazia = corpo.rows.length === 0;
        tabela.hidden = vazia;
        semQuartos.hidden = !vazia;
        if (window.atualizarBusca) window.atualizarBusca();
    }
})();
