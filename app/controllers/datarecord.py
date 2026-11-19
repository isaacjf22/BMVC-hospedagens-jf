import json
import os

from app.models.quarto import Quarto


class DataRecord:
    """Administra os quartos guardados no arquivo JSON.

    É o único lugar do sistema que lê e grava o arquivo de dados.
    O Application usa os métodos daqui e nunca mexe no arquivo diretamente.
    """

    def __init__(self, arquivo='app/controllers/db/quartos.json'):
        self._arquivo = arquivo
        self._quartos = []
        self.ler()

    # ----------------------------------------------------------------------
    # Leitura e gravação do arquivo

    def ler(self):
        """Carrega os quartos do arquivo e os transforma em objetos Quarto."""
        if not os.path.exists(self._arquivo):
            self._quartos = []
            return
        with open(self._arquivo, encoding='utf-8') as f:
            dados = json.load(f)
        self._quartos = [Quarto.from_dict(item) for item in dados]

    def salvar(self):
        """Grava todos os quartos no arquivo, para não perder ao reiniciar."""
        dados = [quarto.to_dict() for quarto in self._quartos]
        with open(self._arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    # ----------------------------------------------------------------------
    # CRUD

    def listar_quartos(self):
        """Read: devolve os quartos ordenados pelo número."""
        return sorted(self._quartos, key=lambda quarto: quarto.numero)

    def buscar_quarto(self, numero):
        """Read: devolve o quarto com esse número, ou None se não existir."""
        for quarto in self._quartos:
            if quarto.numero == numero:
                return quarto
        return None

    def adicionar_quarto(self, quarto):
        """Create: inclui um quarto novo, sem repetir o número."""
        if self.buscar_quarto(quarto.numero):
            raise ValueError(f'Já existe um quarto com o número {quarto.numero}.')
        self._quartos.append(quarto)
        self.salvar()

    def atualizar_quarto(self, numero_original, quarto_editado):
        """Update: troca os dados do quarto que tinha o número original."""
        mudou_numero = quarto_editado.numero != numero_original
        if mudou_numero and self.buscar_quarto(quarto_editado.numero):
            raise ValueError(
                f'Já existe um quarto com o número {quarto_editado.numero}.')

        for posicao, quarto in enumerate(self._quartos):
            if quarto.numero == numero_original:
                self._quartos[posicao] = quarto_editado
                self.salvar()
                return
        raise ValueError(f'O quarto {numero_original} não foi encontrado.')

    def remover_quarto(self, numero):
        """Delete: apaga o quarto com esse número."""
        quarto = self.buscar_quarto(numero)
        if quarto is None:
            raise ValueError(f'O quarto {numero} não foi encontrado.')
        self._quartos.remove(quarto)
        self.salvar()
