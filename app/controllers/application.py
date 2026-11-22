from bottle import template, request, redirect

from app.controllers.auth import Auth
from app.controllers.datarecord import DataRecord
from app.controllers.realtime import Realtime
from app.models.quarto import Quarto


class Application():

    # Mensagens mostradas na listagem depois de cada operação (?msg=...)
    MENSAGENS = {
        'criado': 'Quarto cadastrado com sucesso.',
        'atualizado': 'Quarto atualizado com sucesso.',
        'excluido': 'Quarto excluído com sucesso.',
        'nao_encontrado': 'Quarto não encontrado.',
    }

    # Avisos mostrados na página de login (?aviso=...)
    AVISOS_LOGIN = {
        'restrito': 'Faça login para acessar a área de gestão.',
        'saiu': 'Você saiu do sistema.',
    }

    # Páginas da área restrita: só abrem para quem fez login.
    # Inclui as ações POST (criar, atualizar, excluir), não só os formulários.
    RESTRITAS = {
        'quartos', 'quarto_novo', 'quarto_criar', 'quarto_editar',
        'quarto_atualizar', 'quarto_excluir',
    }

    def __init__(self):
        self.pages = {
            'helper': self.helper,
            'inicio': self.inicio,
            'quartos': self.quartos,
            'quarto_novo': self.quarto_novo,
            'quarto_criar': self.quarto_criar,
            'quarto_editar': self.quarto_editar,
            'quarto_atualizar': self.quarto_atualizar,
            'quarto_excluir': self.quarto_excluir,
            'login': self.login,
            'login_entrar': self.login_entrar,
            'logout': self.logout,
        }
        self.models = DataRecord()
        self.auth = Auth()  # composição: o Application tem um Auth
        self.realtime = Realtime(self.auth)  # e um Realtime (WebSocket)


    def render(self, page, parametro=None):
        # Controle de acesso num só lugar: toda rota passa por aqui.
        if page in self.RESTRITAS and self.auth.usuario_logado() is None:
            redirect('/login?aviso=restrito')
        content = self.pages.get(page, self.helper)
        if parametro is None:
            return content()
        return content(parametro)


    def helper(self):
        return template('app/views/html/helper')


    def inicio(self):
        """Página inicial da hospedagem com a lista de quartos."""
        quartos = self.models.listar_quartos()
        livres = len([q for q in quartos if q.disponivel()])
        return template('app/views/html/inicio', quartos=quartos,
                        livres=livres, usuario=self.auth.usuario_logado())

    # ----------------------------------------------------------------------
    # Login e logout

    def login(self, erro=None, login_digitado=''):
        """Formulário de login (se já estiver logado, vai direto à gestão)."""
        if self.auth.usuario_logado():
            redirect('/quartos')
        return template('app/views/html/login', erro=erro,
                        login_digitado=login_digitado,
                        aviso=self.AVISOS_LOGIN.get(request.query.get('aviso')),
                        sem_usuarios=not self.auth.usuarios.existe_algum())


    def login_entrar(self):
        """Confere login e senha; se estiverem certos, abre a área restrita."""
        login = request.forms.getunicode('login', default='').strip()
        senha = request.forms.getunicode('senha', default='')
        if self.auth.entrar(login, senha):
            redirect('/quartos')
        # Mensagem genérica: não revela se o erro foi no login ou na senha.
        return self.login(erro='Usuário ou senha inválidos.',
                          login_digitado=login)


    def logout(self):
        """Encerra a sessão e volta para a página de login."""
        self.auth.sair()
        redirect('/login?aviso=saiu')

    # ----------------------------------------------------------------------
    # CRUD de quartos

    def quartos(self):
        """Read: listagem de gerenciamento dos quartos."""
        codigo = request.query.get('msg')
        return template('app/views/html/quartos',
                        quartos=self.models.listar_quartos(),
                        mensagem=self.MENSAGENS.get(codigo),
                        usuario=self.auth.usuario_logado())


    def quarto_novo(self):
        """Create (GET): formulário de cadastro vazio."""
        return self._formulario(dados={'status': 'disponivel'})


    def quarto_criar(self):
        """Create (POST): valida, salva e volta para a listagem."""
        dados = self._dados_do_formulario()
        try:
            quarto = Quarto(**dados)
            self.models.adicionar_quarto(quarto)
        except ValueError as erro:
            return self._formulario(dados=dados, erro=str(erro))
        self.realtime.quarto_criado(quarto)  # avisa as outras abas
        redirect('/quartos?msg=criado')


    def quarto_editar(self, numero):
        """Update (GET): formulário preenchido com os dados atuais."""
        quarto = self.models.buscar_quarto(numero)
        if quarto is None:
            redirect('/quartos?msg=nao_encontrado')
        return self._formulario(dados=quarto.to_dict(), numero_original=numero)


    def quarto_atualizar(self, numero):
        """Update (POST): valida, salva e volta para a listagem."""
        dados = self._dados_do_formulario()
        try:
            quarto = Quarto(**dados)
            self.models.atualizar_quarto(numero, quarto)
        except ValueError as erro:
            return self._formulario(dados=dados, erro=str(erro),                                    numero_original=numero)
        self.realtime.quarto_atualizado(numero, quarto)
        redirect('/quartos?msg=atualizado')


    def quarto_excluir(self, numero):
        """Delete (POST): remove o quarto e volta para a listagem."""
        try:
            self.models.remover_quarto(numero)
        except ValueError:
            redirect('/quartos?msg=nao_encontrado')
        self.realtime.quarto_excluido(numero)
        redirect('/quartos?msg=excluido')

    # ----------------------------------------------------------------------
    # Auxiliares

    def _dados_do_formulario(self):
        """Lê os campos enviados pelo formulário (como texto)."""
        campos = ('numero', 'tipo', 'capacidade', 'diaria', 'status')
        return {campo: request.forms.getunicode(campo, default='').strip()
                for campo in campos}


    def _formulario(self, dados, erro=None, numero_original=None):
        """Monta a página de formulário, usada no cadastro e na edição."""
        return template('app/views/html/quarto_form', dados=dados, erro=erro,
                        numero_original=numero_original,
                        tipos=Quarto.TIPOS, status=Quarto.STATUS,
                        usuario=self.auth.usuario_logado())
