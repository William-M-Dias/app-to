import os
from flask import Blueprint, request, jsonify, current_app, url_for
from app.extensions import db
from app.models.paciente import Paciente
from app.models.consulta import Consulta
from app.models.pedi import AvaliacaoPEDI
from datetime import datetime, timedelta
from sqlalchemy import text, desc
from werkzeug.utils import secure_filename

paciente_bp = Blueprint('paciente_bp', __name__, url_prefix='/api/pacientes')

@paciente_bp.route('/', methods=['GET'])
def listar_pacientes():
    try:
        pacientes = Paciente.query.all()
        return jsonify([p.to_dict() for p in pacientes]), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar: {str(e)}"}), 500

@paciente_bp.route('/<int:id>', methods=['GET'])
def obter_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    return jsonify(paciente.to_dict()), 200

@paciente_bp.route('/', methods=['POST'])
def criar_paciente():
    dados = request.get_json()
    if not dados or not dados.get('nome') or not dados.get('data_nascimento'):
        return jsonify({"erro": "Nome e nascimento obrigatórios."}), 400
    try:
        data_nasc = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()
        novo = Paciente(
            nome=dados['nome'],
            data_nascimento=data_nasc,
            escolaridade=dados.get('escolaridade', ''),
            diagnostico=dados.get('diagnostico', ''),
            queixa_principal=dados.get('queixa_principal', ''),
            nome_responsavel=dados.get('nome_responsavel', ''),
            telefone_responsavel=dados.get('telefone_responsavel', ''),
            email_responsavel=dados.get('email_responsavel', '')
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({"mensagem": "Sucesso!", "id": novo.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

@paciente_bp.route('/<int:id>', methods=['PUT'])
def atualizar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    dados = request.get_json()
    try:
        if 'nome' in dados: paciente.nome = dados['nome']
        if 'data_nascimento' in dados:
            paciente.data_nascimento = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()
        if 'escolaridade' in dados: paciente.escolaridade = dados['escolaridade']
        if 'diagnostico' in dados: paciente.diagnostico = dados['diagnostico']
        if 'queixa_principal' in dados: paciente.queixa_principal = dados['queixa_principal']
        if 'nome_responsavel' in dados: paciente.nome_responsavel = dados['nome_responsavel']
        if 'telefone_responsavel' in dados: paciente.telefone_responsavel = dados['telefone_responsavel']
        if 'email_responsavel' in dados: paciente.email_responsavel = dados['email_responsavel']
        
        db.session.commit()
        return jsonify({"mensagem": "Paciente atualizado com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

@paciente_bp.route('/<int:id>', methods=['DELETE'])
def deletar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    try:
        db.session.execute(text("DELETE FROM consultas WHERE paciente_id = :pid"), {"pid": id})
        db.session.execute(text("DELETE FROM anamnese WHERE paciente_id = :pid"), {"pid": id})
        db.session.execute(text("DELETE FROM avaliacoes_pedi WHERE paciente_id = :pid"), {"pid": id})
        db.session.execute(text("DELETE FROM obs_clinica WHERE paciente_id = :pid"), {"pid": id})
        
        db.session.delete(paciente)
        db.session.commit()
        return jsonify({"mensagem": "Excluído com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

@paciente_bp.route('/<int:id>/editar_mapa', methods=['POST'])
def editar_mapa(id):
    paciente = Paciente.query.get_or_404(id)
    dados = request.get_json()
    try:
        paciente.queixa_principal = dados.get('observacoes', paciente.queixa_principal)
        db.session.commit()
        return jsonify({"mensagem": "Mapa atualizado!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

@paciente_bp.route('/<int:id>/upload_foto', methods=['POST'])
def upload_foto(id):
    paciente = Paciente.query.get_or_404(id)
    if 'foto' not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    arquivo = request.files['foto']
    if arquivo.filename == '':
        return jsonify({"erro": "Arquivo sem nome"}), 400

    upload_path = os.path.join(current_app.static_folder, 'uploads', 'perfil')
    
    if not os.path.exists(upload_path):
        os.makedirs(upload_path, exist_ok=True)

    filename = secure_filename(f"avatar_{id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
    arquivo.save(os.path.join(upload_path, filename))
    
    paciente.foto_url = url_for('static', filename=f'uploads/perfil/{filename}')
    db.session.commit()
    
    return jsonify({"url": paciente.foto_url}), 200

@paciente_bp.route('/alertas', methods=['GET'])
def alertas_prontidao():
    try:
        pacientes = Paciente.query.all()
        alertas = []
        hoje = datetime.utcnow().date()

        # ==============================================================================
        # PERFORMANCE MESTRE (O Fim da Lentidão N+1)
        # Vamos ao banco APENAS 2 vezes e trazemos tudo agrupado na memória super-rápida.
        # ==============================================================================
        todas_consultas = Consulta.query.filter_by(status='Realizado').order_by(desc(Consulta.data_hora)).all()
        todos_pedis = AvaliacaoPEDI.query.order_by(desc(AvaliacaoPEDI.data_avaliacao)).all()

        # Dicionários em memória
        consultas_por_paciente = {}
        for c in todas_consultas:
            if c.paciente_id not in consultas_por_paciente:
                consultas_por_paciente[c.paciente_id] = []
            if len(consultas_por_paciente[c.paciente_id]) < 5:
                consultas_por_paciente[c.paciente_id].append(c)

        pedi_por_paciente = {}
        for p_aval in todos_pedis:
            if p_aval.paciente_id not in pedi_por_paciente:
                pedi_por_paciente[p_aval.paciente_id] = p_aval # Salva apenas o mais recente

        # ==============================================================================

        for p in pacientes:
            # Em vez de ir ao banco, lemos da memória (Instantâneo)
            ultimo_pedi = pedi_por_paciente.get(p.id)
            ultimas_consultas = consultas_por_paciente.get(p.id, [])
            
            motivos = []
            
            if ultimo_pedi:
                data_pedi = ultimo_pedi.data_avaliacao
                if isinstance(data_pedi, str):
                    try:
                        data_pedi = datetime.strptime(data_pedi.split(' ')[0], '%Y-%m-%d').date()
                    except:
                        data_pedi = hoje
                elif isinstance(data_pedi, datetime):
                    data_pedi = data_pedi.date()
                
                dias_passados = (hoje - data_pedi).days
                meses_passados = dias_passados / 30
                if meses_passados >= 6:
                    motivos.append(f"A última avaliação PEDI foi há {int(meses_passados)} meses. Recomendada reavaliação de rotina.")
            else:
                if len(ultimas_consultas) > 0:
                    motivos.append("Paciente em intervenção, mas ainda não possui o PEDI base registado.")
                    
            gas_total = 0
            qtd_gas = 0
            for c in ultimas_consultas:
                if c.micro_metas and isinstance(c.micro_metas, dict):
                    valores = [v for k, v in c.micro_metas.items() if v is not None and isinstance(v, (int, float)) and k in ['autocuidado', 'mobilidade', 'funcao_social']]
                    if valores:
                        gas_total += sum(valores) / len(valores)
                        qtd_gas += 1
                        
            if qtd_gas >= 3:
                media_gas = gas_total / qtd_gas
                if media_gas >= 1.0:
                    motivos.append(f"Alta performance constante detectada (Média GAS: +{media_gas:.1f}). Criança pronta para subir de nível no PEDI.")
                    
            if motivos:
                alertas.append({
                    "paciente_id": p.id,
                    "nome_paciente": p.nome,
                    "foto_url": p.foto_url,
                    "motivos": motivos
                })
                
        return jsonify(alertas), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao processar alertas: {str(e)}"}), 500

# ==============================================================================
# NOVO: MOTOR DE INATIVAÇÃO DE PACIENTE E LIMPEZA DE AGENDA (Fase 3)
# ==============================================================================
@paciente_bp.route('/<int:id>/status', methods=['PUT'])
def alterar_status(id):
    paciente = Paciente.query.get_or_404(id)
    dados = request.get_json()
    novo_status = dados.get('status_clinico')

    if not novo_status:
        return jsonify({"erro": "Status não fornecido."}), 400

    try:
        paciente.status_clinico = novo_status
        
        # A MÁGICA DA LIMPEZA: Se inativar ou der alta, apaga as sessões futuras!
        if novo_status in ['Inativo', 'Alta']:
            hoje = datetime.utcnow() - timedelta(hours=3)
            
            consultas_futuras = Consulta.query.filter(
                Consulta.paciente_id == id,
                Consulta.data_hora > hoje,
                Consulta.status == 'Agendado'
            ).all()
            
            # Deleta as sessões futuras para liberar espaço na agenda da clínica
            for c in consultas_futuras:
                db.session.delete(c)
                
        db.session.commit()
        return jsonify({"mensagem": f"Paciente {novo_status}. Agenda atualizada!"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500