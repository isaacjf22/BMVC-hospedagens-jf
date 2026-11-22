# Hospedagem JF

Sistema web de controle de hospedagem, desenvolvido em **Python** com o framework **Bottle** para a disciplina **Orientação a Objetos** do **Prof. Henrique Moura** (UnB), na trilha **BMVC** (Bottle + MVC).

O projeto parte da base [bmvc_start_from_this](https://github.com/hgmachine/bmvc_start_from_this), fornecida pelo professor, e evolui em quatro níveis, liberados aos poucos. Cada nível entregue é marcado por um commit próprio, e o histórico do repositório mostra o sistema crescendo de um nível para o outro.

## Finalidade

Apresentar e gerenciar os quartos de uma hospedagem pela web: quais quartos existem, de que tipo são, quantas pessoas cabem em cada um, quanto custa a diária e se estão disponíveis, ocupados ou em manutenção. A partir do nível 2, os quartos podem ser cadastrados, editados e excluídos pelo navegador. A partir do nível 3, essa gestão fica numa área restrita, que só abre para funcionários com login e senha. No nível 4, as mudanças nos quartos aparecem **em tempo real** para todos que estão com a gestão aberta, via WebSocket.

O projeto segue a arquitetura **MVC** no formato do BMVC: as rotas ficam no `route.py`, o controlador `Application` decide qual página montar, o `DataRecord` cuida do acesso aos dados e as páginas são templates `.tpl` do Bottle, com CSS e JavaScript próprios.

## Níveis do projeto

| Nível | Propósito | Interface | Vídeo | Commit de entrega | Status |
|:---:|---|---|---|---|:---:|
| **1** | Servir uma página própria, com propósito claro, carregando CSS e JS funcionais | Web (`/`) | [Assistir](https://youtu.be/LI_jX0NuIfc) | `nivel 1 concluído` | Concluído |
| **2** | CRUD completo do modelo `Quarto`, com persistência em JSON e validação no servidor | Web (`/quartos`) | [Assistir](https://youtu.be/LgQ_bkzLPaE) | `nivel 2 concluído` | Concluído |
| **3** | Controle de acesso: login, sessão e área restrita protegendo o CRUD de quartos | Web (`/login`) | [Assistir](https://youtu.be/98v4sIiP1ZQ) | `nivel 3 concluído` | Concluído |
| **4** | Atualização em tempo real (WebSocket/Socket.IO) da gestão de quartos entre várias abas e usuários | Web (`/quartos`) | — | `nivel 4 concluído` | Concluído |

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

**Vídeo de apresentação (até 6 min):** [assistir no YouTube](https://youtu.be/LgQ_bkzLPaE)

### Nível 3: Login e área restrita

**Propósito:** adicionar controle de acesso ao sistema: um **login** para os funcionários da hospedagem e uma **área restrita** (o gerenciamento de quartos), mantendo o CRUD do nível 2 funcionando.

| Página / ação | Rota | Acesso |
|---|---|---|
| Página inicial | `GET /` | Pública |
| Formulário de login | `GET /login` | Pública |
| Conferir login e senha | `POST /login` | Pública |
| Sair do sistema | `GET /logout` | Logado |
| Gerenciar quartos (listar, cadastrar, editar, excluir) | `/quartos...` (GET **e** POST) | **Restrita** |

- **Model (`Usuario`):** login, nome, perfil (`admin` ou `recepcionista`) e a senha guardada **só como hash** (PBKDF2-SHA256 com salt aleatório, usando apenas a biblioteca padrão: `hashlib`, `secrets` e `hmac`). O hash e o salt são atributos **privados** (`__hash_senha`, `__salt`): ninguém de fora lê esses valores, e a única forma de conferir uma senha é o método `verificar_senha()`, que compara com `hmac.compare_digest`.
- **Herança (`ArquivoJSON`):** a leitura e a gravação de JSON, que antes ficavam só no `DataRecord`, foram para uma classe base. `DataRecord` (quartos) e `UsuarioRecord` (usuários) herdam dela e só dizem qual modelo guardam; a conversão usa o `to_dict()`/`from_dict()` de cada modelo (polimorfismo).
- **Auth:** concentra o controle de acesso. Ao entrar, gera um identificador de sessão aleatório (`secrets.token_urlsafe`), guarda no servidor (dicionário id → login) e envia ao navegador num **cookie assinado** (`httponly` e `samesite=lax`). Se o cookie for alterado, a assinatura não confere e o acesso é negado. A chave de assinatura vem da variável de ambiente `HOSPEDAGEM_SEGREDO` (o valor padrão serve só para desenvolvimento).
- **Application:** compõe o `Auth` (`self.auth`), assim como compõe o `DataRecord` (`self.models`). As páginas restritas ficam no conjunto `RESTRITAS`, e o `render()` confere o login **antes** de chamar qualquer uma delas. Como toda rota passa pelo `render()`, as rotas `POST` (criar, editar, excluir) também ficam protegidas. Sem login, o usuário é redirecionado para `/login` com o aviso "Faça login para acessar a área de gestão".
- **Login com erro genérico:** se o login ou a senha estiverem errados, a mensagem é sempre "Usuário ou senha inválidos.", sem dizer qual dos dois errou.
- **Páginas restritas:** mostram o nome e o perfil de quem está logado e o botão **Sair**.
- **CSS** (`login.css`): cartão de login com a identidade visual da hospedagem; o `inicio.css` ganhou a barra do usuário logado.
- **JS** (`login.js`): botão **Mostrar/Ocultar** senha, aviso de **Caps Lock** ligado e bloqueio do envio com campos vazios. Nas páginas de gestão continua o `gestao.js` (busca, confirmação de exclusão etc.).

**Vídeo de apresentação (até 10 min):** [assistir no YouTube](https://youtu.be/98v4sIiP1ZQ)

### Nível 4: Atualização em tempo real (WebSocket)

**Propósito:** quando um funcionário cria, edita (inclusive o status) ou exclui um quarto, **todas as outras abas e usuários com a gestão aberta veem a mudança na hora, sem recarregar a página**. O CRUD do nível 2 e o login do nível 3 continuam valendo.

| Evento (servidor → navegador) | Quando é enviado | O que a outra aba faz |
|---|---|---|
| `quarto_criado` | Depois de gravar um quarto novo | Insere a linha na tabela, na ordem do número |
| `quarto_atualizado` | Depois de gravar uma edição | Troca a linha antiga pela nova (o número pode ter mudado) |
| `quarto_excluido` | Depois de remover um quarto | Remove a linha com uma animação |

- **Tecnologia:** [Socket.IO](https://socket.io/) com `python-socketio` e `eventlet`, as bibliotecas que já vinham no Dockerfile da base. O `socketio.WSGIApp` "embrulha" o app Bottle: o caminho `/socket.io/` vai para o WebSocket e todo o resto continua nas rotas do Bottle. Quem serve é o `eventlet.wsgi`, porque o `run()` do Bottle não mantém conexões abertas.
- **Realtime (controller):** classe própria em `app/controllers/realtime.py`, **composta pelo `Application`** (`self.realtime`), como o `DataRecord` e o `Auth`. Tem um método por acontecimento (`quarto_criado`, `quarto_atualizado`, `quarto_excluido`), que faz o `emit` com o `to_dict()` do quarto. O Model `Quarto` continua sem conhecer Bottle ou Socket.IO.
- **O socket só notifica:** as alterações continuam sendo feitas pelas rotas `POST` protegidas. O `Application` só avisa o `Realtime` **depois** de gravar com sucesso; se a validação falha, nenhum evento é enviado. Não existe evento que grave dados vindo do navegador.
- **Só para quem fez login:** no evento `connect`, o `Realtime` pede ao `Auth` para conferir o cookie de sessão assinado (`usuario_da_requisicao`). Sem sessão válida, a conexão é recusada. Os eventos levam só dados de quartos, nunca de usuários.
- **Cliente:** `socket.io.min.js` (versão 4.8.1, compatível com o `python-socketio` 5) servido como arquivo estático, sem depender de CDN.
- **JS** (`realtime.js`): escuta os eventos e atualiza a tabela no DOM (sempre com `textContent`, nunca HTML vindo do socket), destaca a linha alterada e mostra um aviso no canto da tela. O `gestao.js` foi ajustado para que a busca e a confirmação de exclusão funcionem também nas linhas que chegam em tempo real.
- **CSS** (`realtime.css`): indicador de conexão (*conectado*, *reconectando*, *sem conexão*), destaque da linha que mudou e avisos flutuantes.

**Como testar com duas abas/usuários:**

1. Crie dois usuários com `python criar_usuario.py` (por exemplo, um administrador e uma recepcionista).
2. Rode `python route.py` e abra `http://localhost:8080/login` numa janela normal e numa **janela anônima** (cada uma tem seus próprios cookies, então dá para entrar com usuários diferentes).
3. Entre com um usuário em cada janela e deixe as duas em `/quartos`, lado a lado. O indicador deve mostrar **"Tempo real: conectado"**.
4. Numa janela, cadastre, edite (ex.: mude o status para *Ocupado*) ou exclua um quarto. A outra janela atualiza a tabela sozinha, com a linha destacada e um aviso.

**Vídeo de apresentação (até 15 min):** a publicar

## Funcionalidades

- **Página inicial:** nome, descrição da hospedagem e destaque com quantos quartos estão disponíveis no dia.
- **Quartos:** 8 quartos de exemplo dos tipos Solteiro, Casal, Família e Suíte, com capacidade, diária e status (disponível, ocupado ou em manutenção).
- **Filtros:** por status e por tipo, que podem ser combinados, atualizando a lista sem recarregar a página.
- **Login** (`/login`): acesso dos funcionários, com senha guardada como hash e sessão por cookie assinado.
- **Gerenciar quartos** (`/quartos`, área restrita): cadastrar, editar e excluir quartos, com busca na tabela, confirmação de exclusão e mensagens de erro legíveis (ex.: "Já existe um quarto com o número 101.").
- **Tempo real:** as alterações feitas por um funcionário aparecem na hora para os outros que estão com a gestão aberta, com indicador de conexão.

## Arquitetura (MVC)

| Papel | O que faz | Onde está |
|---|---|---|
| **Rota** | Recebe a requisição e só chama `ctl.render('<página>')`. Não contém lógica | `route.py` |
| **Controller** | O `Application` guarda as páginas em `self.pages` e monta cada uma, buscando os dados no `DataRecord`. Antes, confere com o `Auth` se a página é restrita | `app/controllers/application.py` |
| **Auth** | Login, logout e sessões (cookie assinado + dicionário no servidor) | `app/controllers/auth.py` |
| **Realtime** | Servidor Socket.IO: aceita só conexões de quem fez login e envia os avisos de quartos criados, editados e excluídos | `app/controllers/realtime.py` |
| **ArquivoJSON** | Classe base que lê e grava listas de objetos em JSON | `app/controllers/arquivojson.py` |
| **DataRecord / UsuarioRecord** | Herdam do `ArquivoJSON` e oferecem as operações de quartos e de usuários | `app/controllers/datarecord.py`, `usuariorecord.py` |
| **Model** | Classes com os dados encapsulados e as regras do próprio objeto (validação dos campos, se o quarto está disponível, conferência da senha). Não conhece o Bottle | `app/models/` |
| **View** | Templates que exibem os dados, com CSS e JS servidos pela rota `/static` | `app/views/html/` e `app/static/` |

O fluxo de uma requisição é:

```
Navegador  →  route.py  →  Application  →  Auth  →  UsuarioRecord  →  usuarios.json
                               │   (página restrita sem login? → /login)
                               ↓
                           DataRecord  →  quartos.json
                               ↓          (gravou? Realtime → WebSocket → outras abas)
                  inicio.tpl / login.tpl / quartos.tpl
                  quarto_form.tpl  (+ CSS e JS)
```

Nas ações que alteram dados (POST), o `Application` pede a operação ao `DataRecord`, que salva o JSON, avisa o `Realtime` (que envia o evento às outras abas) e então redireciona o navegador de volta para `/quartos`.

Assim, a rota não tem lógica, o controlador não mexe direto no arquivo de dados e a View só exibe o que recebe.

## Estrutura

```
route.py                Ponto de entrada: app Bottle + Socket.IO, rotas e servidor (eventlet) na porta 8080
requirements.txt        Bibliotecas: bottle, python-socketio, eventlet
app/
├── controllers/
│   ├── application.py  Application: mapeia as páginas, protege as restritas e renderiza
│   ├── auth.py         Auth: login, logout e sessões (cookie assinado)
│   ├── realtime.py     Realtime: WebSocket (Socket.IO) que avisa as outras abas
│   ├── arquivojson.py  ArquivoJSON: classe base que lê e grava JSON
│   ├── datarecord.py   DataRecord: CRUD dos quartos (herda de ArquivoJSON)
│   ├── usuariorecord.py  UsuarioRecord: usuários do sistema (herda de ArquivoJSON)
│   └── db/
│       ├── quartos.json   "Banco" dos quartos
│       └── usuarios.json  "Banco" dos usuários (criado pelo criar_usuario.py, fora do Git)
├── models/
│   ├── quarto.py       Classe Quarto (encapsulamento e validação)
│   └── usuario.py      Classe Usuario (hash da senha privado, verificar_senha)
├── views/html/
│   ├── inicio.tpl      Página inicial da hospedagem
│   ├── login.tpl       Página de login
│   ├── quartos.tpl     Listagem de gerenciamento (Read e Delete), atualizada em tempo real
│   ├── quarto_form.tpl Formulário de cadastro e edição (Create e Update)
│   └── helper.tpl      Página de exemplo da base do professor
└── static/
    ├── css/            inicio.css, gestao.css, login.css, realtime.css (e helper.css, da base)
    ├── js/             inicio.js, gestao.js, login.js, realtime.js, socket.io.min.js
    │                   (cliente Socket.IO) (e helper.js, da base)
    └── img/
criar_usuario.py        Script que cadastra usuários pelo terminal
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
pip install -r requirements.txt   # bottle, python-socketio e eventlet
python criar_usuario.py   # só na primeira vez: cria o administrador
python route.py
```

Depois, abra **http://localhost:8080/** no navegador. O gerenciamento de quartos fica em **http://localhost:8080/quartos** e pede login. A página de exemplo da base continua disponível em `/helper`.

> O terminal mostra `Listening on http://0.0.0.0:8080/`, mas no navegador use **`localhost:8080`**: o endereço `0.0.0.0` não abre no Windows.

### Primeiro usuário (administrador)

Nenhuma senha fica gravada no código. Antes de usar a área restrita, crie o primeiro usuário pelo terminal, na pasta do projeto:

```bash
python criar_usuario.py
```

O script pergunta o login, o nome e a senha (a senha não aparece enquanto é digitada e precisa ter pelo menos 6 caracteres). O primeiro usuário é sempre **Administrador**; rodando o script de novo, dá para criar outros usuários e escolher o perfil. Os usuários ficam em `app/controllers/db/usuarios.json`, que guarda só o **hash** das senhas e está no `.gitignore`.

Enquanto não existir nenhum usuário, a página `/login` mostra um aviso lembrando de rodar o script.

**Chave dos cookies:** fora do ambiente de desenvolvimento, defina a variável de ambiente `HOSPEDAGEM_SEGREDO` com um valor longo e aleatório antes de rodar o `route.py` (para gerar um: `python -c "import secrets; print(secrets.token_hex(32))"`).

### Com Docker

```bash
docker build -t bmvci .
docker run -d -p 8080:8080 -v $(pwd):/bmeta bmvci
```

O container instala o Bottle e as demais bibliotecas do BMVC e executa o `route.py`. Para criar o primeiro usuário dentro do container: `docker exec -it <id_do_container> python criar_usuario.py`. A página fica no mesmo endereço: **http://localhost:8080/**.

### Problemas comuns

| Mensagem ou sintoma | Causa provável | Solução |
|---|---|---|
| `ModuleNotFoundError: No module named 'bottle'` (ou `'socketio'`, `'eventlet'`) | As bibliotecas não estão instaladas | Rodar `pip install -r requirements.txt` |
| Aviso `EventletDeprecationWarning` ao subir o servidor | O eventlet está em modo de manutenção, mas é a biblioteca usada pela base do professor | Pode ignorar: o servidor funciona normalmente |
| Indicador "Tempo real: sem conexão" em `/quartos` | O servidor foi parado ou reiniciado (as sessões são apagadas) | Rodar o `route.py` e entrar de novo em `/login` |
| A outra janela não atualiza sozinha | A página foi aberta antes de o servidor subir, ou a sessão daquela janela acabou | Recarregar a página (F5) e conferir o indicador de conexão |
| "Não é possível acessar esse site" ou erro `-108` (`ERR_ADDRESS_INVALID`) no navegador | Foi aberto o endereço `http://0.0.0.0:8080/` mostrado no terminal, ou o servidor não está rodando | Abrir **http://localhost:8080/** com o `route.py` rodando |
| `Not found: '/...'` (erro 404) | A rota digitada não existe | Usar `/`, `/inicio`, `/login`, `/quartos`, `/quartos/novo` ou `/helper` |
| `/quartos` sempre volta para o login | Não há sessão ativa (reiniciar o servidor também encerra as sessões) | Entrar de novo em `/login` |
| "Usuário ou senha inválidos." | Login ou senha errados, ou nenhum usuário criado | Conferir o Caps Lock; se preciso, criar um usuário com `python criar_usuario.py` |
| `OSError: [WinError 10048]` ou `Address already in use` | Já existe outro programa (ou outro servidor) usando a porta 8080 | Fechar o servidor anterior (Ctrl + C no terminal) e rodar de novo |
| Página sem estilo ou filtros sem funcionar | O CSS ou o JS não foi carregado | Conferir no F12, aba *Rede*, se os arquivos `.css` e `.js` da página retornam status 200 |
| `python` não é reconhecido (Windows) | O Python não está no PATH | Usar `py route.py` ou reinstalar o Python marcando *Add to PATH* |

Para ver o sistema exatamente como estava em um nível, use o commit de entrega indicado na [tabela de níveis](#níveis-do-projeto).

## Autor

[Isaac Ferreira](https://github.com/isaacjf22)
