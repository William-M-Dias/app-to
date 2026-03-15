from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.consulta import Consulta
from datetime import datetime

# Criação do Blueprint
consulta_bp = Blueprint('consulta_bp', __name__, url_prefix='/api/consultas')

@consulta_bp.route('/', methods=['GET'])
def listar_consultas():
    # Ordena as consultas cronologicamente e limita a 50 para poupar memória no Tier Gratuito
    consultas = Consulta.query.order_by(Consulta.data_hora.asc()).limit(50).all()
    resultado = [{
        "id": c.id,
        "paciente_id": c.paciente_id,
        "data_hora": c.data_hora.strftime('%Y-%m-%d %H:%M'),
        "tipo_sessao": c.tipo_sessao,
        "status": c.status
    } for c in consultas]
    return jsonify(resultado), 200

@consulta_bp.route('/', methods=['POST'])
def agendar_consulta():
    dados = request.get_json()
    
    if not dados or not dados.get('paciente_id') or not dados.get('data_hora') or not dados.get('tipo_sessao'):
        return jsonify({"erro": "Dados incompletos para agendamento."}), 400
        
    try:
        data_hora_consulta = datetime.strptime(dados['data_hora'], '%Y-%m-%d %H:%M')
        
        nova_consulta = Consulta(
            paciente_id=dados['paciente_id'],
            data_hora=data_hora_consulta,
            tipo_sessao=dados['tipo_sessao'],
            recorrente=dados.get('recorrente', False),
            dados_sensoriais_executivos=dados.get('dados_sensoriais', {}) # Acomoda todo o checklist Tátil/Vestibular/etc
        )
        
        db.session.add(nova_consulta)
        db.session.commit()
        return jsonify({"mensagem": "Consulta agendada com sucesso!", "id": nova_consulta.id}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500