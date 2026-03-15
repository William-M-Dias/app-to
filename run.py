from app import create_app
from app.extensions import db
from dotenv import load_dotenv
import os

# Carrega as variáveis do .env
load_dotenv()

# Cria a instância da aplicação
app = create_app()

# Garante que as tabelas sejam criadas no Neon antes da primeira requisição
with app.app_context():
    # Importar os modelos aqui garante que o SQLAlchemy os reconheça antes de criar as tabelas
    from app.models import paciente, consulta
    db.create_all()

if __name__ == '__main__':
    # Define a porta (Render usa a variável PORT, localmente usamos 5000)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)