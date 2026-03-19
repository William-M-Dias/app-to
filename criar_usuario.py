import os
from dotenv import load_dotenv

# MÁGICA AQUI: Carrega as variáveis do arquivo .env ANTES de iniciar o sistema
load_dotenv()

from app import create_app
from app.extensions import db
from app.models.usuario import Usuario

app = create_app()

with app.app_context():
    # Verifica se a Edna já existe para não duplicar
    admin = Usuario.query.filter_by(email='edna@appto.com.br').first()
    
    if not admin:
        novo_usuario = Usuario(email='edna@appto.com.br', nome='Edna Nogueira')
        novo_usuario.set_senha('appto2026') # A senha inicial dela
        
        db.session.add(novo_usuario)
        db.session.commit()
        print("\n=========================================")
        print("✅ ACESSO CRIADO NO BANCO NEON COM SUCESSO!")
        print("E-mail: edna@appto.com.br")
        print("Senha:  appto2026")
        print("=========================================\n")
    else:
        print("\n✅ O usuário edna@appto.com.br já existe no banco de dados!\n")