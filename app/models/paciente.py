from app.extensions import db
from datetime import datetime

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    escolaridade = db.Column(db.String(100))

    # NOVOS CAMPOS: Responsáveis
    nome_responsavel = db.Column(db.String(150))
    telefone_responsavel = db.Column(db.String(20))
    email_responsavel = db.Column(db.String(120))

    diagnostico = db.Column(db.String(255)) # Aumentado para 255
    queixa_principal = db.Column(db.Text)
    historico_desenvolvimento = db.Column(db.Text)
    intervencoes_atuais = db.Column(db.Text)
    
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    consultas = db.relationship('Consulta', backref='paciente', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento.strftime('%Y-%m-%d') if self.data_nascimento else None,
            "escolaridade": self.escolaridade,
            "diagnostico": self.diagnostico,
            "queixa_principal": self.queixa_principal,
            "nome_responsavel": self.nome_responsavel,
            "telefone_responsavel": self.telefone_responsavel,
            "email_responsavel": self.email_responsavel
        }