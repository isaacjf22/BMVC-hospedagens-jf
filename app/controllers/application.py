from bottle import template

from app.controllers.datarecord import DataRecord


class Application():

    def __init__(self):
        self.pages = {
            'helper': self.helper,
            'inicio': self.inicio,
        }
        self.models = DataRecord()


    def render(self,page):
       content = self.pages.get(page, self.helper)
       return content()


    def helper(self):
        return template('app/views/html/helper')


    def inicio(self):
        """Página inicial da hospedagem com a lista de quartos."""
        quartos = self.models.listar_quartos()
        livres = len([q for q in quartos if q.disponivel()])
        return template('app/views/html/inicio', quartos=quartos,
                        livres=livres)
