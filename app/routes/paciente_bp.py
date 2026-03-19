import os
from flask import Blueprint, request, jsonify, current_app
from app.extensions import db
from app.models.paciente import Paciente
from datetime import datetime
from sqlalchemy import text
from werkzeug.utils import secure_filename

paciente_bp = Blueprint('paciente_bp', __name__, url_prefix='/api/pacientes')

@paciente_bp.route('/', methods=['GET'])
def listar_pacientes():
    pacientes = Paciente.query.all()
    return jsonify([p.to_dict() for p in pacientes]), 200

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
        # SEGURO EXTRA: Limpeza manual de todas as tabelas ligadas antes de apagar o paciente
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

# NOVA ROTA: Edição rápida do Mapa Clínico (Teste 2)
@paciente_bp.route('/<int:id>/editar_mapa', methods=['POST'])
def editar_mapa(id):
    paciente = Paciente.query.get_or_404(id)
    dados = request.get_json()
    try:
        paciente.queixa_principal = dados.get('observacoes', paciente.queixa_principal)
        db.session.commit()
        return jsonify({"mensagem": "Mapa atualizado!"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar mapa"}), 500

# ROTA FASE 6: Upload de Avatar
@paciente_bp.route('/<int:id>/upload_foto', methods=['POST'])
def upload_foto(id):
    paciente = Paciente.query.get_or_404(id)
    if 'foto' not in request.files:
        return jsonify({"erro": "Nenhum arquivo"}), 400
    
    arquivo = request.files['foto']
    if arquivo.filename == '':
        return jsonify({"erro": "Sem nome"}), 400

    filename = secure_filename(f"avatar_{id}.jpg")
    upload_path = os.path.join(current_app.root_path, 'static/uploads/perfil')
    
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        
    arquivo.save(os.path.join(upload_path, filename))
    paciente.foto_url = f"/static/uploads/perfil/{filename}"
    db.session.commit()
    
    return jsonify({"url": paciente.foto_url}), 200