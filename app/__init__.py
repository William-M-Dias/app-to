import os
from flask import Flask
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

    @app.route('/health')
    def health_check():
        return {"status": "Servidor APP-TO Ativo"}, 200

    # Importa os Blueprints
    from app.routes.paciente_bp import paciente_bp
    from app.routes.consulta_bp import consulta_bp
    from app.routes.frontend_bp import frontend_bp # <--- NOVO
    
    # Registra os Blueprints
    app.register_blueprint(paciente_bp)
    app.register_blueprint(consulta_bp)
    app.register_blueprint(frontend_bp)            # <--- NOVO

    return app