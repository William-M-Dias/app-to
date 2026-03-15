from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend_bp', __name__)

@frontend_bp.route('/')
def index():
    return render_template('index.html')

@frontend_bp.route('/paciente/<int:id>')
def perfil_paciente(id):
    return render_template('paciente.html', paciente_id=id)

# <--- NOVA ROTA: TELA DO PEDI --->
@frontend_bp.route('/paciente/<int:id>/pedi')
def pedi_paciente(id):
    return render_template('pedi.html', paciente_id=id)