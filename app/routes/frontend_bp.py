from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend_bp', __name__)

@frontend_bp.route('/')
def index():
    return render_template('index.html')

@frontend_bp.route('/paciente/<int:id>')
def perfil_paciente(id):
    return render_template('paciente.html', paciente_id=id)

@frontend_bp.route('/paciente/<int:id>/anamnese')
def anamnese_paciente(id):
    return render_template('anamnese.html', paciente_id=id)

@frontend_bp.route('/paciente/<int:id>/pedi')
def pedi_paciente(id):
    return render_template('pedi.html', paciente_id=id)

@frontend_bp.route('/paciente/<int:id>/observacao')
def obs_clinica_paciente(id):
    return render_template('obs_clinica.html', paciente_id=id)

@frontend_bp.route('/paciente/<int:id>/evolucao')
def evolucao_paciente(id):
    return render_template('evolucao.html', paciente_id=id)

@frontend_bp.route('/paciente/<int:id>/relatorio')
def relatorio_paciente(id):
    return render_template('relatorio.html', paciente_id=id)

@frontend_bp.route('/agenda')
def abrir_agenda_visual():
    return render_template('agenda.html')

# <--- ROTA NOVA: DASHBOARD DE ESTATÍSTICAS (FASE 5) --->
@frontend_bp.route('/estatisticas')
def dashboard_estatisticas():
    return render_template('estatisticas.html')