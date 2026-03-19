# 🚀 APP-TO | Sistema Integrado de Terapia Ocupacional Pediátrica

**Versão:** 1.0.0 (Produção)
**Direção Clínica:** Edna Nogueira
**Arquitetura e Engenharia:** William 

---

## 🎯 1. Visão Executiva e Produto
O **APP-TO** é uma plataforma *HealthTech* de vanguarda desenhada exclusivamente para as necessidades da Terapia Ocupacional Pediátrica. Ao contrário de sistemas de gestão genéricos, o APP-TO espelha o fluxo clínico real, unindo gestão de prontuários a um **Motor de Inteligência Preditiva** focado no desenvolvimento neuropsicomotor infantil.

A interface foi projetada com foco absoluto em UX/UI Médico (Padrão *Clean & Calm*), utilizando a arquitetura **Split-View** para reduzir a fadiga visual do terapeuta e otimizar a leitura do dossiê do paciente.

---

## 🧬 2. Fundamentação Científica (O Motor Híbrido)
A grande inovação do APP-TO reside no cruzamento de dados entre o esforço diário e a avaliação global, utilizando padrões de ouro da reabilitação mundial:

1. **Escala PEDI (Pediatric Evaluation of Disability Inventory):** Utilizada como o marco temporal macro (avaliações trimestrais/semestrais) para documentar a capacidade funcional nas áreas de Autocuidado, Mobilidade e Função Social.
2. **Escala GAS (Goal Attainment Scaling):** Implementada no Módulo de Evolução Diária. Em vez de registos binários ("conseguiu/não conseguiu"), o sistema rastreia o desempenho da sessão numa escala de -2 a +2. 
3. **Inteligência Clínica (Roadmap):** O acúmulo estruturado (Data Lake) da Escala GAS permite ao sistema gerar "Alertas de Prontidão" para reavaliação do PEDI e, no futuro, treinar modelos de *Machine Learning* para previsibilidade de alta terapêutica.

---

## 🏗️ 3. Arquitetura Técnica (Stack)
O sistema foi construído sob uma arquitetura monolítica moderna, garantindo máxima velocidade, Risco Zero de perda de dados e escalabilidade em nuvem.

* **Backend:** Python 3.11 + Flask (Leve, rápido e seguro)
* **Banco de Dados:** PostgreSQL hospedado na plataforma Neon Serverless.
* **ORM (Mapeamento de Dados):** SQLAlchemy com uso estratégico de colunas `JSONB` (Buracos Negros) para permitir questionários clínicos dinâmicos sem alterar a estrutura do banco.
* **Frontend:** HTML5 responsivo renderizado pelo lado do servidor (Jinja2).
* **Estilização UI:** Tailwind CSS (para o design *Premium Health* centralizado).
* **Reatividade:** Alpine.js (para o motor de busca e interações em tempo real sem a lentidão de frameworks pesados).
* **Hospedagem:** Render Cloud Platform (Deploy contínuo via Git).

---

## 🏥 4. Módulos Clínicos (O Quarteto Fantástico)
O Prontuário do Paciente é o coração do sistema, dividido em 4 pilares de intervenção:

1. **Triagem Inicial (Anamnese):** Captura a história pregressa, mapeando Alertas Sensoriais, Comportamentais e AVDs. Gera automaticamente o "Mapa Clínico Visual" no ecrã principal.
2. **Avaliação PEDI:** Regista os scores quantitativos do paciente e desenha gráficos longitudinais automáticos.
3. **Observação Clínica:** Módulo qualitativo e estruturado para registo das funções executivas e processamento sensorial na prática.
4. **Evolução Diária (Em Atualização):** O diário de bordo do terapeuta, integrado à Escala GAS, para medir o esforço e avanço sessão a sessão.

---

## 🔐 5. Protocolo de Segurança e Risco Zero
* **Migrações Seguras:** Nenhuma coluna do banco de dados é apagada (`drop`) durante atualizações. O sistema utiliza comandos silenciosos de `ALTER TABLE` no arranque para adaptar tabelas antigas às novas lógicas, garantindo 100% de integridade aos prontuários históricos.
* **Backup Inteligente:** Um script interno (`gerar_backup.py`) automatiza a compressão de todo o código-fonte com carimbo de tempo (Timestamp), eliminando redundâncias locais.

---
*Documento gerado para uso oficial da Direção Clínica e Engenharia do APP-TO.*