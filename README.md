# Hospedagem JF

Sistema web de controle de hospedagem, desenvolvido em **Python** com o framework **Bottle** para a disciplina **Orientação a Objetos** do **Prof. Henrique Moura** (UnB), na trilha **BMVC** (Bottle + MVC).

O projeto parte da base [bmvc_start_from_this](https://github.com/hgmachine/bmvc_start_from_this), fornecida pelo professor, e evolui em quatro níveis, liberados aos poucos. Cada nível entregue é marcado por um commit próprio, e o histórico do repositório mostra o sistema crescendo de um nível para o outro.

## Finalidade

Apresentar e gerenciar os quartos de uma hospedagem pela web: quais quartos existem, de que tipo são, quantas pessoas cabem em cada um, quanto custa a diária e se estão disponíveis, ocupados ou em manutenção. A partir do nível 2, os quartos podem ser cadastrados, editados e excluídos pelo navegador.

O projeto segue a arquitetura **MVC** no formato do BMVC: as rotas ficam no `route.py`, o controlador `Application` decide qual página montar, o `DataRecord` cuida do acesso aos dados e as páginas são templates `.tpl` do Bottle, com CSS e JavaScript próprios.

## Níveis do projeto

| Nível | Propósito | Interface | Vídeo | Commit de entrega | Status |
|:---:|---|---|---|---|:---:|
| **1** | Servir uma página própria, com propósito claro, carregando CSS e JS funcionais | Web (`/`) | [Assistir](https://youtu.be/LI_jX0NuIfc) | `nivel 1 concluído` | Concluído |
| **2** | CRUD completo do modelo `Quarto`, com persistência em JSON e validação no servidor | Web (`/quartos`) | (em breve) | `nivel 2 concluído` | Em andamento |
| **3** | A liberar | — | — | — | Bloqueado |
| **4** | A liberar | — | — | — | Bloqueado |

> **Como ler a tabela:** a coluna *Commit de entrega* mostra o nome do commit que marca o nível finalizado. Para ver o projeto naquele momento, basta procurar esse commit (ou a tag de mesmo nome) no histórico.

### Nível 1: Página inicial da hospedagem

**Propósito:** servir uma página estática personalizada, com conteúdo legível e propósito claro, carregando arquivos CSS e JS próprios.

- Rota `/` (e `/inicio`) registrada no `route.py` e tratada pelo `Application`.
- Página `inicio.tpl` com o nome e a descrição da hospedagem, um destaque com a quantidade de quartos livres e a lista de quartos (número, tipo, capacidade, diária e status).
- Classe `Quarto` (Model) e `DataRecord`, que lê os quartos de exemplo do arquivo `quartos.json`.
- **CSS** (`inicio.css`): identidade visual própria, com cartões para os quartos e selos coloridos por status.
- **JS** (`inicio.js`): filtros por status (botões) e por tipo (lista de seleção), com o contador "Mostrando X de Y quartos" e um aviso quando nenhum quarto atende ao filtro.

**Vídeo de apresentação (até 3 min):** [assistir no YouTube](https://youtu.be/LI_jX0NuIfc)

### Nível 2: Gerenciamento de quartos (CRUD)

**Propósito:** servir o modelo `Quarto` em páginas HTML com CRUD completo (criar, listar, editar e excluir), guardando os dados em JSON e carregando CSS e JS próprios.

| Operação | Página / ação | Rota |
|---|---|---|
| **Create** | Formulário de cadastro | `GET /quartos/novo` → `POST /quartos/novo` |
| **Read** | Tabela com todos os quartos (e a página inicial) | `GET /quartos` (e `GET /`) |
| **Update** | Formulário já preenchido com os dados atuais | `GET /quartos/<numero>/editar` → `POST /quartos/<numero>/editar` |
| **Delete** | Botão "Excluir" com confirmação | `POST /quartos/<numero>/excluir` |

- **Model (`Quarto`):** atributos protegidos (`_numero`, `_tipo`...) acessados por `@property`. Cada *setter* valida o valor (número positivo, tipo e status válidos, capacidade de 1 a 10, diária maior que zero) e lança `ValueError` com uma mensagem legível. Tem `to_dict()` e `from_dict()` para converter de/para JSON.
- **DataRecord:** lê e grava o `quartos.json` e oferece os métodos do CRUD (`listar_quartos`, `buscar_quarto`, `adicionar_quarto`, `atualizar_quarto`, `remover_quarto`). Também garante que o número do quarto não se repita. Cada alteração é salva no arquivo, então os dados continuam lá depois de reiniciar o servidor.
- **Application:** um método por página/ação, todos registrados em `self.pages`. O `render()` passou a aceitar um parâmetro (o número do quarto). Quando a validação falha, o formulário volta com a mensagem de erro e os dados digitados; quando dá certo, segue o padrão **POST → redirect → GET**, voltando para a listagem com um aviso de sucesso.
- **CSS** (`gestao.css`): tabela, formulário, botões e avisos de sucesso/erro; no celular a tabela vira uma lista de cartões. O `inicio.css` continua dando a identidade visual (cores, topo e o novo menu de navegação).
- **JS** (`gestao.js`): confirmação antes de excluir, busca na tabela por número/tipo/status com contador, aviso de sucesso que some sozinho e validação do formulário antes do envio (destacando os campos inválidos). O servidor valida de novo, então a regra continua valendo mesmo sem JS.

**Vídeo de apresentação (até 6 min):** em breve

## Funcionalidades

- **Página inicial:** nome, descrição da hospedagem e destaque com quantos quartos estão disponíveis no dia.
- **Quartos:** 8 quartos de exemplo dos tipos Solteiro, Casal, Família e Suíte, com capacidade, diária e status (disponível, ocupado ou em manutenção).
- **Filtros:** por status e por tipo, que podem ser combinados, atualizando a lista sem recarregar a página.
- **Gerenciar quartos** (`/quartos`): cadastrar, editar e excluir quartos, com busca na tabela, confirmação de exclusão e mensagens de erro legíveis (ex.: "Já existe um quarto com o número 101.").

## Arquitetura (MVC)

| Papel | O que faz | Onde está |
|---|---|---|
| **Rota** | Recebe a requisição e só chama `ctl.render('<página>')`. Não contém lógica | `route.py` |
| **Controller** | O `Application` guarda as páginas em `self.pages` e monta cada uma, buscando os dados no `DataRecord` | `app/controllers/application.py` |
| **DataRecord** | Único lugar que lê e grava o arquivo de dados, convertendo-o em objetos do Model, e oferece as operações do CRUD | `app/controllers/datarecord.py` |
| **Model** | Classes com os dados encapsulados e as regras do próprio objeto (validação dos campos, se o quarto está disponível). Não conhece o Bottle | `app/models/` |
| **View** | Templates que exibem os dados, com CSS e JS servidos pela rota `/static` | `app/views/html/` e `app/static/` |

O fluxo de uma requisição é:

```
Navegador  →  route.py  →  Application  →  DataRecord  →  quartos.json
                               ↓                ↓
                  inicio.tpl / quartos.tpl  objetos Quarto
                  quarto_form.tpl
                       (+ CSS e JS)
```

Nas ações que alteram dados (POST), o `Application` pede a operação ao `DataRecord`, que salva o JSON, e então redireciona o navegador de volta para `/quartos`.

Assim, a rota não tem lógica, o controlador não mexe direto no arquivo de dados e a View só exibe o que recebe.

## Estrutura

```
route.py                Ponto de entrada: app Bottle, rotas e servidor na porta 8080
app/
├── controllers/
│   ├── application.py  Application: mapeia as páginas e renderiza os templates
│   ├── datarecord.py   DataRecord: lê, grava e faz o CRUD dos quartos no JSON
│   └── db/
│       └── quartos.json  "Banco" dos quartos
├── models/
│   └── quarto.py       Classe Quarto (encapsulamento e validação)
├── views/html/
│   ├── inicio.tpl      Página inicial da hospedagem
│   ├── quartos.tpl     Listagem de gerenciamento (Read e Delete)
│   ├── quarto_form.tpl Formulário de cadastro e edição (Create e Update)
│   └── helper.tpl      Página de exemplo da base do professor
└── static/
    ├── css/            inicio.css, gestao.css (e helper.css, da base)
    ├── js/             inicio.js, gestao.js (e helper.js, da base)
    └── img/
Dockerfile              Imagem com Python 3.12 e as bibliotecas do BMVC
bmvc_setup.sh           Comandos para criar e rodar o container
docker_install.sh       Instalação do Docker no Ubuntu
LICENSE                 Licença MIT
```

A estrutura de pastas é herdada da base do professor e se mantém em todos os níveis. O que muda de um nível para o outro são as páginas, os modelos e os dados.

## Como executar

### Localmente

É necessário ter o **Python 3** instalado.

```bash
git clone https://github.com/isaacjf22/BMVC-hospedagens-jf.git
cd BMVC-hospedagens-jf
pip install bottle
python route.py
```

Depois, abra **http://localhost:8080/** no navegador. O gerenciamento de quartos fica em **http://localhost:8080/quartos**. A página de exemplo da base continua disponível em `/helper`.

> O terminal mostra `Listening on http://0.0.0.0:8080/`, mas no navegador use **`localhost:8080`**: o endereço `0.0.0.0` não abre no Windows.

### Com Docker

```bash
docker build -t bmvci .
docker run -d -p 8080:8080 -v $(pwd):/bmeta bmvci
```

O container instala o Bottle e as demais bibliotecas do BMVC e executa o `route.py`. A página fica no mesmo endereço: **http://localhost:8080/**.

### Problemas comuns

| Mensagem ou sintoma | Causa provável | Solução |
|---|---|---|
| `ModuleNotFoundError: No module named 'bottle'` | O Bottle não está instalado | Rodar `pip install bottle` |
| "Não é possível acessar esse site" ou erro `-108` (`ERR_ADDRESS_INVALID`) no navegador | Foi aberto o endereço `http://0.0.0.0:8080/` mostrado no terminal, ou o servidor não está rodando | Abrir **http://localhost:8080/** com o `route.py` rodando |
| `Not found: '/...'` (erro 404) | A rota digitada não existe | Usar `/`, `/inicio`, `/quartos`, `/quartos/novo` ou `/helper` |
| `OSError: [WinError 10048]` ou `Address already in use` | Já existe outro programa (ou outro servidor) usando a porta 8080 | Fechar o servidor anterior (Ctrl + C no terminal) e rodar de novo |
| Página sem estilo ou filtros sem funcionar | O CSS ou o JS não foi carregado | Conferir no F12, aba *Rede*, se os arquivos `.css` e `.js` da página retornam status 200 |
| `python` não é reconhecido (Windows) | O Python não está no PATH | Usar `py route.py` ou reinstalar o Python marcando *Add to PATH* |

Para ver o sistema exatamente como estava em um nível, use o commit de entrega indicado na [tabela de níveis](#níveis-do-projeto).

## Autor

[Isaac Ferreira](https://github.com/isaacjf22)
