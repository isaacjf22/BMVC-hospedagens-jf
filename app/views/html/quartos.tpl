<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hospedagem JF | Gerenciar quartos</title>
    <link rel="stylesheet" href="/static/css/inicio.css">
    <link rel="stylesheet" href="/static/css/gestao.css">
    <link rel="stylesheet" href="/static/css/realtime.css">
    <script src="/static/js/gestao.js" defer></script>
    <!-- Nível IV: cliente Socket.IO (v4, compatível com o python-socketio 5) -->
    <script src="/static/js/socket.io.min.js" defer></script>
    <script src="/static/js/realtime.js" defer></script>
</head>

<body>
    <header class="topo">
        <h1>Hospedagem JF</h1>
        <p>Gerenciamento dos quartos da hospedagem.</p>
        <nav class="menu">
            <a href="/">Página inicial</a>
            <a href="/quartos" class="atual">Gerenciar quartos</a>
        </nav>
        % if usuario:
        <div class="usuario-logado">
            <span>Logado como <strong>{{usuario.nome}}</strong></span>
            <span class="perfil">{{usuario.rotulo_perfil}}</span>
            <a href="/logout" id="sair">Sair</a>
        </div>
        % end
    </header>

    <main>
        <div class="cabecalho-gestao">
            <h2>Quartos cadastrados</h2>
            <span id="conexao" class="conexao">Conectando…</span>
            <a href="/quartos/novo" class="botao principal">+ Novo quarto</a>
        </div>

        % if mensagem:
        <p id="aviso" class="aviso sucesso">{{mensagem}}</p>
        % end

        <div class="busca">
            <input type="search" id="busca" placeholder="Buscar por número, tipo ou status">
            <span id="contador-busca" class="contador"></span>
        </div>

        <!-- Avisos das alterações feitas em outras abas (tempo real) -->
        <div id="notificacoes" class="notificacoes" aria-live="polite"></div>

        <table class="tabela-quartos" {{'' if quartos else 'hidden'}}>
            <thead>
                <tr>
                    <th>Número</th>
                    <th>Tipo</th>
                    <th>Capacidade</th>
                    <th>Diária</th>
                    <th>Status</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                % for quarto in quartos:
                <tr data-numero="{{quarto.numero}}">
                    <td data-rotulo="Número">{{quarto.numero}}</td>
                    <td data-rotulo="Tipo">{{quarto.tipo}}</td>
                    <td data-rotulo="Capacidade">{{quarto.capacidade}} pessoa(s)</td>
                    <td data-rotulo="Diária">R$ {{'%.2f' % quarto.diaria}}</td>
                    <td data-rotulo="Status">
                        <span class="selo {{quarto.status}}">{{quarto.rotulo_status}}</span>
                    </td>
                    <td class="acoes">
                        <a href="/quartos/{{quarto.numero}}/editar" class="botao">Editar</a>
                        <form action="/quartos/{{quarto.numero}}/excluir" method="post"
                              class="form-excluir" data-numero="{{quarto.numero}}">
                            <button type="submit" class="botao perigo">Excluir</button>
                        </form>
                    </td>
                </tr>
                % end
            </tbody>
        </table>
        <p id="sem-resultado" class="vazio" hidden>Nenhum quarto encontrado nessa busca.</p>
        <p id="sem-quartos" class="vazio" {{'hidden' if quartos else ''}}>Nenhum quarto cadastrado ainda.</p>
    </main>

    <footer class="rodape">
        Hospedagem JF &middot; Projeto BMVC IV &middot; Orientação a Objetos (UnB)
    </footer>
</body>

</html>
