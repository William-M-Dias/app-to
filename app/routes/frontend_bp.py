from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend_bp', __name__)

@frontend_bp.route('/')
def index():
    """Rota da página inicial (Home)"""
    return render_template('index.html')

@frontend_bp.route('/paciente/<int:id>')
def perfil_paciente(id):
    """Rota do Prontuário do Paciente"""
    return render_template('paciente.html', paciente_id=id)

@frontend_bp.route('/paciente/<int:id>/pedi')
def pedi_paciente(id):
    """Rota do Formulário PEDI"""
    return render_template('pedi.html', paciente_id=id)

@frontend_bp.route('/paciente/<int:id>/observacao')
def obs_clinica_paciente(id):
    """Rota do Formulário de Observação Clínica (Psicomotora/Sensorial)"""
    return render_template('obs_clinica.html', paciente_id=id)