import json
import os


class ArquivoJSON:
    """Classe base para os administradores de dados guardados em JSON.

    Sabe ler e gravar uma lista de objetos em um arquivo. Cada subclasse
    só informa qual modelo guarda (atributo MODELO): a conversão é feita
    pelos métodos to_dict() e from_dict() do próprio modelo (polimorfismo).
    """

    MODELO = None  # definido em cada subclasse (ex.: Quarto, Usuario)

    def __init__(self, arquivo):
        self._arquivo = arquivo
        self._registros = []
        self.ler()

    def ler(self):
        """Carrega o arquivo e transforma cada item em um objeto do modelo."""
        if not os.path.exists(self._arquivo):
            self._registros = []
            return
        with open(self._arquivo, encoding='utf-8') as f:
            dados = json.load(f)
        self._registros = [self.MODELO.from_dict(item) for item in dados]

    def salvar(self):
        """Grava todos os objetos no arquivo, para não perder ao reiniciar."""
        dados = [objeto.to_dict() for objeto in self._registros]
        with open(self._arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
