from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.consulta import Consulta
from datetime import datetime

consulta_bp = Blueprint('consulta_bp', __name__, url_prefix='/api/consultas')

@consulta_bp.route('/paciente/<int:paciente_id>', methods=['GET'])
def listar_consultas_paciente(paciente_id):
    consultas = Consulta.query.filter_by(paciente_id=paciente_id).order_by(Consulta.data_hora.desc()).all()
    resultado = [{
        "id": c.id,
        "data_hora": c.data_hora.strftime('%d/%m/%Y'),
        "tipo_sessao": c.tipo_sessao,
        "status": c.status,
        "evolucao_texto": c.evolucao_texto,
        "micro_metas": c.micro_metas or {}
    } for c in consultas]
    return jsonify(resultado), 200

@consulta_bp.route('/', methods=['POST'])
def registrar_evolucao():
    dados = request.get_json()
    
    if not dados or not dados.get('paciente_id') or not dados.get('data_hora'):
        return jsonify({"erro": "Dados incompletos para registo da evolução."}), 400
        
    try:
        data_string = dados['data_hora']
        if 'T' in data_string:
            data_string = data_string.replace('T', ' ')
        if len(data_string) == 10:
            data_string += ' 00:00'
            
        data_hora_consulta = datetime.strptime(data_string, '%Y-%m-%d %H:%M')
        
        nova_consulta = Consulta(
            paciente_id=dados['paciente_id'],
            data_hora=data_hora_consulta,
            tipo_sessao=dados.get('tipo_sessao', 'Intervenção de Rotina'),
            status=dados.get('status', 'Realizado'),
            evolucao_texto=dados.get('evolucao_texto', ''),
            micro_metas=dados.get('micro_metas', {})
        )
        
        db.session.add(nova_consulta)
        db.session.commit()
        return jsonify({"mensagem": "Evolução Diária registada com sucesso!"}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

# ==========================================
# NOVA ROTA FASE 2: EXCLUIR EVOLUÇÃO
# ==========================================

@consulta_bp.route('/<int:id>', methods=['DELETE'])
def deletar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    try:
        db.session.delete(consulta)
        db.session.commit()
        return jsonify({"mensagem": "Evolução excluída com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500