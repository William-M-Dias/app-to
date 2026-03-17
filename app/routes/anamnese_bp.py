from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.anamnese import Anamnese

anamnese_bp = Blueprint('anamnese_bp', __name__, url_prefix='/api/anamnese')

@anamnese_bp.route('/<int:paciente_id>', methods=['POST'])
def salvar_anamnese(paciente_id):
    dados = request.get_json()
    try:
        nova_anamnese = Anamnese(
            paciente_id=paciente_id,
            dados_triagem=dados.get('dados_triagem', {}),
            queixa_principal=dados.get('queixa_principal', '')
        )
        db.session.add(nova_anamnese)
        db.session.commit()
        return jsonify({"mensagem": "Anamnese salva com sucesso!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

@anamnese_bp.route('/<int:paciente_id>', methods=['GET'])
def listar_anamnese(paciente_id):
    anamneses = Anamnese.query.filter_by(paciente_id=paciente_id).order_by(Anamnese.data_criacao.desc()).all()
    return jsonify([{
        "id": a.id,
        "data": a.data_criacao.strftime('%d/%m/%Y'),
        "dados": a.dados_triagem,
        "queixa": a.queixa_principal
    } for a in anamneses]), 200