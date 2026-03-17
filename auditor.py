import os

def listar_diretorio(caminho_inicial):
    # Pastas e extensões que vamos ignorar para o relatório não ficar sujo
    ignorar_pastas = {'.git', '__pycache__', '.venv', 'venv', '.pytest_cache', '.vscode'}
    
    print(f"ESTRUTURA ATUAL DO PROJETO: {os.path.abspath(caminho_inicial)}\n")
    
    for raiz, diretorios, arquivos in os.walk(caminho_inicial):
        # Remove as pastas ignoradas da busca
        diretorios[:] = [d for d in diretorios if d not in ignorar_pastas]
        
        # Calcula o nível de indentação para o visual
        nivel = raiz.replace(caminho_inicial, '').count(os.sep)
        indentacao = ' ' * 4 * nivel
        
        print(f"{indentacao}[Pasta] {os.path.basename(raiz)}/")
        
        sub_indentacao = ' ' * 4 * (nivel + 1)
        for arquivo in arquivos:
            # Ignora os arquivos de backup (.zip) para não poluir a lista
            if not arquivo.endswith('.zip') and arquivo != 'auditor.py':
                print(f"{sub_indentacao}- {arquivo}")

if __name__ == "__main__":
    listar_diretorio('.')