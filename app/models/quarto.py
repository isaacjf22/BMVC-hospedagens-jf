class Quarto:
    """Representa um quarto da hospedagem.

    Os atributos são protegidos (_atributo) e só mudam pelas propriedades,
    que validam o valor antes de guardar. Assim, nunca existe um objeto
    Quarto com dados inválidos.
    """

    TIPOS = ('Solteiro', 'Casal', 'Família', 'Suíte')
    STATUS = {
        'disponivel': 'Disponível',
        'ocupado': 'Ocupado',
        'manutencao': 'Em manutenção',
    }
    CAPACIDADE_MAXIMA = 10

    def __init__(self, numero, tipo, capacidade, diaria, status='disponivel'):
        # Cada atribuição abaixo passa pelo setter da propriedade (validação).
        self.numero = numero
        self.tipo = tipo
        self.capacidade = capacidade
        self.diaria = diaria
        self.status = status

    # ----------------------------------------------------------------------
    # Propriedades (encapsulamento + validação)

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, valor):
        numero = self._para_inteiro(valor, 'Número do quarto')
        if numero <= 0:
            raise ValueError('O número do quarto deve ser maior que zero.')
        self._numero = numero

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        if valor not in self.TIPOS:
            raise ValueError('Escolha um tipo de quarto válido.')
        self._tipo = valor

    @property
    def capacidade(self):
        return self._capacidade

    @capacidade.setter
    def capacidade(self, valor):
        capacidade = self._para_inteiro(valor, 'Capacidade')
        if not 1 <= capacidade <= self.CAPACIDADE_MAXIMA:
            raise ValueError(
                f'A capacidade deve ficar entre 1 e {self.CAPACIDADE_MAXIMA} pessoas.')
        self._capacidade = capacidade

    @property
    def diaria(self):
        return self._diaria

    @diaria.setter
    def diaria(self, valor):
        diaria = self._para_decimal(valor, 'Diária')
        if diaria <= 0:
            raise ValueError('O valor da diária deve ser maior que zero.')
        self._diaria = diaria

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, valor):
        if valor not in self.STATUS:
            raise ValueError('Escolha um status válido.')
        self._status = valor

    @property
    def rotulo_status(self):
        """Texto do status para exibir na tela (ex.: 'Em manutenção')."""
        return self.STATUS[self._status]

    # ----------------------------------------------------------------------
    # Regras do próprio quarto

    def disponivel(self):
        """Indica se o quarto está livre para hospedar alguém."""
        return self._status == 'disponivel'

    # ----------------------------------------------------------------------
    # Conversão de/para JSON

    def to_dict(self):
        """Converte o quarto em dicionário, pronto para salvar em JSON."""
        return {
            'numero': self._numero,
            'tipo': self._tipo,
            'capacidade': self._capacidade,
            'diaria': self._diaria,
            'status': self._status,
        }

    @classmethod
    def from_dict(cls, dados):
        """Cria um Quarto a partir de um dicionário (vindo do JSON)."""
        return cls(dados['numero'], dados['tipo'], dados['capacidade'],
                   dados['diaria'], dados['status'])

    # ----------------------------------------------------------------------
    # Auxiliares de conversão (aceitam texto vindo do formulário)

    @staticmethod
    def _para_inteiro(valor, campo):
        if str(valor).strip() == '':
            raise ValueError(f'O campo "{campo}" é obrigatório.')
        try:
            return int(valor)
        except ValueError:
            raise ValueError(f'O campo "{campo}" deve ser um número inteiro.')

    @staticmethod
    def _para_decimal(valor, campo):
        texto = str(valor).strip().replace(',', '.')  # aceita "120,50"
        if texto == '':
            raise ValueError(f'O campo "{campo}" é obrigatório.')
        try:
            return float(texto)
        except ValueError:
            raise ValueError(f'O campo "{campo}" deve ser um número.')

    def __repr__(self):
        return f'Quarto({self._numero}, {self._tipo!r}, {self._status!r})'
