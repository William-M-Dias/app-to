import os

def gerar_auditoria():
    pastas_ignoradas = ['venv', '.git', '__pycache__', '.pytest_cache']
    extensoes_permitidas = ['.py', '.html']
    
    with open('raio_x_projeto.txt', 'w', encoding='utf-8') as log:
        log.write("=== AUDITORIA COMPLETA DO PROJETO ===\n\n")
        
        for raiz, diretorios, arquivos in os.walk('.'):
            diretorios[:] = [d for d in diretorios if d not in pastas_ignoradas]
            
            for arquivo in arquivos:
                if any(arquivo.endswith(ext) for ext in extensoes_permitidas):
                    caminho_completo = os.path.join(raiz, arquivo)
                    log.write(f"\n{'='*60}\n")
                    log.write(f"FICHEIRO: {caminho_completo}\n")
                    log.write(f"{'='*60}\n")
                    try:
                        with open(caminho_completo, 'r', encoding='utf-8') as f:
                            log.write(f.read() + "\n")
                    except Exception as e:
                        log.write(f"[Erro ao ler arquivo: {e}]\n")

    print("Auditoria completa gerada com sucesso em: raio_x_projeto.txt")

if __name__ == '__main__':
    gerar_auditoria()