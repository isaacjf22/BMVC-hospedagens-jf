import hashlib
import hmac
import re
import secrets


class Usuario:
    """Funcionário que pode entrar na área restrita da hospedagem.

    A senha nunca é guardada: o objeto guarda só um hash PBKDF2 dela e o
    salt usado para gerá-lo. Esses dois atributos são privados (__atributo)
    e ninguém de fora consegue lê-los; para conferir uma senha existe o
    método verificar_senha().
    """

    PERFIS = {
        'admin': 'Administrador',
        'recepcionista': 'Recepcionista',
    }
    TAMANHO_MINIMO_SENHA = 6
    ITERACOES = 200_000  # quantas vezes o PBKDF2 repete o cálculo do hash

    def __init__(self, login, nome, perfil, hash_senha='', salt=''):
        # login, nome e perfil passam pelos setters (validação)
        self.login = login
        self.nome = nome
        self.perfil = perfil
        self.__hash_senha = hash_senha
        self.__salt = salt

    @classmethod
    def novo(cls, login, nome, perfil, senha):
        """Cria um usuário a partir da senha digitada (ex.: no cadastro)."""
        usuario = cls(login, nome, perfil)
        usuario.definir_senha(senha)
        return usuario

    # ----------------------------------------------------------------------
    # Propriedades (encapsulamento + validação)

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, valor):
        valor = str(valor).strip().lower()
        if not re.fullmatch(r'[a-z0-9._]{3,20}', valor):
            raise ValueError('O login deve ter de 3 a 20 caracteres: letras '
                             'sem acento, números, ponto ou sublinhado.')
        self._login = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        valor = str(valor).strip()
        if not valor:
            raise ValueError('O nome do usuário é obrigatório.')
        self._nome = valor

    @property
    def perfil(self):
        return self._perfil

    @perfil.setter
    def perfil(self, valor):
        if valor not in self.PERFIS:
            raise ValueError('Escolha um perfil válido.')
        self._perfil = valor

    @property
    def rotulo_perfil(self):
        """Texto do perfil para exibir na tela (ex.: 'Administrador')."""
        return self.PERFIS[self._perfil]

    # ----------------------------------------------------------------------
    # Senha

    def definir_senha(self, senha):
        """Gera um salt novo e guarda só o hash da senha."""
        if len(senha) < self.TAMANHO_MINIMO_SENHA:
            raise ValueError(f'A senha deve ter pelo menos '
                             f'{self.TAMANHO_MINIMO_SENHA} caracteres.')
        salt = secrets.token_bytes(16)
        self.__salt = salt.hex()
        self.__hash_senha = self._calcular_hash(senha, salt)

    def verificar_senha(self, senha):
        """Diz se a senha digitada é a mesma que gerou o hash guardado."""
        if not self.__hash_senha:
            return False
        tentativa = self._calcular_hash(senha, bytes.fromhex(self.__salt))
        # compare_digest leva o mesmo tempo acertando ou errando, o que
        # impede descobrir o hash medindo o tempo de resposta.
        return hmac.compare_digest(tentativa, self.__hash_senha)

    def _calcular_hash(self, senha, salt):
        hash_bytes = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'),
                                         salt, self.ITERACOES)
        return hash_bytes.hex()

    # ----------------------------------------------------------------------
    # Conversão de/para JSON

    def to_dict(self):
        """Converte o usuário em dicionário (sem a senha, só o hash)."""
        return {
            'login': self._login,
            'nome': self._nome,
            'perfil': self._perfil,
            'hash_senha': self.__hash_senha,
            'salt': self.__salt,
        }

    @classmethod
    def from_dict(cls, dados):
        """Cria um Usuario a partir de um dicionário (vindo do JSON)."""
        return cls(dados['login'], dados['nome'], dados['perfil'],
                   dados['hash_senha'], dados['salt'])

    def __repr__(self):
        return f'Usuario({self._login!r}, {self._perfil!r})'
