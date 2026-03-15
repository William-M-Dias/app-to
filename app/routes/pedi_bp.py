from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.pedi import AvaliacaoPEDI
from app.models.paciente import Paciente

# Certifique-se de que o nome da variável abaixo é EXATAMENTE pedi_bp
pedi_bp = Blueprint('pedi_bp', __name__, url_prefix='/api/pedi')

@pedi_bp.route('/<int:paciente_id>', methods=['GET'])
def buscar_avaliacoes(paciente_id):
    avaliacoes = AvaliacaoPEDI.query.filter_by(paciente_id=paciente_id).order_by(AvaliacaoPEDI.data_avaliacao.desc()).all()
    
    resultado = [{
        "id": a.id,
        "data_avaliacao": a.data_avaliacao.strftime('%d/%m/%Y'),
        "score_autocuidado": a.score_autocuidado,
        "score_mobilidade": a.score_mobilidade,
        "score_funcao_social": a.score_funcao_social,
        "assistencia_cuidador": a.assistencia_cuidador,
        "observacoes": a.observacoes
    } for a in avaliacoes]
    
    return jsonify(resultado), 200

@pedi_bp.route('/<int:paciente_id>', methods=['POST'])
def salvar_avaliacao(paciente_id):
    Paciente.query.get_or_404(paciente_id)
    dados = request.get_json()
    
    try:
        nova_avaliacao = AvaliacaoPEDI(
            paciente_id=paciente_id,
            score_autocuidado=int(dados.get('score_autocuidado', 0)),
            score_mobilidade=int(dados.get('score_mobilidade', 0)),
            score_funcao_social=int(dados.get('score_funcao_social', 0)),
            assistencia_cuidador=dados.get('assistencia_cuidador', ''),
            observacoes=dados.get('observacoes', '')
        )
        db.session.add(nova_avaliacao)
        db.session.commit()
        return jsonify({"mensagem": "Avaliação PEDI salva com sucesso!"}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500