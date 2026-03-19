from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    nome = db.Column(db.String(100), nullable=False)

    # Função que embaralha a senha antes de salvar no banco
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    # Função que checa se a senha digitada bate com a embaralhada
    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)