import json

from app.models.quarto import Quarto


class DataRecord:
    """Administra o acesso aos dados dos quartos (arquivo JSON)."""

    def __init__(self, arquivo='app/controllers/db/quartos.json'):
        self.arquivo = arquivo
        self.quartos = []
        self.ler()

    def ler(self):
        """Carrega os quartos do arquivo e os transforma em objetos Quarto."""
        with open(self.arquivo, encoding='utf-8') as f:
            dados = json.load(f)
        self.quartos = [Quarto(**item) for item in dados]

    def listar_quartos(self):
        return self.quartos
