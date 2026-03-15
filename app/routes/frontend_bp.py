from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend_bp', __name__)

@frontend_bp.route('/')
def index():
    # Carrega a tela inicial (lista de pacientes)
    return render_template('index.html')

@frontend_bp.route('/paciente/<int:id>')
def perfil_paciente(id):
    # Carrega a tela do prontuário e passa o ID do paciente para o HTML
    return render_template('paciente.html', paciente_id=id)