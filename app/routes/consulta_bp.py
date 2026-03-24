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
    
    agora = datetime.utcnow() - timedelta(hours=3)
    linha_de_corte = agora - timedelta(minutes=60)
    
    if direcao == 'futuro':
        consultas = Consulta.query.filter(
            Consulta.data_hora >= linha_de_corte
        ).order_by(asc(Consulta.data_hora)).offset(offset).limit(limit).all()
    else:
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

# ==========================================
# ROTA INTELIGENTE DE REGISTRO / EVOLUÇÃO
# ==========================================
@consulta_bp.route('/', methods=['POST'])
def registrar_evolucao():
    dados = request.get_json()
    
    if not dados or not dados.get('paciente_id'):
        return jsonify({"erro": "Dados incompletos para registo."}), 400
        
    try:
        paciente_id = dados['paciente_id']
        status_recebido = dados.get('status', 'Realizado')
        
        # Formatação segura da data
        data_string = dados.get('data_hora')
        if not data_string:
            data_string = (datetime.utcnow() - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')
            
        if 'T' in data_string:
            data_string = data_string.replace('T', ' ')
        if len(data_string) == 10:
            data_string += ' 00:00'
            
        data_hora_requisicao = datetime.strptime(data_string, '%Y-%m-%d %H:%M')
        data_apenas = data_hora_requisicao.date()
        
        consulta_existente = None
        
        # A MÁGICA: Se ela estiver dando BAIXA (Realizado ou Falta)
        # Vamos buscar o agendamento original do dia para ATUALIZAR em vez de duplicar
        if status_recebido in ['Realizado', 'Falta']:
            inicio_dia = datetime.combine(data_apenas, datetime.min.time())
            fim_dia = datetime.combine(data_apenas, datetime.max.time())
            
            consulta_existente = Consulta.query.filter(
                Consulta.paciente_id == paciente_id,
                Consulta.data_hora >= inicio_dia,
                Consulta.data_hora <= fim_dia,
                Consulta.status == 'Agendado'
            ).first()
            
        if consulta_existente:
            # ATUALIZA O CARD EXISTENTE (Mantém a hora das 10:00 intacta!)
            consulta_existente.status = status_recebido
            consulta_existente.evolucao_texto = dados.get('evolucao_texto', '')
            consulta_existente.micro_metas = dados.get('micro_metas', {})
            
            if 'tipo_sessao' in dados:
                consulta_existente.tipo_sessao = dados['tipo_sessao']
                
            db.session.commit()
            return jsonify({"mensagem": "Agenda atualizada com evolução/falta!"}), 200
            
        else:
            # CRIA UM CARD NOVO (Apenas se não tinha agenda hoje, ou se está marcando uma nova data futura)
            nova_consulta = Consulta(
                paciente_id=paciente_id,
                data_hora=data_hora_requisicao,
                tipo_sessao=dados.get('tipo_sessao', 'Intervenção de Rotina'),
                status=status_recebido,
                evolucao_texto=dados.get('evolucao_texto', ''),
                micro_metas=dados.get('micro_metas', {})
            )
            
            db.session.add(nova_consulta)
            db.session.commit()
            return jsonify({"mensagem": "Novo registo salvo com sucesso!"}), 201
            
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