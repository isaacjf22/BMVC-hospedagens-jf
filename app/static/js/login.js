// Interações da página de login.
// O servidor confere login e senha de verdade: o JS só ajuda a digitar.

// 1. Botão que mostra ou esconde a senha digitada
function prepararMostrarSenha() {
    const campo = document.getElementById('campo-senha');
    const botao = document.getElementById('mostrar-senha');

    botao.addEventListener('click', function () {
        const escondida = campo.type === 'password';
        campo.type = escondida ? 'text' : 'password';
        botao.textContent = escondida ? 'Ocultar' : 'Mostrar';
        botao.setAttribute('aria-label', escondida ? 'Ocultar senha' : 'Mostrar senha');
        campo.focus();
    });
}

// 2. Aviso quando o Caps Lock está ligado (erro comum ao digitar senha)
function prepararAvisoCapsLock() {
    const campo = document.getElementById('campo-senha');
    const aviso = document.getElementById('aviso-caps');

    campo.addEventListener('keyup', function (evento) {
        aviso.hidden = !evento.getModifierState('CapsLock');
    });
}

// 3. Não deixa enviar o formulário com campos vazios
function prepararValidacao() {
    const form = document.getElementById('form-login');
    const caixaErro = document.getElementById('erro-js');

    form.addEventListener('submit', function (evento) {
        const vazios = [];
        ['login', 'senha'].forEach(function (nome) {
            const campo = form.elements[nome];
            const vazio = campo.value.trim() === '';
            campo.classList.toggle('invalido', vazio);
            if (vazio) vazios.push(nome);
        });

        if (vazios.length > 0) {
            evento.preventDefault();
            caixaErro.textContent = 'Preencha o login e a senha para entrar.';
            caixaErro.hidden = false;
            form.elements[vazios[0]].focus();
        }
    });
}

prepararMostrarSenha();
prepararAvisoCapsLock();
prepararValidacao();
