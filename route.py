import os

from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


# Os caminhos do projeto (app/...) são relativos à pasta do route.py.
# Isso permite rodar o servidor a partir de qualquer pasta.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Suas rotas aqui:

@app.route('/')
@app.route('/inicio')
def inicio():
    return ctl.render('inicio')


#-----------------------------------------------------------------------------


if __name__ == '__main__':

    # O 0.0.0.0 que o Bottle mostra não abre no navegador; use localhost.
    print('Acesse no navegador: http://localhost:8080/')
    run(app, host='0.0.0.0', port=8080, debug=True)
