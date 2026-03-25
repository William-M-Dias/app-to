import os
import zipfile
import glob
from datetime import datetime

def fazer_backup():
    data_atual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_zip = f"APP-TO_backup_{data_atual}.zip"
    
    # Pastas e arquivos que NÃO precisamos copiar (pesados ou recriáveis)
    ignorar = {'.git', '__pycache__', '.venv', 'venv', 'gerar_backup.py'}
    
    print(f"Compactando projeto de forma segura em: {nome_zip}...")
    
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for raiz, diretorios, arquivos in os.walk('.'):
            # Remove diretórios ignorados da busca
            diretorios[:] = [d for d in diretorios if d not in ignorar]
            for arquivo in arquivos:
                # Não zipa arquivos ignorados e nem arquivos .zip antigos/novos
                if arquivo not in ignorar and not arquivo.endswith('.zip'):
                    caminho_completo = os.path.join(raiz, arquivo)
                    zipf.write(caminho_completo, os.path.relpath(caminho_completo, '.'))
                    
    print(f"✅ Backup gerado com sucesso: {nome_zip}")

    # ==========================================
    # LÓGICA DE FAXINA (AUTO-DELETE)
    # ==========================================
    print("🧹 Iniciando limpeza de backups antigos...")
    backups_encontrados = glob.glob("APP-TO_backup_*.zip")
    
    for backup in backups_encontrados:
        if backup != nome_zip: # Se não for o backup que acabei de criar...
            try:
                os.remove(backup)
                print(f"🗑️ Backup antigo removido: {backup}")
            except Exception as e:
                print(f"⚠️ Erro ao remover {backup}: {e}")
                
    print("🚀 PROJETO BLINDADO E SERVIDOR LIMPO!")

if __name__ == "__main__":
    fazer_backup()