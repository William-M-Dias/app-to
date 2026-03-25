from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.consulta import Consulta
from datetime import datetime, timedelta
from sqlalchemy import asc, desc
import uuid 

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
# ROTA INTELIGENTE DE REGISTRO / EVOLUÇÃO / RECORRÊNCIA
# ==========================================
@consulta_bp.route('/', methods=['POST'])
def registrar_evolucao():
    dados = request.get_json()
    
    if not dados or not dados.get('paciente_id'):
        return jsonify({"erro": "Dados incompletos para registo."}), 400
        
    try:
        paciente_id = dados['paciente_id']
        status_recebido = dados.get('status', 'Agendado') 
        profissional_id = dados.get('profissional_id')
        duracao_minutos = int(dados.get('duracao_minutos', 50)) 
        
        data_string = dados.get('data_hora')
        if not data_string:
            data_string = (datetime.utcnow() - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')
            
        if 'T' in data_string:
            data_string = data_string.replace('T', ' ')
        if len(data_string) == 10:
            data_string += ' 00:00'
            
        data_hora_requisicao = datetime.strptime(data_string, '%Y-%m-%d %H:%M')
        data_fim_estimada = data_hora_requisicao + timedelta(minutes=duracao_minutos)
        data_apenas = data_hora_requisicao.date()
        
        consulta_existente = None
        
        # 1. ATUALIZAR UM AGENDAMENTO (Baixa de Sessão: Realizado, Falta ou Cancelado)
        if status_recebido in ['Realizado', 'Falta', 'Cancelado']:
            inicio_dia = datetime.combine(data_apenas, datetime.min.time())
            fim_dia = datetime.combine(data_apenas, datetime.max.time())
            
            consulta_existente = Consulta.query.filter(
                Consulta.paciente_id == paciente_id,
                Consulta.data_hora >= inicio_dia,
                Consulta.data_hora <= fim_dia,
                Consulta.status == 'Agendado'
            ).first()
            
            if consulta_existente:
                consulta_existente.status = status_recebido
                consulta_existente.evolucao_texto = dados.get('evolucao_texto', '')
                consulta_existente.micro_metas = dados.get('micro_metas', {})
                if 'tipo_sessao' in dados:
                    consulta_existente.tipo_sessao = dados['tipo_sessao']
                    
                db.session.commit()
                return jsonify({"mensagem": "Agenda atualizada com evolução/falta!"}), 200

        # 2. SE CHEGOU AQUI, É UM NOVO AGENDAMENTO (Podendo ser único ou recorrente)
        recorrente = dados.get('recorrente', False)
        
        if recorrente:
            dias_semana = dados.get('dias_semana', []) 
            meses = int(dados.get('meses_recorrencia', 1))
            
            if not dias_semana:
                dias_semana = [data_hora_requisicao.weekday()]
                
            data_limite = data_hora_requisicao + timedelta(days=30 * meses)
            grupo_id = str(uuid.uuid4()) 
            
            data_atual_loop = data_hora_requisicao
            consultas_criadas = 0
            
            while data_atual_loop <= data_limite:
                if data_atual_loop.weekday() in dias_semana:
                    nova_consulta = Consulta(
                        paciente_id=paciente_id,
                        profissional_id=profissional_id,
                        data_hora=data_atual_loop,
                        data_fim=data_atual_loop + timedelta(minutes=duracao_minutos),
                        recorrente=True,
                        grupo_recorrencia=grupo_id,
                        tipo_sessao=dados.get('tipo_sessao', 'Intervenção de Rotina'),
                        status='Agendado',
                        evolucao_texto='',
                        micro_metas={}
                    )
                    db.session.add(nova_consulta)
                    consultas_criadas += 1
                    
                data_atual_loop += timedelta(days=1)
                
            db.session.commit()
            return jsonify({"mensagem": f"{consultas_criadas} sessões agendadas com sucesso!"}), 201
            
        else:
            # 3. AGENDAMENTO ÚNICO
            nova_consulta = Consulta(
                paciente_id=paciente_id,
                profissional_id=profissional_id,
                data_hora=data_hora_requisicao,
                data_fim=data_fim_estimada,
                recorrente=False,
                tipo_sessao=dados.get('tipo_sessao', 'Intervenção de Rotina'),
                status=status_recebido,
                evolucao_texto=dados.get('evolucao_texto', ''),
                micro_metas=dados.get('micro_metas', {})
            )
            
            db.session.add(nova_consulta)
            db.session.commit()
            return jsonify({"mensagem": "Novo registro único salvo com sucesso!"}), 201
            
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

# =====================================================================
# NOVO: ROTAS DO CALENDÁRIO VISUAL (FULLCALENDAR) - FASE 4
# =====================================================================
@consulta_bp.route('/calendario', methods=['GET'])
def obter_eventos_calendario():
    from app.models.paciente import Paciente
    
    # O FullCalendar envia 'start' e 'end' na URL automaticamente quando a tela é carregada
    start_str = request.args.get('start')
    end_str = request.args.get('end')
    
    query = Consulta.query.filter(Consulta.status == 'Agendado')
    
    if start_str and end_str:
        # Pega só a parte da data (AAAA-MM-DD)
        start_date = datetime.strptime(start_str[:10], '%Y-%m-%d')
        end_date = datetime.strptime(end_str[:10], '%Y-%m-%d')
        query = query.filter(Consulta.data_hora >= start_date, Consulta.data_hora <= end_date)
        
    consultas = query.all()
    eventos = []
    
    for c in consultas:
        paciente = Paciente.query.get(c.paciente_id)
        if paciente:
            # Se não houver data_fim, estima 50 minutos para desenhar o bloco perfeitamente
            fim_estimado = c.data_fim if c.data_fim else c.data_hora + timedelta(minutes=50)
            
            eventos.append({
                "id": c.id,
                "title": f"{paciente.nome}",
                "start": c.data_hora.isoformat(),
                "end": fim_estimado.isoformat(),
                # Sessões únicas ficam verde-água (teal), recorrentes ficam roxas (purple)
                "backgroundColor": "#0d9488" if not c.recorrente else "#7e22ce", 
                "borderColor": "transparent"
            })
            
    return jsonify(eventos), 200

@consulta_bp.route('/<int:id>/mover', methods=['PUT'])
def mover_consulta(id):
    consulta = Consulta.query.get_or_404(id)
    dados = request.get_json()
    
    nova_data_str = dados.get('nova_data')
    nova_data_fim_str = dados.get('nova_data_fim')
    
    if not nova_data_str:
        return jsonify({"erro": "Nova data não informada"}), 400
        
    try:
        # O FullCalendar envia no padrão ISO: 2026-03-24T10:00:00Z
        consulta.data_hora = datetime.fromisoformat(nova_data_str.replace('Z', '+00:00')).replace(tzinfo=None)
        
        if nova_data_fim_str:
            consulta.data_fim = datetime.fromisoformat(nova_data_fim_str.replace('Z', '+00:00')).replace(tzinfo=None)
            
        db.session.commit()
        return jsonify({"mensagem": "Horário atualizado com sucesso!"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500