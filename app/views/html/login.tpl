<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hospedagem JF | Entrar</title>
    <link rel="stylesheet" href="/static/css/inicio.css">
    <link rel="stylesheet" href="/static/css/login.css">
    <script src="/static/js/login.js" defer></script>
</head>

<body class="pagina-login">
    <header class="topo">
        <h1>Hospedagem JF</h1>
        <p>Área da equipe: acesso restrito a funcionários.</p>
        <nav class="menu">
            <a href="/">Página inicial</a>
            <a href="/login" class="atual">Entrar</a>
        </nav>
    </header>

    <main>
        <section class="cartao-login">
            <h2>Entrar no sistema</h2>
            <p class="explicacao">Use seu login e senha para gerenciar os quartos da hospedagem.</p>

            % if aviso:
            <p class="aviso-login info">{{aviso}}</p>
            % end

            % if erro:
            <p class="aviso-login erro" role="alert">{{erro}}</p>
            % end

            % if sem_usuarios:
            <p class="aviso-login info">
                Nenhum usuário cadastrado ainda. No terminal, rode
                <code>python criar_usuario.py</code> para criar o primeiro administrador.
            </p>
            % end

            <form action="/login" method="post" id="form-login" novalidate>
                <label for="campo-login">Login</label>
                <input type="text" id="campo-login" name="login" value="{{login_digitado}}"
                       autocomplete="username" autofocus required>

                <label for="campo-senha">Senha</label>
                <div class="campo-senha">
                    <input type="password" id="campo-senha" name="senha"
                           autocomplete="current-password" required>
                    <button type="button" id="mostrar-senha" class="mostrar-senha"
                            aria-label="Mostrar senha">Mostrar</button>
                </div>
                <p id="aviso-caps" class="aviso-caps" hidden>Caps Lock está ligado.</p>

                <p id="erro-js" class="aviso-login erro" hidden></p>

                <button type="submit" class="botao-entrar">Entrar</button>
            </form>
        </section>
    </main>

    <footer class="rodape">
        Hospedagem JF &middot; Projeto BMVC IV &middot; Orientação a Objetos (UnB)
    </footer>
</body>

</html>
