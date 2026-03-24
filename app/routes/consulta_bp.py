from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.consulta import Consulta
from datetime import datetime, timedelta
from sqlalchemy import asc, desc

consulta_bp = Blueprint('consulta_bp', __name__, url_prefix='/api/consultas')

# ==========================================
# ROTA ORIGINAL: AGENDA GLOBAL
# ==========================================
@consulta_bp.route('/agenda', methods=['GET'])
def agenda_global():
    from app.models.paciente import Paciente 
    
    # Pega o dia de hoje (Fuso Horário Brasil UTC-3) a partir da meia-noite
    hoje_brasil = datetime.utcnow() - timedelta(hours=3)
    hoje_meia_noite = hoje_brasil.replace(hour=0, minute=0, second=0, microsecond=0)
    
    consultas = Consulta.query.filter(
        Consulta.status == 'Agendado',
        Consulta.data_hora >= hoje_meia_noite
    ).order_by(Consulta.data_hora.asc()).all()
    
    resultado = []
    for c in consultas:
        paciente = Paciente.query.get(c.paciente_id)
        if paciente:
            resultado.append({
                "id": c.id,
                "paciente_id": paciente.id,
                "nome_paciente": paciente.nome,
                "data": c.data_hora.strftime('%d/%m/%Y'),
                "hora": c.data_hora.strftime('%H:%M'),
                "tipo_sessao": c.tipo_sessao
            })
            
    return jsonify(resultado), 200

# ==========================================
# ROTA: AGENDA PAGINADA (Carrossel Horizontal)
# ==========================================
@consulta_bp.route('/agenda_paginada', methods=['GET'])
def agenda_paginada():
    from app.models.paciente import Paciente 
    
    direcao = request.args.get('direcao', 'futuro')
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 6))
    
    # A MÁGICA DO WILLIAM: O momento atual (Brasil) MENOS 60 minutos de tolerância
    # (50 min de sessão + 10 min de intervalo). 
    # Assim, o paciente em atendimento continua visível no carrossel principal.
    agora = datetime.utcnow() - timedelta(hours=3)
    linha_de_corte = agora - timedelta(minutes=60)
    
    if direcao == 'futuro':
        # Do corte para a frente (inclui o paciente que está na sala agora)
        consultas = Consulta.query.filter(
            Consulta.data_hora >= linha_de_corte
        ).order_by(asc(Consulta.data_hora)).offset(offset).limit(limit).all()
    else:
        # Antes do corte (pacientes que já foram embora e terminaram a sessão)
        consultas = Consulta.query.filter(
            Consulta.data_hora < linha_de_corte
        ).order_by(desc(Consulta.data_hora)).offset(offset).limit(limit).all()
        
    resultado = []
    for c in consultas:
        paciente = Paciente.query.get(c.paciente_id)
        if paciente:
            data_obj = c.data_hora
            if isinstance(data_obj, str):
                try:
                    data_obj = datetime.strptime(data_obj, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    data_obj = datetime.strptime(data_obj, '%Y-%m-%d %H:%M')
                    
            resultado.append({
                "id": c.id,
                "paciente_id": paciente.id,
                "nome_paciente": paciente.nome,
                "data": data_obj.strftime('%d/%m/%Y'),
                "hora": data_obj.strftime('%H:%M'),
                "tipo_sessao": c.tipo_sessao,
                "status": c.status
            })
            
    return jsonify(resultado), 200

@consulta_bp.route('/paciente/<int:paciente_id>', methods=['GET'])
def listar_consultas_paciente(paciente_id):
    consultas = Consulta.query.filter_by(paciente_id=paciente_id).order_by(Consulta.data_hora.desc()).all()
    resultado = [{
        "id": c.id,
        "data_hora": c.data_hora.strftime('%d/%m/%Y %H:%M'),
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
        return jsonify({"erro": "Dados incompletos para registo."}), 400
        
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
        return jsonify({"mensagem": "Registo salvo com sucesso!"}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

@consulta_bp.route('/<int:id>', methods=['DELETE'])
def deletar_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    try:
        db.session.delete(consulta)
        db.session.commit()
        return jsonify({"mensagem": "Registro excluído com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500