from app.extensions import db
from datetime import datetime

class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    # 1. Dados do Agendamento
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    
    # Para automatizar a agenda (Sessões contínuas)
    recorrente = db.Column(db.Boolean, default=False) 
    
    # Ex: Avaliação PEDI, Intervenção de Rotina, Devolutiva
    tipo_sessao = db.Column(db.String(100), nullable=False) 
    
    # Ex: Agendado, Confirmado, Realizado, Faltou, Cancelado
    status = db.Column(db.String(50), default='Agendado') 
    
    # 2. Dados Clínicos da Sessão (A preencher durante/após a consulta)
    evolucao_texto = db.Column(db.Text) 
    
    # Campo flexível (JSON) para os checklists de Observação Clínica (ex: Dispraxia, Ecolalia, Atenção)
    # Isso evita criar 50 colunas diferentes na base de dados e poupa processamento no Neon.
    dados_sensoriais_executivos = db.Column(db.JSON, nullable=True) 
    
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Consulta {self.data_hora} - Paciente ID {self.paciente_id}>'