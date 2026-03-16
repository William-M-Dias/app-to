import os

def listar_diretorio(caminho_inicial):
    # Pastas que vamos ignorar para o relatório não ficar gigante e sujo
    ignorar = {'.git', '__pycache__', '.venv', 'venv', '.pytest_cache', '.vscode'}
    
    print(f"ESTRUTURA ATUAL DO PROJETO: {os.path.abspath(caminho_inicial)}\n")
    
    for raiz, diretorios, arquivos in os.walk(caminho_inicial):
        # Remove as pastas ignoradas da busca
        diretorios[:] = [d for d in diretorios if d not in ignorar]
        
        # Calcula o nível de indentação para o visual
        nivel = raiz.replace(caminho_inicial, '').count(os.sep)
        indentacao = ' ' * 4 * (nivel)
        
        print(f"{indentacao}[Pasta] {os.path.basename(raiz)}/")
        
        sub_indentacao = ' ' * 4 * (nivel + 1)
        for arquivo in arquivos:
            if arquivo != 'auditor.py': # Não mostra o próprio script
                print(f"{sub_indentacao}- {arquivo}")

if __name__ == "__main__":
    listar_diretorio('.')