from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.usuario import Usuario

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Procura o usuário no banco de dados
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_senha(senha):
            # Login com sucesso! Guarda a "chave" na sessão.
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.nome
            return redirect(url_for('frontend_bp.index'))
        else:
            flash('E-mail ou senha incorretos. Tente novamente.', 'erro')

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear() # Destrói a chave de acesso
    return redirect(url_for('auth_bp.login'))