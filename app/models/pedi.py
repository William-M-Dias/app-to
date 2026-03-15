from app.extensions import db
from datetime import datetime

class AvaliacaoPEDI(db.Model):
    __tablename__ = 'avaliacoes_pedi'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    data_avaliacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Pontuações de Independência (0 a 100)
    score_autocuidado = db.Column(db.Integer, default=0)
    score_mobilidade = db.Column(db.Integer, default=0)
    score_funcao_social = db.Column(db.Integer, default=0)
    
    # Assistência e Observações
    assistencia_cuidador = db.Column(db.String(100), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    # Relação com o Paciente (para facilitar buscas futuras)
    paciente = db.relationship('Paciente', backref=db.backref('avaliacoes_pedi', lazy=True))