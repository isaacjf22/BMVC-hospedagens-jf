<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hospedagem JF | Gerenciar quartos</title>
    <link rel="stylesheet" href="/static/css/inicio.css">
    <link rel="stylesheet" href="/static/css/gestao.css">
    <script src="/static/js/gestao.js" defer></script>
</head>

<body>
    <header class="topo">
        <h1>Hospedagem JF</h1>
        <p>Gerenciamento dos quartos da hospedagem.</p>
        <nav class="menu">
            <a href="/">Página inicial</a>
            <a href="/quartos" class="atual">Gerenciar quartos</a>
        </nav>
    </header>

    <main>
        <div class="cabecalho-gestao">
            <h2>Quartos cadastrados</h2>
            <a href="/quartos/novo" class="botao principal">+ Novo quarto</a>
        </div>

        % if mensagem:
        <p id="aviso" class="aviso sucesso">{{mensagem}}</p>
        % end

        <div class="busca">
            <input type="search" id="busca" placeholder="Buscar por número, tipo ou status">
            <span id="contador-busca" class="contador"></span>
        </div>

        % if quartos:
        <table class="tabela-quartos">
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
                <tr>
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
        % else:
        <p class="vazio">Nenhum quarto cadastrado ainda.</p>
        % end
    </main>

    <footer class="rodape">
        Hospedagem JF &middot; Projeto BMVC II &middot; Orientação a Objetos (UnB)
    </footer>
</body>

</html>
