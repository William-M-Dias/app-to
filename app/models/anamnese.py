from app.extensions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class Anamnese(db.Model):
    __tablename__ = 'anamnese'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # O "Buraco Negro" que vai guardar TDAH, TEA, TOD, Sensorial, etc.
    dados_triagem = db.Column(JSONB, nullable=False) 
    queixa_principal = db.Column(db.Text)

    paciente = db.relationship('Paciente', backref=db.backref('anamneses', lazy=True))