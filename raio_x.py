import os

def gerar_raio_x(caminho_inicial='.', arquivo_saida='raio_x_projeto.txt'):
    # Pastas e arquivos que não precisamos ler (para o arquivo não ficar gigante)
    ignorar_pastas = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', '.vscode'}
    extensoes_permitidas = {'.py', '.html', '.txt'}

    print("Iniciando o Raio-X Profundo do APP-TO...")

    with open(arquivo_saida, 'w', encoding='utf-8') as f_out:
        f_out.write("=== RAIO-X COMPLETO DO PROJETO APP-TO ===\n\n")

        for raiz, diretorios, arquivos in os.walk(caminho_inicial):
            # Filtra as pastas ignoradas
            diretorios[:] = [d for d in diretorios if d not in ignorar_pastas]

            for arquivo in arquivos:
                _, ext = os.path.splitext(arquivo)
                
                # Pega apenas arquivos de código e ignora scripts de backup ou o próprio raio_x
                if ext in extensoes_permitidas and arquivo not in ['raio_x.py', 'auditor.py', 'gerar_backup.py']:
                    caminho_completo = os.path.join(raiz, arquivo)
                    caminho_relativo = os.path.relpath(caminho_completo, caminho_inicial)

                    f_out.write(f"\n" + "="*60 + "\n")
                    f_out.write(f"ARQUIVO: {caminho_relativo}\n")
                    f_out.write("="*60 + "\n\n")

                    try:
                        with open(caminho_completo, 'r', encoding='utf-8') as f_in:
                            f_out.write(f_in.read() + "\n")
                    except Exception as e:
                        f_out.write(f"[Erro ao ler arquivo: {e}]\n")

    print(f"Sucesso! O DNA do seu projeto foi salvo no arquivo: '{arquivo_saida}'.")

if __name__ == "__main__":
    gerar_raio_x()