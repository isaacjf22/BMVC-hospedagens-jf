import socketio


class Realtime:
    """Avisos em tempo real (WebSocket) para quem está na área de gestão.

    O socket só NOTIFICA: as alterações continuam sendo feitas pelas rotas
    HTTP POST, que já são protegidas pelo login. Depois de gravar com
    sucesso, o Application chama um dos métodos quarto_* desta classe, e ela
    envia (emit) o evento para todos os navegadores conectados.
    """

    SALA = 'gestao'  # grupo de conexões que recebe os avisos

    def __init__(self, auth):
        self._auth = auth  # usado para conferir o login na conexão
        self.sio = socketio.Server(async_mode='eventlet')
        self.sio.on('connect', self._conectar)

    # ----------------------------------------------------------------------
    # Conexão

    def _conectar(self, sid, environ, dados_cliente=None):
        """Só aceita a conexão de quem fez login (cookie de sessão válido)."""
        usuario = self._auth.usuario_da_requisicao(environ)
        if usuario is None:
            raise socketio.exceptions.ConnectionRefusedError('Login necessário.')
        self.sio.enter_room(sid, self.SALA)

    # ----------------------------------------------------------------------
    # Avisos enviados depois de cada alteração no CRUD

    def quarto_criado(self, quarto):
        self.sio.emit('quarto_criado', self._dados(quarto), to=self.SALA)

    def quarto_atualizado(self, numero_original, quarto):
        # numero_original: o número pode ter mudado na edição, e o navegador
        # precisa saber qual linha da tabela substituir.
        dados = {'numero_original': numero_original,
                 'quarto': self._dados(quarto)}
        self.sio.emit('quarto_atualizado', dados, to=self.SALA)

    def quarto_excluido(self, numero):
        self.sio.emit('quarto_excluido', {'numero': numero}, to=self.SALA)

    # ----------------------------------------------------------------------

    @staticmethod
    def _dados(quarto):
        """Só os dados do quarto (to_dict) mais o texto do status."""
        dados = quarto.to_dict()
        dados['rotulo_status'] = quarto.rotulo_status
        return dados
