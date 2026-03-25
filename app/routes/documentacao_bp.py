from flask import Blueprint, make_response
from fpdf import FPDF
from datetime import datetime

documentacao_bp = Blueprint('documentacao_bp', __name__, url_prefix='/api/documentacao')

class PDFManual(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(13, 148, 136) # Cor clinica-600
        self.cell(0, 10, 'APP-TO: Guia Pratico de Uso', 0, 1, 'C')
        
        self.set_font('Arial', 'I', 10)
        self.set_text_color(100, 116, 139) # slate-500
        self.cell(0, 6, 'Manual Operacional para a Rotina da Clinica', 0, 1, 'C')
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Página {self.page_no()} | Gerado automaticamente pelo APP-TO em {datetime.now().strftime("%d/%m/%Y")}', 0, 0, 'C')

@documentacao_bp.route('/gerar_pdf', methods=['GET'])
def gerar_pdf():
    pdf = PDFManual()
    pdf.add_page()
    
    # --- 1. PACIENTES ---
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(0, 10, '1. Gestao de Pacientes e Cadastro', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, "Para cadastrar uma nova criança, clique em 'Novo Paciente' na Mesa de Controle. Preencha os dados de contato dos responsáveis, o laudo e a queixa principal.\n\nIMPORTANTE: Se um paciente receber alta ou interromper o tratamento, altere o status dele para 'Inativo' ou 'Alta' no perfil. O APP-TO cancelará automaticamente todas as sessões futuras dessa criança, liberando espaço na agenda da clínica.")
    pdf.ln(6)

    # --- 2. AGENDA ---
    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, '2. Como Funciona a Agenda Inteligente', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, "A agenda permite criar sessões Únicas ou Recorrentes. Ao agendar uma sessão recorrente (ex: repetir por 6 meses), o sistema bloqueará aquele horário semanalmente para o paciente.\n\nREMARCAÇÃO: Na tela de Agenda (Visualização Semanal), você pode simplesmente clicar e arrastar (Drag & Drop) a sessão de um dia para o outro. O banco de dados salva a nova data na hora.\n\nCORES DA AGENDA:\nVerde = Realizado | Vermelho = Falta/Cancelado | Roxo = Recorrente | Azul = Única.")
    pdf.ln(6)

    # --- 3. PRONTUÁRIO ---
    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, '3. Prontuario, Evolucoes e Metas (GAS)', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, "Ao abrir o perfil do paciente, você encontra a linha do tempo de evolução. Em cada sessão realizada, você pode atribuir notas para as micro-metas (Mobilidade, Autocuidado, etc).\n\nQuando o sistema detectar que a criança está com um desempenho médio alto (Média GAS superior a +1) em várias sessões consecutivas, a Mesa de Controle exibirá um 'Alerta de Prontidão', sugerindo que é o momento ideal para aplicar uma nova Avaliação PEDI.")
    pdf.ln(6)
    
    # --- 4. ESTATÍSTICAS ---
    pdf.set_font('Arial', 'B', 13)
    pdf.cell(0, 10, '4. Painel de Gestao', 0, 1)
    
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, "Acesse a aba 'Gestão' para ter um panorama completo da clínica. Lá você visualizará gráficos de assiduidade (presenças vs. faltas) e o progresso clínico geral. Isso facilita a tomada de decisão terapêutica e financeira do consultório.")

    # Gera o arquivo
    pdf_bytes = pdf.output(dest='S').encode('latin-1')

    response = make_response(pdf_bytes)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Manual_de_Uso_APP-TO.pdf'
    
    return response