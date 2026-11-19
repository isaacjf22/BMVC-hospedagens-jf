class Quarto:
    """Representa um quarto da hospedagem."""

    def __init__(self, numero, tipo, capacidade, diaria, status):
        self.numero = numero
        self.tipo = tipo
        self.capacidade = capacidade
        self.diaria = diaria
        self.status = status

    def disponivel(self):
        """Indica se o quarto está livre para hospedar alguém."""
        return self.status == 'disponivel'
