import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (URL do Neon)
load_dotenv()

from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("🚀 Iniciando injeção das novas colunas de Agenda...")
    
    try:
        # 1. Atualizando tabela pacientes
        db.session.execute(text("ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS status_clinico VARCHAR(50) DEFAULT 'Ativo';"))
        
        # 2. Atualizando tabela consultas
        db.session.execute(text("ALTER TABLE consultas ADD COLUMN IF NOT EXISTS profissional_id INTEGER;"))
        db.session.execute(text("ALTER TABLE consultas ADD COLUMN IF NOT EXISTS data_fim TIMESTAMP;"))
        db.session.execute(text("ALTER TABLE consultas ADD COLUMN IF NOT EXISTS grupo_recorrencia VARCHAR(100);"))
        
        # Opcional: Se 'usuarios' não existir ainda, criaremos uma foreign key no futuro,
        # por enquanto o PostgreSQL aceita a coluna integer limpa.
        
        db.session.commit()
        print("✅ Banco de dados blindado! Novas colunas adicionadas sem perda de dados.")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Erro durante a atualização do banco: {str(e)}")