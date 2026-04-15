from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    
    # NOVO: Profissional responsável pela sessão
    profissional_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    
    data_hora = db.Column(db.DateTime, nullable=False)
    # NOVO: Data/Hora de término para desenhar o bloco na Agenda Visual
    data_fim = db.Column(db.DateTime, nullable=True)
    
    recorrente = db.Column(db.Boolean, default=False) 
    # NOVO: ID unificador para sessões clonadas (Ex: todas as sessões do Miguel geradas juntas)
    grupo_recorrencia = db.Column(db.String(100), nullable=True)
    
    tipo_sessao = db.Column(db.String(100), nullable=False) 
    status = db.Column(db.String(50), default='Agendado') 
    
    evolucao_texto = db.Column(db.Text) 
    
    # Mantido para garantir Risco Zero
    dados_sensoriais_executivos = db.Column(db.JSON, nullable=True) 
    
    # O MOTOR DE INFERÊNCIA DO PEDI
    micro_metas = db.Column(JSONB, nullable=True)
    
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Consulta {self.data_hora} - Paciente ID {self.paciente_id}>'