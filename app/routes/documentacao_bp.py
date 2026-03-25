from flask import Blueprint, make_response
from fpdf import FPDF
from datetime import datetime

documentacao_bp = Blueprint('documentacao_bp', __name__, url_prefix='/api/documentacao')

class PDFDocumentacao(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(13, 148, 136) # Cor clinica-600
        self.cell(0, 10, 'APP-TO: Documentacao Oficial de Arquitetura', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Página {self.page_no()} | Gerado em {datetime.now().strftime("%d/%m/%Y")}', 0, 0, 'C')

@documentacao_bp.route('/gerar_pdf', methods=['GET'])
def gerar_pdf():
    pdf = PDFDocumentacao()
    pdf.add_page()
    
    # --- 1. INTRODUÇÃO ---
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 10, '1. O Ecossistema (Mapa Mental)', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    mapa_mental = """
    APP-TO (Sistema de Gestão Clínica T.O.)
    |
    |-- FRONTEND (A Cara do Sistema)
    |   |-- Tailwind CSS (Estilização visual e responsividade)
    |   |-- Alpine.js (Interatividade leve, modais, abas)
    |   |-- FullCalendar.js (Motor da Agenda Inteligente)
    |   |-- Chart.js (Gráficos da tela de Gestão)
    |
    |-- BACKEND (O Cérebro)
    |   |-- Python 3.x + Flask (Servidor e Roteamento)
    |   |-- SQLAlchemy (Mapeamento do Banco de Dados)
    |
    |-- BANCO DE DADOS (A Memória)
    |   |-- PostgreSQL hospedado no Neon.tech
    |   |-- Cloudinary (Armazenamento permanente de imagens)
    """
    pdf.multi_cell(0, 6, mapa_mental)
    pdf.ln(5)

    # --- 2. SOLUÇÃO DE FOTOS ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '2. Estrutura de Armazenamento de Fotos (Cloudinary)', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    texto_fotos = """
    Devido à natureza de 'discos efêmeros' em servidores de nuvem (como o Render), as imagens 
    salvas localmente são apagadas durante os deploys. 
    
    SOLUÇÃO IMPLEMENTADA:
    Utilizamos a API do Cloudinary. Quando a clínica faz o upload de um avatar, o backend 
    direciona o arquivo para o Cloudinary, que o otimiza e devolve uma URL segura (HTTPS). 
    Apenas essa URL é salva na coluna 'foto_url' do banco de dados Neon. Isso garante que as 
    fotos jamais sumam, independentemente de reboots do servidor.
    """
    pdf.multi_cell(0, 6, texto_fotos)
    pdf.ln(5)

    # --- 3. PERFORMANCE ---
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '3. Otimizacao de Performance (Gargalo N+1)', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    texto_perf = """
    A página inicial (Mesa de Controle) realiza a verificação de 'Alertas de Prontidão' 
    cruzando dados de pacientes com o histórico de PEDI e o GAS das últimas 5 consultas.
    
    ESTRATÉGIA APLICADA:
    Em vez de realizar consultas iterativas (N+1 trips), o motor realiza um 'Eager Load' manual 
    (Bulk Query). Todos os dados necessários são carregados em duas consultas únicas e mapeados 
    em dicionários na memória do servidor, reduzindo o tempo de carregamento em mais de 95%.
    """
    pdf.multi_cell(0, 6, texto_perf)

    # Gerando o binário do PDF
    pdf_bytes = pdf.output(dest='S').encode('latin-1')

    # Enviando para o navegador baixar
    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=APP-TO_Documentacao_Arquitetura.pdf'
    
    return response