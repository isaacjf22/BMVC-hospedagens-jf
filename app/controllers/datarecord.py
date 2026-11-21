from app.controllers.arquivojson import ArquivoJSON
from app.models.quarto import Quarto


class DataRecord(ArquivoJSON):
    """Administra os quartos guardados no arquivo JSON.

    É o único lugar do sistema que lê e grava o arquivo de quartos.
    A leitura e a gravação vêm da classe base ArquivoJSON (herança);
    aqui ficam só as operações do CRUD de quartos.
    """

    MODELO = Quarto

    def __init__(self, arquivo='app/controllers/db/quartos.json'):
        super().__init__(arquivo)

    # ----------------------------------------------------------------------
    # CRUD

    def listar_quartos(self):
        """Read: devolve os quartos ordenados pelo número."""
        return sorted(self._registros, key=lambda quarto: quarto.numero)

    def buscar_quarto(self, numero):
        """Read: devolve o quarto com esse número, ou None se não existir."""
        for quarto in self._registros:
            if quarto.numero == numero:
                return quarto
        return None

    def adicionar_quarto(self, quarto):
        """Create: inclui um quarto novo, sem repetir o número."""
        if self.buscar_quarto(quarto.numero):
            raise ValueError(f'Já existe um quarto com o número {quarto.numero}.')
        self._registros.append(quarto)
        self.salvar()

    def atualizar_quarto(self, numero_original, quarto_editado):
        """Update: troca os dados do quarto que tinha o número original."""
        mudou_numero = quarto_editado.numero != numero_original
        if mudou_numero and self.buscar_quarto(quarto_editado.numero):
            raise ValueError(
                f'Já existe um quarto com o número {quarto_editado.numero}.')

        for posicao, quarto in enumerate(self._registros):
            if quarto.numero == numero_original:
                self._registros[posicao] = quarto_editado
                self.salvar()
                return
        raise ValueError(f'O quarto {numero_original} não foi encontrado.')

    def remover_quarto(self, numero):
        """Delete: apaga o quarto com esse número."""
        quarto = self.buscar_quarto(numero)
        if quarto is None:
            raise ValueError(f'O quarto {numero} não foi encontrado.')
        self._registros.remove(quarto)
        self.salvar()
