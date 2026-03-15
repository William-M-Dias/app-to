from flask import Blueprint, render_template

# Criamos o Blueprint sem prefixo de URL, pois ele vai responder na raiz do site ("/")
frontend_bp = Blueprint('frontend_bp', __name__)

@frontend_bp.route('/')
def index():
    # O Flask procura automaticamente dentro da pasta 'templates'
    return render_template('index.html')