import os
from flask import Flask
from sqlalchemy import text
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True, "pool_recycle": 300}

    db.init_app(app)

    # Blueprints
    from app.routes.paciente_bp import paciente_bp
    from app.routes.consulta_bp import consulta_bp
    from app.routes.frontend_bp import frontend_bp
    from app.routes.pedi_bp import pedi_bp
    from app.routes.obs_clinica_bp import obs_clinica_bp
    from app.routes.anamnese_bp import anamnese_bp

    app.register_blueprint(paciente_bp)
    app.register_blueprint(consulta_bp)
    app.register_blueprint(frontend_bp)
    app.register_blueprint(pedi_bp)
    app.register_blueprint(obs_clinica_bp)
    app.register_blueprint(anamnese_bp)

    with app.app_context():
        from app.models.paciente import Paciente
        from app.models.consulta import Consulta
        db.create_all()
        
        # A PICARETA: Garante colunas dos pais
        try:
            with db.engine.connect() as conexao:
                conexao.execute(text('ALTER TABLE consultas ADD COLUMN IF NOT EXISTS micro_metas JSONB;'))
                conexao.execute(text('ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS nome_responsavel VARCHAR(150);'))
                conexao.execute(text('ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS telefone_responsavel VARCHAR(20);'))
                conexao.execute(text('ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS email_responsavel VARCHAR(120);'))
                conexao.commit()
                print("Banco Neon: Estrutura OK.")
        except Exception:
            print("Banco Neon: Verificação concluída.")

    return app