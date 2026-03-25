import os
import shutil
from dotenv import load_dotenv

# 1. CARREGA AS VARIÁVEIS DE AMBIENTE (A SENHA DO BANCO NEON) ANTES DE TUDO!
load_dotenv()

from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()

def run_diagnostics_and_cleanup():
    print("==================================================")
    print(" 🔍 INICIANDO DIAGNÓSTICO E FAXINA DO APP-TO 🔍")
    print("==================================================\n")
    
    print("🧹 1. FAXINA DE PASTAS E ARQUIVOS DESNECESSÁRIOS...")
    pasta_fantasma = os.path.join('app', 'templates', 'app')
    if os.path.exists(pasta_fantasma):
        try:
            shutil.rmtree(pasta_fantasma)
            print(f"   ✅ [SUCESSO] Pasta duplicada eliminada: {pasta_fantasma}")
        except Exception as e:
            print(f"   ❌ [ERRO] Falha ao tentar apagar a pasta: {str(e)}")
    else:
        print("   ✨ [OK] Nenhuma pasta duplicada encontrada na raiz.")

    cache_count = 0
    for root, dirs, files in os.walk('.', topdown=False):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                dir_path = os.path.join(root, dir_name)
                try:
                    shutil.rmtree(dir_path)
                    cache_count += 1
                except:
                    pass
    print(f"   ✨ [OK] {cache_count} diretórios de lixo (__pycache__) removidos.")

    print("\n📁 2. MAPEAMENTO DA ESTRUTURA CRÍTICA...")
    pastas_criticas = ['app/templates', 'app/routes', 'app/models']
    for p in pastas_criticas:
        if os.path.exists(p):
            print(f"   ✅ [OK] Pasta íntegra: {p}")
        else:
            print(f"   ❌ [ERRO FATAL] Pasta AUSENTE: {p}")
            
    arquivos = ['app/templates/agenda.html', 'app/templates/estatisticas.html', 'app/routes/consulta_bp.py']
    for a in arquivos:
        if os.path.exists(a):
            print(f"   ✅ [OK] Arquivo íntegro: {a}")
        else:
            print(f"   ❌ [ERRO FATAL] Arquivo AUSENTE: {a}")

    print("\n🗄️ 3. CHECK-UP DO BANCO DE DADOS (NEON)...")
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            print("   ✅ [OK] Conexão com banco Neon 100% estável.")
            
            total_consultas = db.session.execute(text("SELECT COUNT(*) FROM consultas")).scalar()
            nulos_prof = db.session.execute(text("SELECT COUNT(*) FROM consultas WHERE profissional_id IS NULL")).scalar()
            nulos_fim = db.session.execute(text("SELECT COUNT(*) FROM consultas WHERE data_fim IS NULL")).scalar()
            
            print(f"   📊 Total de Agendamentos Cadastrados: {total_consultas}")
            
            if nulos_prof > 0:
                print(f"   ⚠️ [ALERTA] Existem {nulos_prof} consultas sem 'profissional_id' vinculado.")
            else:
                print("   ✅ [OK] Todas as consultas possuem profissional.")
                
        except Exception as e:
            print(f"   ❌ [ERRO CRÍTICO NO BANCO]: {str(e)}")

    print("\n==================================================")
    print(" 🚀 DIAGNÓSTICO E FAXINA CONCLUÍDOS!")
    print("==================================================\n")

if __name__ == '__main__':
    run_diagnostics_and_cleanup()