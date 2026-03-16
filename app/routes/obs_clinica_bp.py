from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.obs_clinica import ObsClinica

obs_clinica_bp = Blueprint('obs_clinica_bp', __name__, url_prefix='/api/obs-clinica')

@obs_clinica_bp.route('/<int:paciente_id>', methods=['POST'])
def salvar_obs(paciente_id):
    dados = request.get_json()
    try:
        nova_obs = ObsClinica(
            paciente_id=paciente_id,
            dados_json=dados.get('dados_json'),
            observacoes_texto=dados.get('observacoes_texto', '')
        )
        db.session.add(nova_obs)
        db.session.commit()
        return jsonify({"mensagem": "Observação salva!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500

@obs_clinica_bp.route('/<int:paciente_id>', methods=['GET'])
def listar_obs(paciente_id):
    obs = ObsClinica.query.filter_by(paciente_id=paciente_id).order_by(ObsClinica.data_observacao.desc()).all()
    return jsonify([{
        "id": o.id,
        "data": o.data_observacao.strftime('%d/%m/%Y'),
        "dados": o.dados_json
    } for o in obs]), 200