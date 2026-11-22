% editando = numero_original is not None
<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hospedagem JF | {{'Editar quarto' if editando else 'Novo quarto'}}</title>
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
        % if usuario:
        <div class="usuario-logado">
            <span>Logado como <strong>{{usuario.nome}}</strong></span>
            <span class="perfil">{{usuario.rotulo_perfil}}</span>
            <a href="/logout" id="sair">Sair</a>
        </div>
        % end
    </header>

    <main>
        % if editando:
        <h2>Editar quarto {{numero_original}}</h2>
        % else:
        <h2>Cadastrar novo quarto</h2>
        % end

        % if erro:
        <p class="aviso erro">{{erro}}</p>
        % end

        % acao = '/quartos/%s/editar' % numero_original if editando else '/quartos/novo'
        <form action="{{acao}}" method="post" id="form-quarto" class="form-quarto" novalidate>
            <label>
                Número do quarto
                <input type="number" name="numero" value="{{dados.get('numero', '')}}" min="1" required>
            </label>

            <label>
                Tipo
                <select name="tipo" required>
                    <option value="">Selecione</option>
                    % for tipo in tipos:
                    <option value="{{tipo}}" {{'selected' if dados.get('tipo') == tipo else ''}}>{{tipo}}</option>
                    % end
                </select>
            </label>

            <label>
                Capacidade (pessoas)
                <input type="number" name="capacidade" value="{{dados.get('capacidade', '')}}" min="1" max="10" required>
            </label>

            <label>
                Diária (R$)
                <input type="text" name="diaria" value="{{dados.get('diaria', '')}}" inputmode="decimal" required>
            </label>

            <label>
                Status
                <select name="status" required>
                    % for chave, rotulo in status.items():
                    <option value="{{chave}}" {{'selected' if dados.get('status') == chave else ''}}>{{rotulo}}</option>
                    % end
                </select>
            </label>

            <p id="erros-form" class="aviso erro" hidden></p>

            <div class="botoes-form">
                <button type="submit" class="botao principal">{{'Salvar alterações' if editando else 'Cadastrar quarto'}}</button>
                <a href="/quartos" class="botao">Cancelar</a>
            </div>
        </form>
    </main>

    <footer class="rodape">
        Hospedagem JF &middot; Projeto BMVC IV &middot; Orientação a Objetos (UnB)
    </footer>
</body>

</html>
