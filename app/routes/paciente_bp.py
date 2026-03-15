from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.paciente import Paciente
from datetime import datetime

# Criação do Blueprint
paciente_bp = Blueprint('paciente_bp', __name__, url_prefix='/api/pacientes')

@paciente_bp.route('/', methods=['GET'])
def listar_pacientes():
    pacientes = Paciente.query.all()
    resultado = [{
        "id": p.id,
        "nome": p.nome,
        "diagnostico": p.diagnostico,
        "data_nascimento": p.data_nascimento.strftime('%Y-%m-%d') if p.data_nascimento else None
    } for p in pacientes]
    return jsonify(resultado), 200

@paciente_bp.route('/', methods=['POST'])
def criar_paciente():
    dados = request.get_json()
    
    # Validação básica para evitar erros no Neon
    if not dados or not dados.get('nome') or not dados.get('data_nascimento'):
        return jsonify({"erro": "Nome e data de nascimento são obrigatórios."}), 400
        
    try:
        # Converte a string de data que vem do Frontend para um objeto Date do Python
        data_nasc = datetime.strptime(dados['data_nascimento'], '%Y-%m-%d').date()
        
        novo_paciente = Paciente(
            nome=dados['nome'],
            data_nascimento=data_nasc,
            escolaridade=dados.get('escolaridade', ''),
            diagnostico=dados.get('diagnostico', ''),
            queixa_principal=dados.get('queixa_principal', '')
        )
        
        db.session.add(novo_paciente)
        db.session.commit()
        return jsonify({"mensagem": "Paciente registado com sucesso!", "id": novo_paciente.id}), 201
        
    except Exception as e:
        db.session.rollback() # Protege a base de dados em caso de falha
        return jsonify({"erro": str(e)}), 500