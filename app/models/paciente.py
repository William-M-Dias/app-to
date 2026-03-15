from app.extensions import db
from datetime import datetime

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    
    # 1. Identificação
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    escolaridade = db.Column(db.String(100))
    
    # 2. Histórico Clínico
    diagnostico = db.Column(db.String(200))
    queixa_principal = db.Column(db.Text)
    historico_desenvolvimento = db.Column(db.Text) # Ex: Marcos motores e linguagem
    intervencoes_atuais = db.Column(db.Text)       # Ex: Outras terapias e medicação
    
    # Controlo de sistema
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento: Um paciente pode ter várias consultas/sessões
    consultas = db.relationship('Consulta', backref='paciente', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Paciente {self.nome}>'