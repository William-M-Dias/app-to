from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    
    recorrente = db.Column(db.Boolean, default=False) 
    tipo_sessao = db.Column(db.String(100), nullable=False) 
    status = db.Column(db.String(50), default='Agendado') 
    
    evolucao_texto = db.Column(db.Text) 
    
    # Mantido para garantir Risco Zero (não crashar o Neon)
    dados_sensoriais_executivos = db.Column(db.JSON, nullable=True) 
    
    # NOVO: O MOTOR DE INFERÊNCIA DO PEDI
    micro_metas = db.Column(JSONB, nullable=True)
    
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

    paciente = db.relationship('Paciente', backref=db.backref('consultas', lazy=True))

    def __repr__(self):
        return f'<Consulta {self.data_hora} - Paciente ID {self.paciente_id}>'