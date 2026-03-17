import os
import zipfile
from datetime import datetime

def fazer_backup():
    data_atual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_zip = f"APP-TO_backup_{data_atual}.zip"
    
    # Pastas e arquivos que NÃO precisamos copiar (pesados ou recriáveis)
    ignorar = {'.git', '__pycache__', '.venv', 'venv', 'gerar_backup.py'}
    
    print(f"Compactando projeto de forma segura em: {nome_zip}...")
    
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for raiz, diretorios, arquivos in os.walk('.'):
            diretorios[:] = [d for d in diretorios if d not in ignorar]
            for arquivo in arquivos:
                if arquivo not in ignorar and not arquivo.endswith('.zip'):
                    caminho_completo = os.path.join(raiz, arquivo)
                    zipf.write(caminho_completo, os.path.relpath(caminho_completo, '.'))
                    
    print("✅ Backup gerado com sucesso! Projeto blindado.")

if __name__ == "__main__":
    fazer_backup()