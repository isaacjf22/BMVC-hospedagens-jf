# Hospedagem JF

Sistema web de controle de hospedagem, desenvolvido em **Python** com o framework **Bottle** para a disciplina **Orientação a Objetos** do **Prof. Henrique Moura** (UnB), na trilha **BMVC** (Bottle + MVC).

O projeto parte da base [bmvc_start_from_this](https://github.com/hgmachine/bmvc_start_from_this), fornecida pelo professor, e evolui em quatro níveis, liberados aos poucos. Cada nível entregue é marcado por um commit próprio, e o histórico do repositório mostra o sistema crescendo de um nível para o outro.

## Finalidade

Apresentar e gerenciar os quartos de uma hospedagem pela web: quais quartos existem, de que tipo são, quantas pessoas cabem em cada um, quanto custa a diária e se estão disponíveis, ocupados ou em manutenção.

O projeto segue a arquitetura **MVC** no formato do BMVC: as rotas ficam no `route.py`, o controlador `Application` decide qual página montar, o `DataRecord` cuida do acesso aos dados e as páginas são templates `.tpl` do Bottle, com CSS e JavaScript próprios.

## Níveis do projeto

| Nível | Propósito | Interface | Vídeo | Commit de entrega | Status |
|:---:|---|---|---|---|:---:|
| **1** | Servir uma página própria, com propósito claro, carregando CSS e JS funcionais | Web (`/`) | Em breve | `nivel 1 concluído` | Em andamento |
| **2** | A liberar | — | — | — | Bloqueado |
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

**Vídeo de apresentação (até 3 min):** em breve

## Funcionalidades

- **Página inicial:** nome, descrição da hospedagem e destaque com quantos quartos estão disponíveis no dia.
- **Quartos:** 8 quartos de exemplo dos tipos Solteiro, Casal, Família e Suíte, com capacidade, diária e status (disponível, ocupado ou em manutenção).
- **Filtros:** por status e por tipo, que podem ser combinados, atualizando a lista sem recarregar a página.

## Arquitetura (MVC)

| Papel | O que faz | Onde está |
|---|---|---|
| **Rota** | Recebe a requisição e só chama `ctl.render('<página>')`. Não contém lógica | `route.py` |
| **Controller** | O `Application` guarda as páginas em `self.pages` e monta cada uma, buscando os dados no `DataRecord` | `app/controllers/application.py` |
| **DataRecord** | Único lugar que lê o arquivo de dados e o converte em objetos do Model | `app/controllers/datarecord.py` |
| **Model** | Classes simples com os dados e as regras do próprio objeto (por exemplo, se o quarto está disponível). Não conhece o Bottle | `app/models/` |
| **View** | Templates que exibem os dados, com CSS e JS servidos pela rota `/static` | `app/views/html/` e `app/static/` |

O fluxo de uma requisição é:

```
Navegador  →  route.py  →  Application  →  DataRecord  →  quartos.json
                               ↓                ↓
                          inicio.tpl     objetos Quarto
                       (+ CSS e JS)
```

Assim, a rota não tem lógica, o controlador não mexe direto no arquivo de dados e a View só exibe o que recebe.

## Estrutura

```
route.py                Ponto de entrada: app Bottle, rotas e servidor na porta 8080
app/
├── controllers/
│   ├── application.py  Application: mapeia as páginas e renderiza os templates
│   ├── datarecord.py   DataRecord: lê os quartos do banco em JSON
│   └── db/
│       └── quartos.json  Dados de exemplo dos quartos
├── models/
│   └── quarto.py       Classe Quarto
├── views/html/
│   ├── inicio.tpl      Página inicial da hospedagem
│   └── helper.tpl      Página de exemplo da base do professor
└── static/
    ├── css/            inicio.css (e helper.css, da base)
    ├── js/             inicio.js (e helper.js, da base)
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

Depois, abra **http://localhost:8080/** no navegador. A página de exemplo da base continua disponível em `/helper`.

> O `route.py` precisa ser executado **na raiz do projeto**: os caminhos dos templates, do CSS/JS e do `quartos.json` são relativos a essa pasta.

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
| `FileNotFoundError: ... quartos.json` | O `route.py` foi executado fora da raiz do projeto | Entrar na pasta `BMVC-hospedagens-jf` e rodar `python route.py` |
| `OSError: [WinError 10048]` ou `Address already in use` | Já existe outro programa (ou outro servidor) usando a porta 8080 | Fechar o servidor anterior (Ctrl + C no terminal) e rodar de novo |
| Página sem estilo ou filtros sem funcionar | O CSS ou o JS não foi carregado | Conferir no F12, aba *Rede*, se `inicio.css` e `inicio.js` retornam status 200 |
| `python` não é reconhecido (Windows) | O Python não está no PATH | Usar `py route.py` ou reinstalar o Python marcando *Add to PATH* |

Para ver o sistema exatamente como estava em um nível, use o commit de entrega indicado na [tabela de níveis](#níveis-do-projeto).

## Autor

[Isaac Ferreira](https://github.com/isaacjf22)
