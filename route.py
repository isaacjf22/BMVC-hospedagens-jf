# O eventlet precisa ajustar a biblioteca padrão (rede, threads) antes de
# qualquer outro import, para atender várias conexões WebSocket ao mesmo tempo.
import eventlet
eventlet.monkey_patch()

import os

import socketio
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


# Login e logout (páginas públicas).

@app.route('/login', method='GET')
def login():
    return ctl.render('login')

@app.route('/login', method='POST')
def login_entrar():
    return ctl.render('login_entrar')

@app.route('/logout')
def logout():
    return ctl.render('logout')


# CRUD de quartos: GET mostra páginas, POST altera dados (e redireciona).
# Área restrita: o Application só deixa passar quem fez login.

@app.route('/quartos')
def quartos():
    return ctl.render('quartos')

@app.route('/quartos/novo', method='GET')
def quarto_novo():
    return ctl.render('quarto_novo')

@app.route('/quartos/novo', method='POST')
def quarto_criar():
    return ctl.render('quarto_criar')

@app.route('/quartos/<numero:int>/editar', method='GET')
def quarto_editar(numero):
    return ctl.render('quarto_editar', numero)

@app.route('/quartos/<numero:int>/editar', method='POST')
def quarto_atualizar(numero):
    return ctl.render('quarto_atualizar', numero)

@app.route('/quartos/<numero:int>/excluir', method='POST')
def quarto_excluir(numero):
    return ctl.render('quarto_excluir', numero)


#-----------------------------------------------------------------------------


# Nível IV: o Socket.IO "embrulha" o app Bottle. Requisições /socket.io/
# vão para o WebSocket (classe Realtime); todas as outras, para o Bottle.
servidor = socketio.WSGIApp(ctl.realtime.sio, app)


if __name__ == '__main__':

    # O run() do Bottle não atende WebSocket, então quem serve é o eventlet.
    # Sem reloader: o recarregamento automático do Bottle conflita com ele.
    print('Acesse no navegador: http://localhost:8080/')
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 8080)), servidor)
