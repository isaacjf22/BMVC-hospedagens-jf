<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hospedagem JF | Quartos</title>
    <link rel="stylesheet" href="/static/css/inicio.css">
    <script src="/static/js/inicio.js" defer></script>
</head>

<body>
    <header class="topo">
        <h1>Hospedagem JF</h1>
        <p>Quartos confortáveis, café da manhã caseiro e atendimento de família.</p>
        <nav class="menu">
            <a href="/" class="atual">Página inicial</a>
            <a href="/quartos">Gerenciar quartos</a>
        </nav>
    </header>

    <section class="destaque">
        <strong>{{livres}}</strong> de <strong>{{len(quartos)}}</strong> quartos disponíveis hoje
    </section>

    <main>
        <h2>Nossos quartos</h2>

        <div class="filtros">
            <div class="botoes-status">
                <button class="filtro ativo" data-status="todos">Todos</button>
                <button class="filtro" data-status="disponivel">Disponíveis</button>
                <button class="filtro" data-status="ocupado">Ocupados</button>
                <button class="filtro" data-status="manutencao">Em manutenção</button>
            </div>

            <label>
                Tipo:
                <select id="filtro-tipo">
                    <option value="todos">Todos</option>
                    <option value="Solteiro">Solteiro</option>
                    <option value="Casal">Casal</option>
                    <option value="Família">Família</option>
                    <option value="Suíte">Suíte</option>
                </select>
            </label>
        </div>

        <p id="contador" class="contador"></p>

        <div class="grade-quartos">
            % for quarto in quartos:
            <article class="quarto" data-status="{{quarto.status}}" data-tipo="{{quarto.tipo}}">
                <h3>Quarto {{quarto.numero}}</h3>
                <p class="tipo">{{quarto.tipo}}</p>
                <ul>
                    <li>Capacidade: {{quarto.capacidade}} pessoa(s)</li>
                    <li>Diária: R$ {{'%.2f' % quarto.diaria}}</li>
                </ul>
                <span class="selo {{quarto.status}}">{{quarto.rotulo_status}}</span>
            </article>
            % end
        </div>

        <p id="vazio" class="vazio" hidden>Nenhum quarto encontrado com esses filtros.</p>
    </main>

    <footer class="rodape">
        Hospedagem JF &middot; Projeto BMVC II &middot; Orientação a Objetos (UnB)
    </footer>
</body>

</html>
