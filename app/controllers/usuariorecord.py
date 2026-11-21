from app.controllers.arquivojson import ArquivoJSON
from app.models.usuario import Usuario


class UsuarioRecord(ArquivoJSON):
    """Administra os usuários guardados no arquivo usuarios.json.

    Assim como o DataRecord, herda a leitura e a gravação do ArquivoJSON.
    """

    MODELO = Usuario

    def __init__(self, arquivo='app/controllers/db/usuarios.json'):
        super().__init__(arquivo)

    def buscar(self, login):
        """Devolve o usuário com esse login, ou None se não existir."""
        login = str(login).strip().lower()
        for usuario in self._registros:
            if usuario.login == login:
                return usuario
        return None

    def adicionar(self, usuario):
        """Cadastra um usuário novo, sem repetir o login."""
        if self.buscar(usuario.login):
            raise ValueError(f'Já existe um usuário com o login {usuario.login}.')
        self._registros.append(usuario)
        self.salvar()

    def existe_algum(self):
        """Indica se já existe pelo menos um usuário cadastrado."""
        return len(self._registros) > 0
