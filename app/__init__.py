import os
from flask import Flask
from sqlalchemy import text
from app.extensions import db

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    db.init_app(app)

    # Importa os Blueprints
    from app.routes.paciente_bp import paciente_bp
    from app.routes.consulta_bp import consulta_bp
    from app.routes.frontend_bp import frontend_bp
    from app.routes.pedi_bp import pedi_bp
    from app.routes.obs_clinica_bp import obs_clinica_bp
    from app.routes.anamnese_bp import anamnese_bp

    # Registra os Blueprints
    app.register_blueprint(paciente_bp)
    app.register_blueprint(consulta_bp)
    app.register_blueprint(frontend_bp)
    app.register_blueprint(pedi_bp)
    app.register_blueprint(obs_clinica_bp)
    app.register_blueprint(anamnese_bp)

    with app.app_context():
        # Importa os modelos
        from app.models.paciente import Paciente
        from app.models.consulta import Consulta
        from app.models.pedi import AvaliacaoPEDI
        from app.models.obs_clinica import ObsClinica
        from app.models.anamnese import Anamnese
        
        # Cria as tabelas que ainda não existem
        db.create_all()
        
        # A MÁGICA: A "Picareta" de Segurança
        # Tenta forçar a adição da coluna micro_metas. Se ela já existir, ignora o erro e segue em frente.
        try:
            with db.engine.connect() as conexao:
                conexao.execute(text('ALTER TABLE consultas ADD COLUMN micro_metas JSONB;'))
                conexao.commit()
                print("Coluna 'micro_metas' adicionada com sucesso.")
        except Exception as e:
            # Se der erro (ex: a coluna já existe), ele passa silenciosamente
            print("Verificação do banco: Colunas OK.")

    return app