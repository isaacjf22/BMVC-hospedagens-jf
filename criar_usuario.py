"""Cadastra um usuário da área restrita pelo terminal.

A senha é digitada na hora (sem aparecer na tela) e só o hash dela é
salvo em app/controllers/db/usuarios.json. Assim nenhuma senha fica
escrita no código do repositório.

Uso: python criar_usuario.py
"""
import getpass
import os

# Mesma ideia do route.py: os caminhos app/... partem da pasta do projeto.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app.controllers.usuariorecord import UsuarioRecord  # noqa: E402
from app.models.usuario import Usuario  # noqa: E402


def perguntar_perfil(primeiro_usuario):
    """O primeiro usuário é sempre administrador; os demais escolhem."""
    if primeiro_usuario:
        print('Primeiro usuário do sistema: perfil Administrador.')
        return 'admin'
    opcoes = list(Usuario.PERFIS)
    for numero, chave in enumerate(opcoes, start=1):
        print(f'  {numero}. {Usuario.PERFIS[chave]}')
    escolha = input('Perfil (número): ').strip()
    if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
        return opcoes[int(escolha) - 1]
    raise ValueError('Escolha um perfil válido.')


def main():
    usuarios = UsuarioRecord()
    print('=== Novo usuário da Hospedagem JF ===')
    try:
        login = input('Login: ')
        nome = input('Nome para exibir: ')
        perfil = perguntar_perfil(not usuarios.existe_algum())
        senha = getpass.getpass('Senha (não aparece ao digitar): ')
        if senha != getpass.getpass('Repita a senha: '):
            raise ValueError('As senhas não conferem.')
        usuario = Usuario.novo(login, nome, perfil, senha)
        usuarios.adicionar(usuario)
    except ValueError as erro:
        print('Erro:', erro)
        return
    print(f'Usuário "{usuario.login}" criado. Já dá para entrar em '
          'http://localhost:8080/login')


if __name__ == '__main__':
    main()
