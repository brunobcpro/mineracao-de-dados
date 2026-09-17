#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Reescrita Integral do Artigo Científico com Linguagem Direta e Acessível
Projeto: Mineração de Dados para Previsão da Inflação (IPCA)
Arquivo gerado: Artigo/Artigo_Previsao_Inflacao_v6_Direto.docx
"""

import os
import shutil
import docx
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_ARTIGO = os.path.join(BASE_DIR, 'Artigo')
DIR_GRAFICOS = os.path.join(BASE_DIR, 'Entrega_Classroom', '4_Graficos_Alta_Resolucao')
DOC_ORIGEM = os.path.join(DIR_ARTIGO, 'Artigo_Previsao_Inflacao_v5_Atual.docx')

# Carregar documento original para recuperar dados das tabelas existentes (Tabela 1 e Tabela 3)
doc_orig = Document(DOC_ORIGEM)
tbl_inventario_orig = doc_orig.tables[0]
tbl_final_orig = doc_orig.tables[2]

# Extrair linhas da Tabela 1 (Inventário)
dados_tabela_1 = []
for row in tbl_inventario_orig.rows[1:]:
    dados_tabela_1.append([c.text.strip() for c in row.cells])

# Extrair linhas da Tabela 3 (Dicionário Final)
dados_tabela_3 = []
for row in tbl_final_orig.rows[1:]:
    dados_tabela_3.append([c.text.strip() for c in row.cells])

print(f"Extraídas {len(dados_tabela_1)} linhas da Tabela 1 e {len(dados_tabela_3)} linhas da Tabela 3.")

# Criar novo documento limpo
doc = Document()

# Configurações de margens (A4, 2.5 cm / ~1 polegada)
for sec in doc.sections:
    sec.top_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.left_margin = Inches(1.0)
    sec.right_margin = Inches(1.0)

# Helpers de Formatação
def add_p(text="", bold_prefix="", font_size=11.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=5, heading_level=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = align
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.15
    
    if heading_level == 1:
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.space_before = Pt(16)
        pf.space_after = Pt(6)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(13)
        r.bold = True
        return p
    elif heading_level == 2:
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.space_before = Pt(13)
        pf.space_after = Pt(5)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.bold = True
        return p
    elif heading_level == 3:
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.space_before = Pt(10)
        pf.space_after = Pt(4)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(11.5)
        r.bold = True
        return p
        
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = "Arial"
        r_bold.font.size = Pt(font_size)
        r_bold.bold = True
        
    if text:
        r_text = p.add_run(text)
        r_text.font.name = "Arial"
        r_text.font.size = Pt(font_size)
        
    return p

def add_img(img_name, caption_text, width=Inches(5.5)):
    img_path = os.path.join(DIR_GRAFICOS, img_name)
    p_img = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=7, space_after=3)
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=width)
    
    p_cap = add_p(text=caption_text, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=6)
    p_cap.runs[0].font.size = Pt(9.5)
    p_cap.runs[0].italic = True

def helper_format_cell(cell, text, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex=None, width=None):
    if width:
        cell.width = width
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', 70), ('bottom', 70), ('left', 80), ('right', 80)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)
    
    if bg_hex:
        shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_hex}"/>')
        tcPr.append(shading)
        
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(9.0)
    r.bold = bold

print("Construindo cabeçalho e título...")

# Cabeçalho Institucional
add_p(text="FACULDADE POLI-UPE | ESCOLA POLITÉCNICA DE PERNAMBUCO", bold_prefix="", font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
add_p(text="DISCIPLINA: MINERAÇÃO DE DADOS", bold_prefix="", font_size=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)

# Título do Artigo
p_tit = add_p(text="Previsão da Inflação Brasileira (IPCA) por Mineração de Séries Temporais: Uma Abordagem Comparativa entre Modelos Univariados e Multivariados Híbridos", font_size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
p_tit.runs[0].bold = True

add_p(text="Bruno Protásio | Equipe de Pesquisa em Engenharia e Ciência de Dados", font_size=10.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=16)

# =============================================================================
# 1. INTRODUÇÃO DO PROJETO
# =============================================================================
print("Escrevendo Seção 1 (Introdução)...")
add_p(text="1. Introdução do Projeto", heading_level=1)

add_p(bold_prefix="Tema Central: ",
      text="Este projeto investiga a capacidade de previsão da inflação brasileira (IPCA) utilizando técnicas de mineração de séries temporais. Confrontamos duas estratégias: a abordagem univariada (que prevê o IPCA baseando-se apenas em seu próprio histórico) e a abordagem multivariada (que combina o histórico da inflação a variáveis macroeconômicas externas, como taxa Selic, câmbio, atividade econômica, emprego e combustíveis). Nosso objetivo é responder se a inclusão de dados externos traz ganho real de acurácia e quais indicadores econômicos são mais determinantes para antecipar a trajetória dos preços no Brasil.",
      space_after=5)

add_p(text="A estabilidade de preços é essencial para a economia brasileira. A inflação corrói a renda das famílias, eleva os custos operacionais das empresas e aumenta as incertezas financeiras do país. O Índice Nacional de Preços ao Consumidor Amplo (IPCA), calculado mensalmente pelo IBGE, é o balizador oficial do regime de metas de inflação do Banco Central do Brasil. Por essa razão, antecipar o comportamento desse índice com precisão é uma necessidade crítica para a formulação de políticas públicas e para o planejamento financeiro corporativo.", space_after=5)

add_p(text="1.1 Contextualização", heading_level=2)
add_p(text="No regime de metas de inflação, o Banco Central utiliza a taxa básica de juros (Selic) para conter pressões de preços. Como as decisões de juros levam entre 6 e 12 meses para surtir efeito pleno na economia, ter projeções de inflação confiáveis e tempestivas é pré-requisito fundamental para decisões assertivas.", space_after=4)

add_p(text="A relevância da previsão da inflação sob a ótica da Mineração de Dados desdobra-se em três pilares práticos:", space_after=4)
add_p(bold_prefix="• Setor Público e Regulatório: ", text="Permite ancorar expectativas de mercado e avaliar o cumprimento das metas oficiais do Conselho Monetário Nacional (CMN);", space_after=3)
add_p(bold_prefix="• Empresas e Mercado Financeiro: ", text="Suporta a precificação de contratos de longo prazo, a gestão de estoques, orçamentos corporativos e ativos atrelados à inflação (como NTN-B e debêntures);", space_after=3)
add_p(bold_prefix="• Pesquisa e Ciência de Dados: ", text="Oferece um ambiente real e rigoroso para testar se modelos complexos de aprendizado de máquina compensam o aumento da dimensionalidade frente a modelos temporais parcimoniosos.", space_after=5)

add_p(text="1.2 Descrição do Problema", heading_level=2)
add_p(text="A previsão da inflação enfrenta um dilema clássico de mineração de dados: avaliar se os preços são guiados principalmente por sua própria inércia temporal ou se a inclusão de fatores externos traz sinais antecipados cruciais:", space_after=4)
add_p(bold_prefix="1. Abordagem Univariada (Apenas Histórico): ", text="Explica o IPCA unicamente por defasagens passadas e sazonalidade, partindo da premissa de que o histórico recente sintetiza as informações mais relevantes.", space_after=3)
add_p(bold_prefix="2. Abordagem Multivariada (Histórico + Fatores Externos): ", text="Combina a inércia temporal a múltiplos indicadores macroeconômicos de preços setoriais, moeda, câmbio, emprego e energia.", space_after=4)

add_p(text="Contudo, adicionar variáveis em excesso pode introduzir ruído e multicolinearidade, prejudicando os modelos. Por isso, a investigação deve responder não só se a abordagem multivariada é superior, mas quais grupos de variáveis realmente agregam valor preditivo.", space_after=4)

add_p(bold_prefix="Pergunta Central de Pesquisa: ",
      text='"A utilização de variáveis macroeconômicas exógenas melhora a acurácia da previsão do IPCA em relação a modelos puramente univariados? Quais grupos de indicadores possuem maior capacidade de antecipar a inflação brasileira?"',
      space_after=6)

add_p(text="1.3 Objetivos", heading_level=2)
add_p(text="1.3.1 Objetivo Geral", heading_level=3)
add_p(text="Desenvolver, comparar e validar modelos preditivos de mineração de dados em séries temporais para a previsão do IPCA brasileiro, confrontando o desempenho das abordagens univariada e multivariada e identificando os atributos macroeconômicos mais relevantes.", space_after=4)

add_p(text="1.3.2 Objetivos Específicos", heading_level=3)
add_p(bold_prefix="1. Engenharia de Dados: ", text="Coletar, higienizar e consolidar a série histórica mensal do IPCA e de 28 variáveis exógenas de março de 2012 a agosto de 2026 via API oficial do SGS/Banco Central;", space_after=3)
add_p(bold_prefix="2. Categorização Setorial: ", text="Agrupar as variáveis exógenas em quatro dimensões macroeconômicas: Índices de Preços, Setor Financeiro/Câmbio, Atividade/Emprego e Energia/Combustíveis;", space_after=3)
add_p(bold_prefix="3. Modelagem de Referência (Baseline): ", text="Calibrar modelos univariados clássicos (ARIMA) para estabelecer a base mínima de comparação;", space_after=3)
add_p(bold_prefix="4. Modelagem Multivariada e Híbrida: ", text="Implementar modelos lineares (ARIMAX, Lasso) e arquiteturas híbridas (ARIMAX + Random Forest) que modelam conjuntamente a tendência linear e os resíduos não lineares;", space_after=3)
add_p(bold_prefix="5. Seleção Inteligente de Atributos: ", text="Aplicar meta-heurísticas bioinspiradas (Algoritmo Genético - GA e Otimização por Enxame de Partículas - PSO) para encontrar os subconjuntos ótimos de variáveis;", space_after=3)
add_p(bold_prefix="6. Validação Temporal Walk-Forward: ", text="Avaliar as previsões com divisão sequencial 80% treino e 20% teste em horizonte de 1 passo à frente, prevenindo rigorosamente o vazamento de dados futuros (lookahead bias).", space_after=6)

add_p(text="1.4 Justificativa e Impacto", heading_level=2)
add_p(text="Compreender a previsibilidade da inflação contribui diretamente para a redução de riscos econômicos no país. Para os agentes econômicos, antecipar variações nos preços viabiliza decisões financeiras conscientes e reduz custos de incerteza. Para a ciência de dados, este projeto preenche uma lacuna prática ao comparar sistematicamente modelos lineares e não lineares sob rigoroso esquema de validação walk-forward em uma economia emergente caracterizada por volatilidade e choques exógenos frequentes.", space_after=5)

add_p(text="1.5 Escopo Negativo", heading_level=2)
add_p(text="Para manter o foco metodológico, este trabalho delimita claramente o que não faz parte do seu escopo:", space_after=4)
add_p(bold_prefix="• Previsões em Alta Frequência: ", text="O estudo analisa dados mensais e não desenvolve previsões diárias ou intradiárias de preços;", space_after=3)
add_p(bold_prefix="• Análise Microeconômica Individual: ", text="Não são avaliadas cestas de consumo de indivíduos ou domicílios específicos;", space_after=3)
add_p(bold_prefix="• Recomendação de Políticas Públicas: ", text="O objetivo é puramente preditivo e comparativo, sem proposição prescritiva de política monetária.", space_after=6)

# =============================================================================
# 2. FUNDAMENTAÇÃO TEÓRICA E TRABALHOS RELACIONADOS
# =============================================================================
print("Escrevendo Seção 2 (Fundamentação Teórica)...")
add_p(text="2. Fundamentação Teórica e Trabalhos Relacionados", heading_level=1)

add_p(text="2.1 Dinâmica Macroeconômica da Inflação no Brasil", heading_level=2)
add_p(text="A dinâmica dos preços no Brasil é orientada por três canais fundamentais: (i) a inércia inflacionária, que propaga variações passadas por contratos indexados; (ii) os choques de oferta e custos, com destaque para a oscilação do dólar (repasse cambial) e cotações de commodities energéticas; e (iii) as pressões de demanda agregada, refletidas no nível de desemprego e na atividade econômica. Essa pluralidade de estímulos justifica testar se conjuntos específicos de variáveis agregam poder preditivo superior ao simples histórico do índice.", space_after=5)

add_p(text="2.2 Mineração de Séries Temporais e Seleção de Atributos", heading_level=2)
add_p(text="Séries temporais econômicas contêm desafios particulares: tendência estocástica, quebras estruturais e relacionamentos lineares e não lineares simultâneos. Além disso, incluir dezenas de covariáveis macroeconômicas pode saturar os modelos (a chamada maldição da dimensionalidade). Por isso, o uso de meta-heurísticas de busca estocástica, como Algoritmos Genéticos (GA) e Enxame de Partículas (PSO), destaca-se na literatura como solução eficiente para identificar subconjuntos de variáveis compactos e preditivos.", space_after=5)

add_p(text="2.3 Trabalhos Relacionados", heading_level=2)
add_p(text="A literatura científica sobre modelagem da inflação organiza-se em três eixos principais:", space_after=4)
add_p(bold_prefix="1. Modelos Lineares Tradicionais: ", text="A metodologia clássica de Box e Jenkins [1] (ARIMA e SARIMA) permanece como a base de referência para capturar autocorrelação temporal e sazonalidade em séries de preços;", space_after=3)
add_p(bold_prefix="2. Arquiteturas Híbridas (Linear + Não Linear): ", text="Zhang [3] propôs a combinação entre ARIMA (para capturar a estrutura linear) e Redes Neurais / Random Forest (para modelar os resíduos não lineares), demonstrando reduções substanciais de erro em comparação a modelos isolados [4];", space_after=3)
add_p(bold_prefix="3. Meta-heurísticas na Seleção de Atributos: ", text="Estudos recentes utilizam Algoritmos Genéticos e PSO para selecionar variáveis macroeconômicas em bases de alta dimensionalidade, provando que modelos com 5 a 7 atributos bem selecionados superam modelos com todas as variáveis [5, 6].", space_after=6)

# =============================================================================
# 3. PLANEJAMENTO, GOVERNANÇA E DADOS DO PROJETO
# =============================================================================
print("Escrevendo Seção 3 (Planejamento, Dados e Dicionário 1)...")
add_p(text="3. Planejamento, Governança e Dados do Projeto", heading_level=1)

add_p(text="3.1 Stakeholders do Projeto", heading_level=2)
add_p(text="O desenvolvimento deste trabalho conecta-se a quatro grupos principais de interesse:", space_after=4)
add_p(bold_prefix="• Comunidade Acadêmica: ", text="Estudantes e pesquisadores de ciência de dados aplicados a problemas econômicos reais;", space_after=3)
add_p(bold_prefix="• Mercado Financeiro e Investidores: ", text="Gestores de fundos e analistas de risco que necessitam de projeções para títulos indexados à inflação (NTN-B/IPCA+);", space_after=3)
add_p(bold_prefix="• Setor Corporativo: ", text="Departamentos de planejamento orçamentário que utilizam projeções do IPCA para reajustes salariais e contratos de fornecimento;", space_after=3)
add_p(bold_prefix="• Setor Público: ", text="Órgãos governamentais e formuladores de políticas públicas que monitoram a evolução de preços.", space_after=6)

add_p(text="3.2 Base de Dados e Contextualização Macroeconômica", heading_level=2)
add_p(text="A base de dados empírica foi construída por meio da coleta automatizada de séries temporais oficiais disponibilizadas na API pública do Sistema Gerenciador de Séries Temporais do Banco Central (SGS/BACEN). O horizonte histórico abrange observações mensais contínuas (frequência Month Start - MS) de março de 2012 a agosto de 2026, totalizando 174 meses sem lacunas amostrais.", space_after=5)

add_p(text="O conjunto de dados consolida 1 variável dependente alvo (IPCA) e 28 variáveis exógenas (preditoras), estruturadas em quatro dimensões macroeconômicas funcionais da economia brasileira:", space_after=4)
add_p(bold_prefix="• Índices de Preços e Desagregações Setoriais (11 variáveis): ", text="Subíndices do IPCA (Alimentação, Transportes, Habitação, Saúde, Vestuário, Educação e Despesas Pessoais) e índices gerais de preços (INPC, IGP-M, IGP-DI e IPC-BR);", space_after=3)
add_p(bold_prefix="• Setor Financeiro, Moeda e Câmbio (3 variáveis): ", text="Taxa básica de juros (Selic Over), taxa de câmbio média PTAX (USDBRL) e reservas internacionais;", space_after=3)
add_p(bold_prefix="• Atividade Econômica e Mercado de Trabalho (7 variáveis): ", text="PIB Mensal a preços correntes, taxa de desocupação (PNAD Contínua), salário mínimo nacional, estoques de empregos formais ativos do CAGED (Total, Agropecuária e Construção Civil) e produção física de ovos;", space_after=3)
add_p(bold_prefix="• Energia e Combustíveis (6 variáveis): ", text="Volume de refino de derivados de petróleo, consumo aparente de gasolina automotiva, consumo de óleo combustível e consumo faturado de energia elétrica (Comercial, Residencial e Total).", space_after=5)

add_p(text="Para evitar redundância de inventários no texto, a especificação técnica completa de cada variável (código SGS, unidade, teste de estacionariedade ADF e seleção por meta-heurísticas) está detalhada de forma consolidada no Dicionário de Dados Final (Tabela 2), apresentado na Seção 3.4.4 após a descrição dos procedimentos de pré-processamento.", space_after=6)

add_p(text="3.2.1 Delimitação Temporal e Justificativa Metodológica (2012 a 2026)", heading_level=3)
add_p(text="A escolha de março de 2012 como ponto inicial do painel fundamenta-se em três critérios metodológicos rigorosos:", space_after=4)
add_p(bold_prefix="1. Transição da Medição do Desemprego pelo IBGE: ", text="Em março de 2012, o IBGE implementou a Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua), substituindo a antiga Pesquisa Mensal de Emprego (PME), restrita a 6 regiões metropolitanas. Usar dados anteriores geraria quebra estrutural severa na série de emprego;", space_after=3)
add_p(bold_prefix="2. Nova Ponderação da Cesta do IPCA: ", text="Em janeiro de 2012, o IBGE atualizou os pesos de consumo com base na POF 2008-2009, alterando a composição dos gastos das famílias brasileiras;", space_after=3)
add_p(bold_prefix="3. Painel Balanceado no SGS/BACEN: ", text="Diversas séries desagregadas do Banco Central só passaram a ser apuradas de maneira contínua e sem interrupções a partir de 2012.", space_after=6)

# =============================================================================
# 3.3 ANÁLISE EXPLORATÓRIA DOS DADOS (EDA)
# =============================================================================
print("Escrevendo Seção 3.3 (Análise Exploratória e Figuras)...")
add_p(text="3.3 Análise Exploratória dos Dados e Caracterização dos Atributos", heading_level=2)
add_p(text="A análise exploratória de dados (EDA) avalia a distribuição dos valores, a presença de assimetria, a dispersão estatística e os valores extremos (outliers) da série histórica antes da calibração dos modelos preditivos. Para atender aos critérios metodológicos da disciplina, selecionamos e caracterizamos um atributo contínuo numérico primordial e um atributo categórico nominal institucionalmente fundamentado.", space_after=5)

add_p(text="3.3.1 Seleção e Justificativa dos Atributos Numérico e Nominal", heading_level=3)
add_p(bold_prefix="1. Atributo Numérico Contínuo (IPCA): ",
      text="Consiste na taxa percentual mensal de variação da inflação oficial (SGS/BACEN código 4447). Trata-se da variável dependente alvo (target, y) que os modelos irão prever.",
      space_after=3)

add_p(bold_prefix="2. Atributo Nominal Categórico (Regime de Inflação): ",
      text="Construído com base no Regime de Metas para a Inflação estipulado pelo Conselho Monetário Nacional (CMN/BACEN). Discretizamos a série mensal contínua em três classes qualitativas mutuamente exclusivas:",
      space_after=3)
add_p(bold_prefix="   • Deflação (IPCA < 0,00%): ", text="Meses com queda atípica generalizada de preços provocada por choques pontuais de demanda ou desonerações fiscais;", space_after=2)
add_p(bold_prefix="   • Meta / Estável (0,00% ≤ IPCA ≤ 0,50%): ", text="Meses compatíveis com o centro da meta oficial anualizada do BACEN (equivalente a taxas mensais de 0,25% a 0,50% a.m.);", space_after=2)
add_p(bold_prefix="   • Alta / Acima da Meta (IPCA > 0,50%): ", text="Meses com pressão inflacionária excessiva que demandam aperto de política monetária.", space_after=5)

add_p(text="3.3.2 Distribuição de Frequências e Métricas Descritivas", heading_level=3)
add_p(text="A análise da amostra atualizada (março de 2012 a agosto de 2026, com 174 meses contínuos) aponta a predominância de meses dentro da meta oficial, conforme demonstrado na Tabela 1.", space_after=4)

# Inserção da Tabela 1 (Frequência)
p_cap1 = add_p(text="Tabela 1 – Distribuição de Frequência do Atributo Nominal (Regime de Inflação)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=4)
p_cap1.runs[0].bold = True
p_cap1.runs[0].font.size = Pt(10)

dados_tab1 = [
    ["Deflação", "IPCA < 0,00%", "27", "15,52%", "27", "15,52%"],
    ["Meta / Estável", "0,00% ≤ IPCA ≤ 0,50%", "77", "44,25%", "104", "59,77%"],
    ["Alta / Acima da Meta", "IPCA > 0,50%", "70", "40,23%", "174", "100,00%"],
    ["Total Geral Amostral", "Horizonte 2012–2026", "174", "100,00%", "174", "100,00%"]
]
widths_tab1 = [Inches(1.5), Inches(1.3), Inches(0.9), Inches(0.9), Inches(0.9), Inches(1.0)]
tbl1 = doc.add_table(rows=len(dados_tab1) + 1, cols=6)
headers_tab1 = ["Classe Nominal", "Faixa Paramétrica", "Freq. Absoluta (fi)", "Freq. Relativa (%)", "Freq. Acumulada (Fi)", "Freq. Rel. Acum. (%)"]

for j, h_text in enumerate(headers_tab1):
    helper_format_cell(tbl1.rows[0].cells[j], h_text, bold=True, bg_hex="EAECEF", width=widths_tab1[j])

for i, row in enumerate(dados_tab1):
    row_cells = tbl1.rows[i + 1].cells
    is_tot = (i == len(dados_tab1) - 1)
    bg = "F2F4F7" if is_tot else None
    for j, val in enumerate(row):
        is_bold = (j == 0 or is_tot)
        align = WD_ALIGN_PARAGRAPH.LEFT if (j == 0) else WD_ALIGN_PARAGRAPH.CENTER
        helper_format_cell(row_cells[j], val, bold=is_bold, align=align, bg_hex=bg, width=widths_tab1[j])

add_p(text="Fonte: Elaboração própria com base em microdados do SGS/BACEN (2026).", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=6)

add_p(text="Principais estimadores estatísticos do IPCA contínuo na amostra:", space_after=4)
add_p(bold_prefix="• Média e Mediana: ", text="Média de 0,4324% ao mês e mediana de 0,4150% ao mês;", space_after=2)
add_p(bold_prefix="• Dispersão: ", text="Desvio padrão amostral de 0,4719% e variância de 0,2226;", space_after=2)
add_p(bold_prefix="• Assimetria e Curtose: ", text="Assimetria positiva (+0,5287), indicando cauda direita alongada por choques de alta, e curtose de +0,3736 (fracamente leptocúrtica);", space_after=2)
add_p(bold_prefix="• Valores Extremos: ", text="Mínimo histórico de -0,7400% (junho/2023) e máximo de +1,9500% (dezembro/2019);", space_after=2)
add_p(bold_prefix="• Quartis e Intervalo Interquartílico: ", text="Q1 = 0,0800%, Q3 = 0,6775% e IQR = 0,5975 p.p.", space_after=6)

add_p(text="3.3.3 Análise Visual: Histograma, Boxplot e Gráfico de Dispersão", heading_level=3)
add_p(text="Para examinar as características visuais da inflação, geramos quatro gráficos em alta resolução (300 DPI), apresentados a seguir acompanhados de suas interpretações práticas.", space_after=5)

# Figura 1
add_img("Figura_1_Histograma_IPCA.png", "Figura 1 – Histograma e Densidade Empírica (KDE) do IPCA (2012 a 2026)")
add_p(text="A Figura 1 confirma que a distribuição da inflação concentra-se entre 0,10% e 0,60% ao mês. A proximidade entre média e mediana reforça a regularidade central, enquanto a assimetria positiva (+0,53) demonstra que choques inflacionários são mais acentuados do que quedas de preço.", space_after=5)

# Figura 2
add_img("Figura_2_Boxplot_IPCA.png", "Figura 2 – Diagrama de Caixa (Boxplot) do IPCA: Amostra Global e por Regimes de Inflação")
add_p(text="O Boxplot univariado na Figura 2(A) identifica 5 outliers pelo critério de Tukey (IQR): dezembro/2019 (+1,95%), outubro/2020 (+1,72%), novembro/2020 (+1,61%), dezembro/2020 (+1,58%) e dezembro/2021 (+1,58%), correspondendo a choques de carnes e restrições de cadeias globais durante a pandemia. Na Figura 2(B), nota-se que a variabilidade da classe 'Alta' é muito mais ampla do que na classe 'Meta', justificando o emprego de modelos híbridos com aprendizado de máquina para modelar os resíduos.", space_after=5)

# Figura 3
add_img("Figura_3_Dispersao_IPCA_Cambio.png", "Figura 3 – Gráfico de Dispersão entre IPCA e Taxa de Câmbio (USDBRL) por Regime Nominal")
add_p(text="O gráfico de dispersão da Figura 3 evidencia a relação positiva entre desvalorização cambial e inflação (repasse cambial). À medida que a cotação do dólar sobe, a proporção de observações no regime de 'Alta' aumenta perceptivelmente, comprovando a relevância do câmbio como variável preditiva exógena.", space_after=5)

# Figura 4
add_img("Figura_4_Distribuicao_Regimes.png", "Figura 4 – Proporção Percentual dos Regimes Nominais de Inflação (N = 174 meses)")
add_p(text="A Figura 4 sintetiza a predominância dos regimes: 44,25% dos meses situaram-se dentro da meta, 40,23% em patamares elevados e apenas 15,52% em deflação (composta por desonerações fiscais temporárias e contrações severas de demanda).", space_after=5)

add_p(text="3.3.4 Governança, Integridade e Requisitos de Qualidade", heading_level=3)
add_p(text="O tratamento dos dados segue rigorosamente a Lei Geral de Proteção de Dados Pessoais (LGPD – Lei nº 13.709/2018). As séries temporais empregadas são dados macroeconômicos públicos e agregados (SGS/BACEN, IBGE, FGV e Ministério do Trabalho), sem identificadores individuais. Sob a perspectiva de engenharia de dados, garantimos: (i) prevenção estrita de vazamento prospectivo (lookahead bias); (ii) completude amostral de 100% sem lacunas no período de 2012 a 2026; e (iii) reprodutibilidade científica por meio de scripts Python automatizados.", space_after=6)

# =============================================================================
# 3.4 PRÉ-PROCESSAMENTO DOS DADOS E DICIONÁRIO FINAL
# =============================================================================
print("Escrevendo Seção 3.4 (Pré-processamento e Dicionário Final)...")
add_p(text="3.4 Pré-processamento dos Dados e Dicionário de Dados Final", heading_level=1)
add_p(text="O pré-processamento transforma as séries econômicas brutas em um painel equilibrado, consistente e apto a alimentar os estimadores lineares e não lineares. Esse fluxo é organizado em três etapas fundamentais: Limpeza, Redução e Transformação.", space_after=5)

add_p(text="3.4.1 Procedimentos de Limpeza e Saneamento de Dados (Data Cleaning)", heading_level=2)
add_p(bold_prefix="1. Sincronização Cronológica: ", text="Séries diárias do mercado financeiro (taxa de câmbio PTAX e taxa Selic) foram convertidas para médias mensais de dias úteis e alinhadas sob frequência contínua Month Start (MS) de março de 2012 a agosto de 2026;", space_after=3)
add_p(bold_prefix="2. Tratamento de Zeros Estruturais: ", text="Em fluxos e estoques contínuos (refino de petróleo, consumo de combustíveis, energia e estoque do CAGED), zeros espúrios causados por atrasos de declaração contábil foram substituídos por valores nulos (NaN) para não distorcer variações percentuais;", space_after=3)
add_p(bold_prefix="3. Sanitização Numérica: ", text="Valores infinitos positivos ou negativos (±inf) decorrentes de potenciais divisões aritméticas foram substituídos por NaN;", space_after=3)
add_p(bold_prefix="4. Imputação Temporal sem Vazamento de Dados: ", text="Valores faltantes foram tratados via interpolação linear temporal contínua indexada por datas (interpolate(method='time')). Para regressores de Machine Learning, qualquer imputação estatística é calibrada no treino e aplicada de forma cega no teste;", space_after=3)
add_p(bold_prefix="5. Diagnóstico de Outliers e Preservação de Choques Reais: ", text="Choques genuínos (deflação da COVID-19 em 2020 e desonerações tributárias em 2022) foram integralmente preservados para os modelos ARIMA e ARIMAX, enquanto modelos de aprendizado de máquina contam com winsorização conservadora (percentis 1% e 99% no treino) para evitar distorções espaciais nos pesos.", space_after=6)

add_p(text="3.4.2 Técnicas de Redução de Dados e Dimensionalidade (Data Reduction)", heading_level=2)
add_p(bold_prefix="1. Redução Amostral Estrutural (Truncamento pós-2012): ", text="O descarte intencional de registros anteriores a março de 2012 eliminou quebras estruturais severas da transição PME para PNAD Contínua e da reformulação da cesta da POF;", space_after=3)
add_p(bold_prefix="2. Seleção de Atributos por Meta-heurísticas (GA e PSO): ", text="Dos 27 atributos exógenos candidatos, Algoritmos Genéticos (GA) e Enxame de Partículas (PSO) selecionaram os subconjuntos ótimos de 5 variáveis-chave. No modelo campeão (ARIMAX + Random Forest), o PSO selecionou: IPCA_Transportes, IGP_DI, Produção_Derivados_Petróleo, Consumo_Gasolina e Estoque_Empregos_Formais_Total, reduzindo a dimensionalidade em mais de 80% e alcançando o menor erro do estudo (RMSE de 0,1046).", space_after=6)

add_p(text="3.4.3 Transformação de Dados e Engenharia de Atributos (Data Transformation)", heading_level=2)
add_p(bold_prefix="1. Particionamento Temporal Cronológico 80/20: ", text="A base tratada foi dividida estritamente em ordem cronológica (sem embaralhamento) em 80% para treino e 20% para teste, suportando o esquema walk-forward (previsões dinâmicas de 1 passo à frente);", space_after=3)
add_p(bold_prefix="2. Teste ADF e Estacionarização Automática: ", text="Modelos ARIMA pressupõem séries estacionárias. O teste Augmented Dickey-Fuller (ADF a 5%) confirmou que o IPCA e os subíndices de preços são I(0) (estacionários em nível). Séries com raiz unitária (como PIB, Câmbio e Combustíveis) foram submetidas à primeira diferenciação sucessiva (ΔX_t = X_t - X_{t-1}), eliminando regressão espúria;", space_after=3)
add_p(bold_prefix="3. Engenharia de Defasagens Temporais (Lags): ", text="Criamos defasagens autoregressivas de 1 a 3 meses para capturar o tempo de transmissão de decisões de juros e oscilações cambiais até os preços ao consumidor;", space_after=3)
add_p(bold_prefix="4. Padronização de Escalas via StandardScaler: ", text="Para evitar que variáveis medidas em bilhões (como PIB) dominassem atributos medidos em percentuais decimais (como IPCA e Selic), normalizou-se os dados via Z-Score com média e desvio padrão calibrados estritamente na partição de treino.", space_after=6)

add_p(text="3.4.4 Dicionário de Dados Final do Projeto", heading_level=2)
add_p(text="Como síntese de todas as etapas de saneamento, estacionarização e seleção bioinspirada, a Tabela 2 apresenta o Dicionário de Dados Final do projeto, especificando cada atributo, seu código SGS, tipo, transformação aplicada, resultado do teste ADF e função metodológica nos modelos.", space_after=5)

# Inserção da Tabela 2 (Dicionário Final)
p_cap2 = add_p(text="Tabela 2 – Dicionário de Dados Final e Especificação de Atributos Pré-Processados", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=4)
p_cap2.runs[0].bold = True
p_cap2.runs[0].font.size = Pt(10)

headers_tab2_final = ["Atributo Final", "Código SGS", "Tipo", "Transformação Aplicada", "Estacionariedade (ADF)", "Seleção / Subconjunto", "Papel Metodológico"]
widths_tab2_final = [Inches(1.2), Inches(0.55), Inches(0.55), Inches(1.2), Inches(0.85), Inches(1.05), Inches(1.6)]

tbl2_final = doc.add_table(rows=len(dados_tabela_3) + 1, cols=7)
for j, h_text in enumerate(headers_tab2_final):
    helper_format_cell(tbl2_final.rows[0].cells[j], h_text, bold=True, bg_hex="EAECEF", width=widths_tab2_final[j])

for i, row in enumerate(dados_tabela_3):
    row_cells = tbl2_final.rows[i + 1].cells
    for j, val in enumerate(row):
        is_bold = (j == 0)
        align = WD_ALIGN_PARAGRAPH.LEFT if (j == 0 or j == 6) else WD_ALIGN_PARAGRAPH.CENTER
        helper_format_cell(row_cells[j], val, bold=is_bold, align=align, width=widths_tab2_final[j])

add_p(text="Fonte: Elaboração própria com base no pipeline computacional desenvolvido (2026).", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=8)

# =============================================================================
# REFERÊNCIAS BIBLIOGRÁFICAS
# =============================================================================
print("Escrevendo Referências Bibliográficas...")
add_p(text="Referências Bibliográficas", heading_level=1)

referencias = [
    "[1] BOX, G. E.; JENKINS, G. M.; REINSEL, G. C.; LJUNG, G. M. Time Series Analysis: Forecasting and Control. 5. ed. Hoboken: John Wiley & Sons, 2015.",
    "[2] BANCO CENTRAL DO BRASIL (BACEN). Sistema Gerenciador de Séries Temporais (SGS). Disponível em: <https://www3.bcb.gov.br/sgspub/>. Acesso em: 16 set. 2026.",
    "[3] ZHANG, G. P. Time series forecasting using a hybrid ARIMA and neural network model. Neurocomputing, v. 50, p. 159–175, 2003.",
    "[4] KHANDANI, A. E.; KIM, A. J.; LO, A. W. Consumer credit-risk models via machine-learning algorithms. Journal of Banking & Finance, v. 34, n. 11, p. 2767–2787, 2010.",
    "[5] KENNEDY, J.; EBERHART, R. Particle swarm optimization. In: PROCEEDINGS OF ICNN'95 - INTERNATIONAL CONFERENCE ON NEURAL NETWORKS, v. 4, p. 1942–1948, 1995.",
    "[6] HOLLAND, J. H. Adaptation in Natural and Artificial Systems: An Introductory Analysis with Applications to Biology, Control, and Artificial Intelligence. Cambridge: MIT Press, 1992.",
    "[7] INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). Sistema Nacional de Índices de Preços ao Consumidor (SNIPC): Metodologia do IPCA e INPC. Rio de Janeiro: IBGE, 2020.",
    "[8] HYNDMAN, R. J.; ATHANASOPOULOS, G. Forecasting: Principles and Practice. 3. ed. Melbourne: OTexts, 2021.",
    "[9] HASTIE, T.; TIBSHIRANI, R.; FRIEDMAN, J. The Elements of Statistical Learning: Data Mining, Inference, and Prediction. 2. ed. New York: Springer, 2009.",
    "[10] PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, v. 12, p. 2825–2830, 2011."
]

for ref in referencias:
    p_ref = add_p(text=ref, font_size=9.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=4)
    p_ref.paragraph_format.line_spacing = 1.05

# Salvar como Artigo Principal oficial
caminho_principal = os.path.join(DIR_ARTIGO, 'Artigo_Previsao_Inflacao.docx')
caminho_entrega_artigo = os.path.join(BASE_DIR, 'Entrega_Classroom', '3_Artigo_Completo', 'Artigo_Previsao_Inflacao.docx')

doc.save(caminho_principal)
print(f"Artigo Principal salvo em: {caminho_principal}")

doc.save(caminho_entrega_artigo)
print(f"Cópia da Entrega atualizada em: {caminho_entrega_artigo}")
