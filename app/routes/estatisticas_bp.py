from flask import Blueprint, jsonify
from sqlalchemy import func
from app.extensions import db
from app.models.paciente import Paciente
from app.models.consulta import Consulta
from datetime import datetime, timedelta

estatisticas_bp = Blueprint('estatisticas_bp', __name__, url_prefix='/api/estatisticas')

@estatisticas_bp.route('/geral', methods=['GET'])
def obter_estatisticas():
    try:
        # 1. Total de Pacientes Ativos no Diretório
        total_pacientes = Paciente.query.count()

        # 2. Distribuição Clínica (Diagnósticos)
        # Como o diagnóstico pode vir separado por vírgula (ex: "TEA, TDAH"), 
        # puxamos tudo e contabilizamos via Python para garantir precisão
        todos_pacientes = Paciente.query.all()
        distribuicao_clinica = {}
        for p in todos_pacientes:
            if p.diagnostico:
                diags = [d.strip() for d in p.diagnostico.split(',')]
                for d in diags:
                    if d:
                        distribuicao_clinica[d] = distribuicao_clinica.get(d, 0) + 1
            else:
                distribuicao_clinica["Em Investigação"] = distribuicao_clinica.get("Em Investigação", 0) + 1

        # Prepara para o formato do gráfico do Chart.js
        grafico_diagnosticos = {
            "labels": list(distribuicao_clinica.keys()),
            "data": list(distribuicao_clinica.values())
        }

        # 3. Taxa de Assiduidade (Últimos 30 dias)
        hoje = datetime.utcnow() - timedelta(hours=3)
        trinta_dias_atras = hoje - timedelta(days=30)

        sessoes_periodo = Consulta.query.filter(
            Consulta.data_hora >= trinta_dias_atras,
            Consulta.data_hora <= hoje,
            Consulta.status.in_(['Realizado', 'Falta', 'Cancelado'])
        ).all()

        total_sessoes = len(sessoes_periodo)
        realizadas = sum(1 for s in sessoes_periodo if s.status == 'Realizado')
        faltas = sum(1 for s in sessoes_periodo if s.status in ['Falta', 'Cancelado'])

        # Evita divisão por zero
        taxa_assiduidade = 0
        if total_sessoes > 0:
            taxa_assiduidade = round((realizadas / total_sessoes) * 100, 1)

        # 4. Consultas da Semana (Previsão de Carga de Trabalho)
        inicio_semana = hoje - timedelta(days=hoje.weekday()) # Segunda-feira
        fim_semana = inicio_semana + timedelta(days=6, hours=23, minutes=59) # Domingo

        carga_semana = Consulta.query.filter(
            Consulta.data_hora >= inicio_semana,
            Consulta.data_hora <= fim_semana,
            Consulta.status != 'Cancelado'
        ).count()

        return jsonify({
            "total_pacientes": total_pacientes,
            "taxa_assiduidade": taxa_assiduidade,
            "total_sessoes_30d": total_sessoes,
            "sessoes_realizadas": realizadas,
            "sessoes_faltas": faltas,
            "carga_semana": carga_semana,
            "grafico_diagnosticos": grafico_diagnosticos
        }), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500