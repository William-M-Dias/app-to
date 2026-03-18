from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.paciente import Paciente
from datetime import datetime

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