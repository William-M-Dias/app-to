import os
from flask import Flask
from app.extensions import db

def create_app():
    app = Flask(__name__)
    
    # Configurações do Banco de Dados Neon
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Otimização crucial para o plano gratuito (Pool de conexões)
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Inicializa o banco de dados com a aplicação
    db.init_app(app)

    # Rota básica de verificação de saúde (Health Check)
    @app.route('/health')
    def health_check():
        return {"status": "Servidor APP-TO Ativo", "message": "Integração Sensorial e PEDI prontos!"}, 200

    # Importa e registra os Blueprints (Rotas)
    from app.routes.paciente_bp import paciente_bp
    from app.routes.consulta_bp import consulta_bp
    
    app.register_blueprint(paciente_bp)
    app.register_blueprint(consulta_bp)

    return app 