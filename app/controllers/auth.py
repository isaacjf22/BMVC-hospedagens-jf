import os
import secrets

from bottle import BaseRequest, request, response

from app.controllers.usuariorecord import UsuarioRecord


class Auth:
    """Controle de acesso: login, logout e sessões dos usuários.

    Ao entrar, o usuário recebe um identificador de sessão aleatório.
    O servidor guarda esse identificador num dicionário (id -> login) e o
    navegador o recebe num cookie assinado. Nas próximas requisições, o
    cookie é lido de volta para saber quem está logado.
    """

    COOKIE = 'sessao_hospedagem'
    # Chave que assina o cookie. Em produção, defina a variável de ambiente
    # HOSPEDAGEM_SEGREDO; o valor padrão serve só para desenvolvimento.
    SEGREDO = os.environ.get('HOSPEDAGEM_SEGREDO',
                             'segredo-apenas-para-desenvolvimento')

    def __init__(self):
        self.usuarios = UsuarioRecord()  # composição
        self._sessoes = {}  # id da sessão -> login do usuário

    def entrar(self, login, senha):
        """Confere as credenciais. Se estiverem certas, abre a sessão.

        Devolve True ou False, sem dizer se o erro foi no login ou na senha.
        """
        usuario = self.usuarios.buscar(login)
        if usuario is None or not usuario.verificar_senha(senha):
            return False

        id_sessao = secrets.token_urlsafe(32)
        self._sessoes[id_sessao] = usuario.login
        # httponly: o JavaScript da página não consegue ler o cookie.
        # samesite='lax': outros sites não enviam o cookie em formulários POST.
        response.set_cookie(self.COOKIE, id_sessao, secret=self.SEGREDO,
                            path='/', httponly=True, samesite='lax')
        return True

    def sair(self):
        """Encerra a sessão no servidor e apaga o cookie do navegador."""
        self._sessoes.pop(self._id_da_sessao(), None)
        response.delete_cookie(self.COOKIE, path='/')

    def usuario_logado(self):
        """Devolve o Usuario dono da sessão atual, ou None se ninguém entrou."""
        login = self._sessoes.get(self._id_da_sessao())
        if login is None:
            return None
        return self.usuarios.buscar(login)

    def usuario_da_requisicao(self, environ):
        """Igual a usuario_logado(), mas para uma requisição fora do Bottle.

        Usado pelo WebSocket: na conexão, o Socket.IO entrega só o
        'environ' (dados brutos da requisição, com os cookies).
        """
        login = self._sessoes.get(self._id_da_sessao(BaseRequest(environ)))
        if login is None:
            return None
        return self.usuarios.buscar(login)

    def _id_da_sessao(self, requisicao=request):
        # Se o cookie foi alterado no navegador, a assinatura não confere
        # e o Bottle devolve None.
        return requisicao.get_cookie(self.COOKIE, secret=self.SEGREDO)
