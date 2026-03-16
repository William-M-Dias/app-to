from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class ObsClinica(db.Model):
    __tablename__ = 'obs_clinica'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    data_observacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Armazena Psicomotora, Executivas, Sensorial e Práxis do seu DOC
    dados_json = db.Column(JSONB, nullable=False)
    observacoes_texto = db.Column(db.Text)

    paciente = db.relationship('Paciente', backref=db.backref('observacoes_clinicas', lazy=True))