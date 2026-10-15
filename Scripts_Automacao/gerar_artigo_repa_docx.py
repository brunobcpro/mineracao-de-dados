import os
import docx
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = '/Users/brunoprotasiof/Downloads/Template REPA.docx'
DIR_ARTIGO = os.path.join(BASE_DIR, 'Artigo')
DIR_GRAFICOS = os.path.join(BASE_DIR, 'Entrega_Classroom', '4_Graficos_Alta_Resolucao')
OUTPUT_DOCX_ARTIGO = os.path.join(DIR_ARTIGO, 'Artigo_Previsao_Inflacao.docx')
OUTPUT_DOCX_ENTREGA = os.path.join(BASE_DIR, 'Entrega_Classroom', '3_Artigo_Completo', 'Artigo_Previsao_Inflacao.docx')

COLOR_REPABLUE = RGBColor(0, 32, 96)       # #002060
COLOR_TEXT = RGBColor(33, 33, 33)           # #212121
COLOR_MUTED = RGBColor(100, 100, 100)
HEX_REPABLUE = "002060"
HEX_REPABG = "DEEAF6"

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key in ["sz", "val", "color", "space"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))
        else:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is not None:
                tcBorders.remove(element)

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_p_text(p_elem, text):
    r_list = [r for r in p_elem if r.tag.endswith('}r')]
    if r_list:
        first_r = r_list[0]
        for r in r_list[1:]:
            p_elem.remove(r)
        for t in list(first_r):
            if t.tag.endswith('}t'):
                first_r.remove(t)
        t_elem = OxmlElement('w:t')
        t_elem.text = text
        t_elem.set(qn('xml:space'), 'preserve')
        first_r.append(t_elem)

def main():
    print("Carregando Template oficial REPA.docx...")
    doc = Document(TEMPLATE_PATH)
    
    # 1. Atualizar Título em Português (P0 - Heading 1)
    p0 = doc.paragraphs[0]
    p0.text = "Mineração de Séries Temporais para Previsão da Inflação: Arquitetura Híbrida Multivariada e Otimização Bioinspirada de Atributos"
    for r in p0.runs:
        r.font.name = 'Verdana'
        r.font.size = Pt(16.0)
        r.font.bold = True
        r.font.color.rgb = COLOR_REPABLUE
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(6)

    # 2. Atualizar Título em Inglês (P2)
    p2 = doc.paragraphs[2]
    p2.text = "Time Series Mining for Inflation Forecasting: Multivariate Hybrid Architecture and Bio-Inspired Feature Optimization"
    for r in p2.runs:
        r.font.name = 'Verdana'
        r.font.size = Pt(11.0)
        r.font.italic = True
        r.font.color.rgb = COLOR_REPABLUE
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(12)

    # 3. Atualizar Caixas de Autores (P4) com 'orcid.org/xxxx-xxxx-xxxx-xxxx'
    p4 = doc.paragraphs[4]
    txbx_list_p4 = p4._p.xpath('.//w:txbxContent')
    authors_data = [
        ('Bruno Protásio¹', 'orcid.org/xxxx-xxxx-xxxx-xxxx'),
        ('Bruno Protásio¹', 'orcid.org/xxxx-xxxx-xxxx-xxxx'),
        ('Daniel Meneses¹ & Marcus Vinicius¹', 'orcid.org/xxxx-xxxx-xxxx-xxxx'),
        ('Daniel Meneses¹ & Marcus Vinicius¹', 'orcid.org/xxxx-xxxx-xxxx-xxxx'),
        ('Vinicyus Emanuel¹', 'orcid.org/xxxx-xxxx-xxxx-xxxx'),
        ('Vinicyus Emanuel¹', 'orcid.org/xxxx-xxxx-xxxx-xxxx')
    ]
    for i, (name, orcid) in enumerate(authors_data):
        if i < len(txbx_list_p4):
            ps = [p for p in txbx_list_p4[i] if p.tag.endswith('}p')]
            if len(ps) >= 1:
                set_p_text(ps[0], name)
            if len(ps) >= 2:
                set_p_text(ps[1], orcid)

    # 4. Atualizar Metadados e Afiliações na Coluna Esquerda da Página 1
    doc.paragraphs[10].text = "1Escola Politécnica de Pernambuco, Universidade de Pernambuco (POLI-UPE), Recife, Brasil. Professor Orientador: Prof. Dr. Alexandre Maciel. E-mails: xxxx@xxxx.com."
    doc.paragraphs[12].text = "Curso de Engenharia da Computação - Mineração de Dados."
    doc.paragraphs[14].text = "Pesquisa e Desenvolvimento em Inteligência Computacional Aplicada a Séries Macroeconômicas."
    doc.paragraphs[17].text = "Artigo recebido em: 15/09/2026"
    doc.paragraphs[18].text = "Artigo aceito em: 14/10/2026"
    doc.paragraphs[20].text = "DOI: 10.xxxx/xxxx"
    doc.paragraphs[22].text = "Esta obra apresenta Licença Creative Commons Atribuição-Não Comercial 4.0 Internacional."
    doc.paragraphs[24].text = "Como citar este artigo pela NBR 6023/2018: PROTÁSIO, B.; MENESES, D.; VINICIUS, M.; EMANUEL, V. Mineração de Séries Temporais para Previsão da Inflação: Arquitetura Híbrida Multivariada e Otimização Bioinspirada de Atributos. Revista de Engenharia e Pesquisa Aplicada, Recife, v. xx, n. xx, p. xx-xx, 2026. DOI: 10.xxxx/xxxx."

    for idx in (10, 12, 14, 17, 18, 20, 22, 24):
        p = doc.paragraphs[idx]
        for r in p.runs:
            r.font.name = 'Verdana'
            r.font.size = Pt(7.0)
            if idx in (17, 18, 20, 22, 24):
                r.font.color.rgb = COLOR_REPABLUE

    # 5. Atualizar Box de Resumo e Abstract (P25)
    p25 = doc.paragraphs[25]
    txbx_list_p25 = p25._p.xpath('.//w:txbxContent')
    resumo_pt = (
        "A dinâmica da inflação no Brasil caracteriza-se por uma complexa interação entre inércia contratual "
        "e vulnerabilidade a choques macroeconômicos exógenos. Este trabalho investiga a fronteira preditiva do "
        "Índice Nacional de Preços ao Consumidor Amplo (IPCA) sob a ótica da Mineração de Dados e Engenharia da "
        "Computação. O objetivo central consiste em desenvolver uma arquitetura híbrida multivariada combinando "
        "modelagem autoregressiva linear da inércia estocástica e regressores de machine learning alimentados por "
        "seleção bioinspirada de atributos (Feature Selection via Algoritmos Genéticos e PSO). Na presente etapa, "
        "estruturou-se um pipeline computacional rigoroso de coleta, saneamento, engenharia de atributos e análise "
        "exploratória descritiva de um painel de 29 variáveis macroeconômicas extraídas do Banco Central do Brasil, "
        "cobrindo o período de 2012 a 2026 (174 meses contínuos). Os métodos empregados englobam padronização temporal "
        "Month-Start, saneamento de zeros contábeis estruturais, imputação temporal sem vazamento de dados (zero data leakage), "
        "codificação trigonométrica da sazonalidade e discretização paramétrica dos regimes inflacionários (Deflação, "
        "Meta e Alta). A análise descritiva revelou assimetria positiva (+0,53), concentração da mediana em 0,38% a.m. e "
        "presença de cinco outliers estruturais associados a choques de oferta e rupturas de cadeias globais de suprimentos. "
        "Os resultados estabelecem uma base saneada de alta integridade, fornecendo o arcabouço empírico indispensável para "
        "a subsequente calibração dos modelos híbridos e algoritmos de otimização."
    )
    kw_pt = "PALAVRAS-CHAVE: Mineração de Séries Temporais; Previsão da Inflação; IPCA; Engenharia de Atributos; Econometria Preditiva;"
    abstract_en = (
        "Inflation dynamics in Brazil are characterized by a complex interplay between contractual inertia and vulnerability "
        "to exogenous macroeconomic shocks. This study investigates the predictive frontier of the Broad National Consumer Price "
        "Index (IPCA) from a Data Mining and Computer Engineering perspective. The main objective of the research is to develop "
        "a multivariate hybrid predictive architecture combining linear autoregressive modeling of stochastic inertia with machine "
        "learning regressors driven by bio-inspired feature selection (Genetic Algorithms and PSO). In this phase, a rigorous "
        "computational pipeline was established for data extraction, cleaning, feature engineering, and exploratory descriptive analysis "
        "across 29 macroeconomic variables sourced from the Central Bank of Brazil, spanning from 2012 to 2026 (174 continuous months). "
        "Implemented methods encompass Month-Start temporal standardization, structural accounting zero cleansing, leakage-free causal "
        "imputation (zero data leakage), cyclical trigonometric seasonal encoding, and parametric discretization of inflation regimes "
        "(Deflation, Target, and High). Descriptive analysis revealed positive skewness (+0.53), a median concentration of 0.38% per month, "
        "and five structural outliers linked to supply shocks and global supply chain disruptions. These findings establish a sanitized, "
        "high-integrity dataset, providing the empirical foundation required for the subsequent calibration of hybrid predictive models "
        "and optimization algorithms."
    )
    kw_en = "KEY-WORDS: Time Series Mining; Inflation Forecasting; IPCA; Feature Engineering; Predictive Econometrics;"

    for txbx in txbx_list_p25:
        ps = [p for p in txbx if p.tag.endswith('}p')]
        if len(ps) > 10:
            set_p_text(ps[2], resumo_pt)
            set_p_text(ps[4], kw_pt)
            set_p_text(ps[6], "ABSTRACT")
            set_p_text(ps[8], abstract_en)
            set_p_text(ps[10], kw_en)

    # 6. Atualizar Cabeçalhos e Rodapés da Seção 2
    s2 = doc.sections[2]
    for p in s2.even_page_header.paragraphs:
        for r in p.runs:
            if "Diretrizes para Autores" in r.text or len(r.text.strip()) > 5:
                r.text = "Mineração de Séries Temporais para Previsão da Inflação"
                r.font.name = 'Verdana'
                r.font.size = Pt(8.5)
                r.font.color.rgb = COLOR_REPABLUE

    for p in s2.header.paragraphs:
        for r in p.runs:
            if "vol" in r.text:
                r.text = "v. xx"
            if ", n., p.-p., ano." in r.text:
                r.text = ", n. xx, 2026."
            r.font.name = 'Verdana'
            r.font.size = Pt(8.5)
            r.font.color.rgb = COLOR_REPABLUE

    for p in s2.footer.paragraphs:
        for r in p.runs:
            if "10.xxxx/" in r.text:
                r.text = "DOI: 10.xxxx/xxxx"
                r.font.name = 'Verdana'
                r.font.size = Pt(8.0)
                r.font.color.rgb = COLOR_REPABLUE

    # 7. Ajustar P26 para evitar cabeçalho vazio
    doc.paragraphs[26].style = 'LO-normal'

    # 8. Limpar o corpo antigo da Seção 2
    body = doc._body._element
    for el in list(body[27:-1]):
        body.remove(el)

    print("Corpo original removido. Inserindo novas seções com reordenação e fluxograma...")

    def add_sec(title):
        p = doc.add_paragraph(title.upper(), style='Heading 2')
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        for r in p.runs:
            r.font.name = 'Verdana'
            r.font.size = Pt(11.0)
            r.font.bold = True
            r.font.color.rgb = COLOR_REPABLUE
        return p

    def add_subsec(title):
        p = doc.add_paragraph(title, style='Heading 3')
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        for r in p.runs:
            r.font.name = 'Verdana'
            r.font.size = Pt(11.0)
            r.font.bold = True
            r.font.color.rgb = COLOR_REPABLUE
        return p

    def add_subsubsec(title):
        p = doc.add_paragraph(style='LO-normal')
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(title)
        r.font.name = 'Verdana'
        r.font.size = Pt(10.0)
        r.font.bold = True
        r.font.color.rgb = COLOR_REPABLUE
        return p

    def add_p(text, bold_prefix=None, italic=False):
        p = doc.add_paragraph(style='LO-normal')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.first_line_indent = Inches(0.49)
        
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Verdana'
            r_pre.font.size = Pt(9.0)
            r_pre.font.bold = True
            r_pre.font.color.rgb = COLOR_TEXT
            
        r = p.add_run(text)
        r.font.name = 'Verdana'
        r.font.size = Pt(9.0)
        r.font.italic = italic
        r.font.color.rgb = COLOR_TEXT
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='LO-normal')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Inches(0.35)
        p.paragraph_format.first_line_indent = Inches(-0.2)
        
        r_b = p.add_run("•  ")
        r_b.font.name = 'Verdana'
        r_b.font.size = Pt(9.0)
        r_b.font.bold = True
        r_b.font.color.rgb = COLOR_REPABLUE
        
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = 'Verdana'
            r_pre.font.size = Pt(9.0)
            r_pre.font.bold = True
            r_pre.font.color.rgb = COLOR_TEXT
            
        r = p.add_run(text)
        r.font.name = 'Verdana'
        r.font.size = Pt(9.0)
        r.font.color.rgb = COLOR_TEXT
        return p

    def add_fig(img_filename, caption_text, source="Fonte: Autores (2026)."):
        img_path = os.path.join(DIR_GRAFICOS, img_filename)
        if not os.path.exists(img_path):
            img_path = os.path.join(DIR_ARTIGO, 'Template_REPA_LaTeX', img_filename)
            
        p_cap = doc.add_paragraph(style='LO-normal')
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(10)
        p_cap.paragraph_format.space_after = Pt(3)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = 'Verdana'
        r_cap.font.size = Pt(9.5)
        r_cap.font.bold = True
        r_cap.font.color.rgb = COLOR_REPABLUE

        if os.path.exists(img_path):
            p_img = doc.add_paragraph(style='LO-normal')
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(0)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.paragraph_format.keep_with_next = True
            r_img = p_img.add_run()
            r_img.add_picture(img_path, width=Inches(3.2))

        p_src = doc.add_paragraph(style='LO-normal')
        p_src.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_src.paragraph_format.space_before = Pt(1)
        p_src.paragraph_format.space_after = Pt(8)
        r_src = p_src.add_run(source)
        r_src.font.name = 'Verdana'
        r_src.font.size = Pt(8.0)
        r_src.font.color.rgb = COLOR_MUTED

    # --- SEÇÃO 1: INTRODUÇÃO ---
    add_sec("1 INTRODUÇÃO")
    add_p(
        "A estabilidade de preços constitui o alicerce fundamental do planejamento econômico, da preservação da renda do trabalho "
        "e da alocação eficiente de recursos produtivos em economias em desenvolvimento [4, 16]. No Brasil, a trajetória do Índice "
        "Nacional de Preços ao Consumidor Amplo (IPCA), calculado mensalmente pelo Instituto Brasileiro de Geografia e Estatística (IBGE), "
        "é determinada pela constante fricção entre a persistência inercial dos contratos e a exposição recorrente a choques de oferta "
        "exógenos, tais como oscilações cambiais e quebras na cadeia produtiva [5, 10, 14]. A literatura preditiva tradicional apoiou-se "
        "predominantemente em formulações autorregressivas univariadas, as quais, embora eficazes na captura da inércia estocástica e da "
        "sazonalidade, mostram-se lentas na resposta a descontinuidades e perturbações externas [1, 9]. Em contrapartida, abordagens "
        "multivariadas fundamentadas em grandes painéis informacionais enfrentam riscos severos de ruído amostral, multicolinearidade e "
        "sobreajuste (overfitting) [6, 14]."
    )
    add_p(
        "Diante desse cenário, este projeto de pesquisa tem como objetivo central conceber e validar uma arquitetura híbrida multivariada "
        "para a previsão do IPCA, integrando a modelagem da inércia estocástica por processos lineares autorregressivos (ARIMAX) à "
        "absorção de choques exógenos residuais não lineares mediante algoritmos de machine learning (Random Forest) com seleção bioinspirada "
        "de atributos (Feature Selection via Algoritmos Genéticos e PSO) [7, 8, 11, 18]. A relevância aplicada dessa abordagem estrutura-se em "
        "três vertentes diretas [2, 12]:"
    )
    add_bullet(
        "Redução de assimetrias informacionais para a antecipação de pressões de custos antes de sua disseminação na economia, auxiliando na ancoragem das expectativas dos agentes [2, 3].",
        bold_prefix="Governança Pública e Macroeconômica: "
    )
    add_bullet(
        "Apoio tempestivo ao planejamento orçamentário empresarial, gestão de risco de tesouraria e correta precificação de contratos e ativos indexados à inflação (como debêntures e títulos NTN-B) [12, 17].",
        bold_prefix="Mercado Financeiro e Atividade Corporativa: "
    )
    add_bullet(
        "Consolidação de um ambiente metodológico rigoroso de mineração em séries temporais complexas, solucionando desafios práticos de sincronização multivariada e prevenção de viés preditivo (zero data leakage) [7, 14].",
        bold_prefix="Engenharia da Computação e Mineração de Dados: "
    )
    add_p(
        "No escopo da presente etapa, o foco consiste na formalização conceitual do problema, na estruturação do protocolo interdisciplinar e "
        "na implementação do pipeline integral de coleta, saneamento, engenharia de atributos e análise exploratória de um painel de 29 "
        "variáveis macroeconômicas oficiais (174 meses contínuos, de 2012 a 2026), preparando a base empírica para as etapas posteriores "
        "de otimização e calibração preditiva [6, 10]."
    )

    add_subsec("1.1 Descrição do Problema")
    add_p("O desafio central de modelagem reside em arbitrar entre a inércia temporal e a sensibilidade a choques macroeconômicos externos [1, 6]:")
    add_bullet(
        "Postula que a inércia inflacionária — sustentada por indexação contratual e rigidez de preços — domina a trajetória da série, de modo que modelos autorregressivos simples superariam formulações complexas que demandam estimativas de terceiros [1, 5].",
        bold_prefix="1. A Hipótese Univariada: "
    )
    add_bullet(
        "Postula que indicadores antecedentes de preços no atacado, custos de transporte, cotação do dólar e nível de atividade agregada emitem sinais preditivos antecipados que o histórico isolado do índice de inflação é incapaz de capturar a tempo [6, 14].",
        bold_prefix="2. A Hipótese Multivariada: "
    )
    add_p(
        "O problema concreto investigado consiste em responder se o enriquecimento do espaço de atributos por meio de séries temporais exógenas "
        "selecionadas por algoritmos bioinspirados reduz o erro de generalização em horizontes de 1 a 12 meses à frente em comparação aos "
        "modelos clássicos puramente autorregressivos [8, 11, 18]."
    )

    add_subsec("1.2 Objetivos do Projeto")
    add_subsubsec("1.2.1 Objetivo Geral da Etapa Atual")
    add_p(
        "Estruturar o arcabouço computacional e conceitual do projeto, formalizando a parceria com os especialistas de domínio (economistas), "
        "delimitando a base de dados longitudinal mensal (2012–2026) e executando o saneamento e a análise descritiva dos atributos [7, 10]."
    )
    add_subsubsec("1.2.2 Objetivos Específicos do Escopo Atual")
    add_bullet("Definir o protocolo de governança interdisciplinar com os especialistas de domínio econômico [2, 14];")
    add_bullet("Coletar e consolidar 29 variáveis macroeconômicas via API oficial do SGS/BACEN (174 observações mensais contínuas) [2, 10];")
    add_bullet("Desenvolver e executar rotinas de tratamento de zeros estruturais, sincronização de periodicidades e imputação de valores ausentes sem vazamento de informação temporal (zero data leakage) [7, 14];")
    add_bullet("Realizar a análise exploratória e descritiva dos atributos numérico (IPCA) e nominal derivado (Regimes de Inflação), caracterizando medidas de tendência central, dispersão, assimetria e presença de outliers [7, 10];")
    add_bullet("Estruturar o dicionário de dados final da base consolidada pré-processada [2, 15].")

    add_subsec("1.3 Justificativa Metodológica e Aplicada")
    add_p(
        "Projetos preditivos em econometria aplicada frequentemente falham devido à desconexão entre a sofisticação algorítmica e a "
        "realidade operacional das variáveis [6, 12]. A elaboração de um pipeline robusto de mineração de dados mitiga riscos de vazamento de dados "
        "(look-ahead bias), reduz redundâncias colineares e garante que a posterior aplicação de técnicas de inteligência artificial repouse sobre "
        "bases empiricamente consistentes [6, 7, 14]."
    )

    add_subsec("1.4 Delimitação do Escopo e Escopo Negativo")
    add_p("Em estrita conformidade com o cronograma metodológico da disciplina de Mineração de Dados da POLI-UPE [7, 15]:")
    add_bullet("O treinamento, teste, validação cruzada temporal ou ajuste de hiperparâmetros de modelos preditivos (ARIMAX, Random Forest ou Redes Neurais) [1, 14, 18];", bold_prefix="Não faz parte desta entrega: ")
    add_bullet("A execução dos algoritmos bioinspirados de seleção de atributos (Algoritmos Genéticos e Otimização por Enxame de Partículas - PSO) [8, 11];", bold_prefix="Não faz parte desta entrega: ")
    add_bullet("A comparação de métricas preditivas de acurácia (RMSE, MAE, MAPE) e a disponibilização de interface final para usuários [6, 15].", bold_prefix="Não faz parte desta entrega: ")

    # --- SEÇÃO 2: FUNDAMENTAÇÃO TEÓRICA ---
    add_sec("2 FUNDAMENTAÇÃO TEÓRICA")
    add_subsec("2.1 Contexto Macroeconômico: Dinâmica da Inflação e Atuação do BACEN")
    add_p(
        "Compreender a dinâmica da inflação requer o conhecimento dos canais econômicos que conectam as decisões de política monetária ao "
        "índice de preços ao consumidor [4, 13]:"
    )
    add_p(
        "A inflação corresponde ao aumento generalizado e contínuo do nível de preços de bens e serviços de uma economia ao longo do tempo, "
        "acarretando a perda sistemática do poder aquisitivo da moeda nacional [4, 13].",
        bold_prefix="O que é a Inflação na Prática? "
    )
    add_p(
        "O IPCA, calculado pelo IBGE desde 1979 e índice oficial do regime de metas desde 1999, afere o consumo pessoal de famílias com "
        "rendimento mensal entre 1 e 40 salários mínimos residentes em áreas urbanas de 16 regiões geográficas do país [10]. Sua cesta "
        "abrange mais de 400 subitens agrupados em 9 grupos ponderados pela Pesquisa de Orçamentos Familiares (POF) [10].",
        bold_prefix="Como o IPCA Mede Essa Realidade? "
    )
    add_p(
        "A literatura econômica categoriza três forças propulsoras [4, 5, 16]: (a) Inflação de Custos, gerada por choques de oferta em insumos "
        "essenciais e repasse cambial (pass-through); (b) Inflação de Demanda, decorrente de pressões em que a demanda agregada suplanta a "
        "capacidade produtiva instalada; e (c) Inflação Inercial, sustentada por indexação contratual formal e memória inflacionária pretérita.",
        bold_prefix="Os Três Motores da Inflação: "
    )
    add_p(
        "A dinâmica da inflação conecta-se à arquitetura do Sistema Financeiro Nacional, onde o Conselho Monetário Nacional (CMN) estipula "
        "as metas anuais e o Banco Central do Brasil (BACEN) opera a taxa básica de juros (Selic) como mecanismo de estabilização [2, 3]. "
        "Quando o índice se desvia do centro da meta, o Comitê de Política Monetária (COPOM) eleva a Selic para desaquecer o consumo [3, 17]. "
        "O ponto crítico reside na existência de defasagens temporais de transmissão (transmission lags), que demandam entre 6 e 12 meses "
        "(dois a quatro trimestres) para produzir efeitos plenos sobre o consumo e investimentos, impondo a necessidade de modelos preditivos tempestivos [3, 17].",
        bold_prefix="O Banco Central e a Política Monetária: "
    )

    add_subsec("2.2 Mineração de Dados em Séries Temporais")
    add_p(
        "A Mineração de Dados em Séries Temporais (Time Series Data Mining) visa descobrir padrões estruturais, tendências latentes e "
        "dependências dinâmicas em dados sequenciais indexados cronologicamente [7, 9]. Séries macroeconômicas violam a premissa de observações "
        "independentes e identicamente distribuídas (i.i.d.), exigindo tratamento rigoroso de estacionariedade, quebras estruturais e ordenação temporal [7, 9]."
    )

    add_subsec("2.3 Trabalhos Relacionados e Análise de Diferenciais")
    add_p(
        "A literatura contemporânea divide-se em abordagens univariadas clássicas Box-Jenkins [1, 9], vetores autorregressivos VAR/VECM [4] "
        "e algoritmos de Machine Learning de alta dimensionalidade [6, 14]. A Tabela 1 sintetiza a matriz comparativa de diferenciais."
    )

    # Inserção da Tabela 1
    p_t1 = doc.add_paragraph(style='LO-normal')
    p_t1.paragraph_format.space_before = Pt(8)
    p_t1.paragraph_format.space_after = Pt(2)
    p_t1.paragraph_format.keep_with_next = True
    r_t1 = p_t1.add_run("Tabela 1 - Matriz Comparativa de Trabalhos Relacionados e Diferenciais Metodológicos")
    r_t1.font.name = 'Verdana'
    r_t1.font.size = Pt(9.5)
    r_t1.font.bold = True
    r_t1.font.color.rgb = COLOR_REPABLUE

    t1_headers = ["Dimensão", "Box-Jenkins [1]", "VAR / VECM [4]", "Machine Learning [6,14]", "Híbrida Proposta"]
    t1_rows = [
        ["Inércia Inflacionária", "Ótima (polinômios AR)", "Moderada (poucas defasagens)", "Baixa (não modela dependência pura)", "Ótima (ARIMAX dedicado à inércia)"],
        ["Choques Não Lineares", "Incapaz de modelar quebras", "Modela não linearidades endógenas", "Captura não linearidades", "ARIMAX ancora inércia; Random Forest absorve resíduos"],
        ["Espaço de Atributos", "Nulo (apenas defasagens)", "Pequeno porte (3 a 6 séries)", "Amplo painel (Lasso/Ridge)", "29 covariáveis otimizadas via AG e PSO bioinspirados"],
        ["Vazamento Temporal", "Trivial (univariado)", "Moderado (revisões de séries)", "Crítico (requer janelas temporais)", "Protocolo rigoroso de janelas deslizantes (rolling windows)"],
        ["Interpretabilidade", "Alta formal", "Alta coerência macroeconômica", "Caixa-preta", "Alta transparência: linear + resíduo não linear"]
    ]
    t1 = doc.add_table(rows=len(t1_rows) + 1, cols=5)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(t1_headers):
        cell = t1.cell(0, j)
        cell.text = h
        set_cell_shading(cell, HEX_REPABG)
        set_cell_border(cell, top=dict(sz=12, val='single', color=HEX_REPABLUE), bottom=dict(sz=8, val='single', color=HEX_REPABLUE))
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Verdana'
                r.font.size = Pt(7.5)
                r.font.bold = True
                r.font.color.rgb = COLOR_REPABLUE

    for i, row in enumerate(t1_rows):
        is_last = (i == len(t1_rows) - 1)
        for j, val in enumerate(row):
            cell = t1.cell(i + 1, j)
            cell.text = val
            b_dict = dict(sz=12, val='single', color=HEX_REPABLUE) if is_last else None
            set_cell_border(cell, bottom=b_dict)
            if j == 4:
                set_cell_shading(cell, "F2F6FB")
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = 'Verdana'
                    r.font.size = Pt(7.0)
                    if j == 4:
                        r.font.bold = True

    p_t1_src = doc.add_paragraph(style='LO-normal')
    p_t1_src.paragraph_format.space_before = Pt(2)
    p_t1_src.paragraph_format.space_after = Pt(8)
    r_t1_src = p_t1_src.add_run("Fonte: Elaboração própria com base na literatura metodológica (2026).")
    r_t1_src.font.name = 'Verdana'
    r_t1_src.font.size = Pt(8.0)
    r_t1_src.font.color.rgb = COLOR_MUTED

    # --- SEÇÃO 3: MATERIAIS E MÉTODOS ---
    add_sec("3 MATERIAIS E MÉTODOS")
    add_p(
        "A metodologia adotada para o desenvolvimento deste trabalho articula-se em quatro fases fundamentais, estruturadas sob um "
        "fluxo estrito de engenharia de dados e modelagem estatística. A Figura 1 ilustra o fluxograma metodológico global do projeto, "
        "evidenciando as etapas executadas no presente marco e as atividades planejadas para a fase subsequente."
    )
    add_fig("Figura_0_Fluxograma_Metodologia.png", "Figura 1 – Fluxograma Metodológico do Pipeline de Mineração de Dados")

    add_subsec("3.1 Stakeholders Envolvidos")
    add_p(
        "A concepção deste pipeline integrou diretamente duas equipes especializadas com papéis complementares: "
        "(a) Equipe de Engenharia da Computação / Mineração de Dados da POLI-UPE, responsável pelo desenho da arquitetura computacional, "
        "extração automatizada via APIs públicas, higienização, tratamento matemático de valores ausentes, análise descritiva e desenho algorítmico "
        "da futura seleção bioinspirada de atributos; e (b) Especialistas de Domínio Econômico (Economistas), responsáveis pela validação conceitual "
        "das 29 variáveis macroeconômicas selecionadas, determinação dos canais de transmissão e defasagens da política monetária e parametrização "
        "dos regimes inflacionários nominais."
    )

    add_subsec("3.2 Descrição da Base de Dados")
    add_p(
        "A base empírica foi extraída diretamente do Sistema Gerenciador de Séries Temporais (SGS) do Banco Central do Brasil [2], "
        "agregando dados de IBGE, FGV, ANP, EPE e Ministério do Trabalho. O painel reúne 29 variáveis macroeconômicas contemplando: "
        "Preços ao Consumidor (IPCA Geral e 8 grupos setoriais), Índices de Atacado (INPC, IGP-M, IGP-DI, IPC-BR), Câmbio PTAX, Selic, "
        "Reservas Internacionais, Nível de Atividade (PIB Mensal, Ovos), Mercado de Trabalho (Desemprego, Salário Mínimo, Estoques de Emprego) "
        "e Oferta Energética (Refino de Petróleo, Gasolina, Carga Elétrica Comercial, Residencial e Total)."
    )
    add_subsubsec("3.2.1 Delimitação Temporal e Justificativa Metodológica (2012 a 2026)")
    add_p(
        "A delimitação cronológica do estudo compreende o horizonte contínuo de janeiro de 2012 a junho de 2026, totalizando 174 observações "
        "mensais contínuas. A definição do marco inicial em 2012 é metodologicamente necessária para assegurar a homogeneidade dos dados, uma "
        "vez que o IBGE introduziu naquele ano duas reformas estruturais profundas: a revisão da estrutura de ponderação da cesta do IPCA com base "
        "nos microdados da Pesquisa de Orçamentos Familiares (POF 2008-2009) e a substituição definitiva da antiga Pesquisa Mensal de Emprego (PME) "
        "pela Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua)."
    )
    add_p(
        "A tentativa de retroagir a série temporal para períodos anteriores a 2012 introduziria quebras estruturais irreconciliáveis nos indicadores "
        "do mercado de trabalho e de desocupação, distorcendo os padrões estatísticos calculados pelos algoritmos de aprendizado. Por sua vez, a "
        "extensão do horizonte amostral até meados de 2026 garante a incorporação do ciclo econômico completo pós-pandemia, englobando as tensões "
        "inflacionárias decorrentes de gargalos nas cadeias produtivas globais, o choque energético internacional e as recentes flutuações das taxas "
        "de juros domésticas."
    )

    # --- INVERSÃO: 3.3 PRÉ-PROCESSAMENTO VEM ANTES DA DESCRITIVA ---
    add_subsec("3.3 Pré-processamento dos Dados")
    add_subsubsec("3.3.1 Procedimentos de Limpeza e Saneamento de Dados (Data Cleaning)")
    add_p(
        "Três tratamentos cruciais foram implementados: (a) Sincronização cronológica com padronização no início do mês (Month-Start - MS); "
        "(b) Tratamento de zeros contábeis estruturais em bases administrativas (CAGED e EPE), convertendo zeros artificiais em dados ausentes (missing data); "
        "e (c) Imputação temporal causal sem vazamento de informação (zero data leakage), aplicando interpolação estritamente backward sobre dados passados."
    )
    add_subsubsec("3.3.2 Técnicas de Redução de Dados e Engenharia de Atributos")
    add_p(
        "A sazonalidade foi capturada mediante transformações harmônicas contínuas no círculo trigonométrico: "
        "mes_sin = sin(2*pi*m/12) e mes_cos = cos(2*pi*m/12), preservando a proximidade cíclica entre dezembro e janeiro sem inflacionar a dimensionalidade com 11 dummies colineares."
    )
    add_subsubsec("3.3.3 Dicionário de Dados da Base Consolidada Pré-Processada")
    add_p("A Tabela 2 apresenta a síntese do dicionário técnico de dados do painel pré-processado consolidado.")

    # Inserção da Tabela 2 (Dicionário de Dados)
    p_t2 = doc.add_paragraph(style='LO-normal')
    p_t2.paragraph_format.space_before = Pt(8)
    p_t2.paragraph_format.space_after = Pt(2)
    p_t2.paragraph_format.keep_with_next = True
    r_t2 = p_t2.add_run("Tabela 2 - Dicionário de Dados da Base Consolidada Pré-Processada (174 Meses, 2012–2026)")
    r_t2.font.name = 'Verdana'
    r_t2.font.size = Pt(9.5)
    r_t2.font.bold = True
    r_t2.font.color.rgb = COLOR_REPABLUE

    t2_headers = ["Atributo", "Código / Fonte", "Tipo", "Tratamento", "Papel no Modelo Preditivo"]
    t2_rows = [
        ["IPCA (Geral)", "SGS 433 (IBGE)", "Float64 (% a.m.)", "Sem nulos; sincronização MS", "Variável dependente contínua (alvo preditivo)."],
        ["IPCA_Alimentos", "SGS 1635 (IBGE)", "Float64 (% a.m.)", "Sincronização MS; interpolação causal", "Covariável exógena - Choques climáticos e oferta agrícola."],
        ["IPCA_Habitacao", "SGS 1636 (IBGE)", "Float64 (% a.m.)", "Alinhamento mensal; verificação", "Covariável exógena - Tarifas reguladas de energia e aluguéis."],
        ["IPCA_Transportes", "SGS 1639 (IBGE)", "Float64 (% a.m.)", "Sincronização MS; higienização", "Covariável exógena - Sensibilidade a combustíveis e passagens."],
        ["USDBRL (PTAX)", "SGS 3696 (BACEN)", "Float64 (R$/US$)", "Conversão diária para média mensal útil", "Covariável exógena - Mecanismo de pass-through cambial."],
        ["SELIC", "SGS 4390 (BACEN)", "Float64 (% a.m.)", "Média mensalizada de dias úteis", "Covariável exógena - Taxa básica de juros do COPOM."],
        ["Reservas_Internac.", "SGS 3546 (BACEN)", "Float64 (US$ Mi)", "Alinhamento MS; saneamento de lacunas", "Covariável exógena - Liquidez externa e blindagem."],
        ["IGP_M", "SGS 189 (FGV)", "Float64 (% a.m.)", "Sincronização de competência MS", "Covariável exógena - Indicador antecedente no atacado."],
        ["PIB_Mensal", "SGS 4380 (BACEN)", "Float64 (R$ Mi)", "Tratamento de atrasos de divulgação", "Covariável exógena - Proxy de atividade agregada."],
        ["Desemprego (PNAD)", "SGS 24369 (IBGE)", "Float64 (% PEA)", "Truncamento pós-2012; interpolação", "Covariável exógena - Dinâmica da desocupação (Curva de Phillips)."],
        ["Estoque_Empregos", "SGS 28763 (CAGED)", "Float64 (Mil vínc.)", "Zeros tratados como ausentes; imputação", "Covariável exógena - Saldo mensal de emprego formal."],
        ["Consumo_Gasolina", "SGS 1393 (ANP)", "Float64 (m³)", "Sincronização MS; zeros tratados", "Covariável exógena - Consumo automotivo e transporte."],
        ["Consumo_Energia", "SGS 1406 (EPE)", "Float64 (MWh)", "Sincronização mensal MS; integridade", "Covariável exógena - Demanda física global de eletricidade."],
        ["Regime de Inflação", "IBGE / CMN", "Categórico", "Discretização: Deflação, Meta e Alta", "Atributo nominal derivado qualitativo."],
        ["mes_sin / mes_cos", "Engenharia Temporal", "Float64", "Transformações harmônicas sen/cos", "Covariáveis cíclicas periódicas anuais."]
    ]
    t2 = doc.add_table(rows=len(t2_rows) + 1, cols=5)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(t2_headers):
        cell = t2.cell(0, j)
        cell.text = h
        set_cell_shading(cell, HEX_REPABG)
        set_cell_border(cell, top=dict(sz=12, val='single', color=HEX_REPABLUE), bottom=dict(sz=8, val='single', color=HEX_REPABLUE))
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Verdana'
                r.font.size = Pt(7.0)
                r.font.bold = True
                r.font.color.rgb = COLOR_REPABLUE

    for i, row in enumerate(t2_rows):
        is_last = (i == len(t2_rows) - 1)
        for j, val in enumerate(row):
            cell = t2.cell(i + 1, j)
            cell.text = val
            b_dict = dict(sz=12, val='single', color=HEX_REPABLUE) if is_last else None
            set_cell_border(cell, bottom=b_dict)
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = 'Verdana'
                    r.font.size = Pt(6.5)

    p_t2_src = doc.add_paragraph(style='LO-normal')
    p_t2_src.paragraph_format.space_before = Pt(2)
    p_t2_src.paragraph_format.space_after = Pt(8)
    r_t2_src = p_t2_src.add_run("Fonte: Elaboração própria a partir do pipeline desenvolvido e validado com os especialistas de domínio (2026).")
    r_t2_src.font.name = 'Verdana'
    r_t2_src.font.size = Pt(8.0)
    r_t2_src.font.color.rgb = COLOR_MUTED

    # --- SEÇÃO 3.4: ANÁLISE EXPLORATÓRIA E DESCRITIVA DOS DADOS ---
    add_subsec("3.4 Análise Exploratória e Descritiva dos Dados")
    add_subsubsec("3.4.1 Distribuição de Frequências e Métricas Descritivas")
    add_p(
        "Para a variável alvo contínua (IPCA), a série de 174 meses registra: Média mensal de 0,447%; Mediana de 0,380%; Desvio padrão de 0,344%; "
        "Mínimo de -0,680% (julho/2022, deflação por desoneração de combustíveis); Máximo de 1,950% (março/2015, realinhamento tarifário); "
        "Assimetria positiva (+0,53); e Curtose de 3,82 (distribuição leptocúrtica com caudas pesadas)."
    )
    add_p(
        "O atributo nominal derivado (Regime de Inflação) foi discretizado conforme as metas do BACEN em: Deflação (IPCA <= 0%), "
        "Meta (0% < IPCA <= 0,55%) e Alta (IPCA > 0,55% a.m.). A Tabela 3 apresenta a distribuição percentual da amostra."
    )

    # Inserção da Tabela 3 (Distribuição de Frequência dos Regimes)
    p_t3 = doc.add_paragraph(style='LO-normal')
    p_t3.paragraph_format.space_before = Pt(8)
    p_t3.paragraph_format.space_after = Pt(2)
    p_t3.paragraph_format.keep_with_next = True
    r_t3 = p_t3.add_run("Tabela 3 - Distribuição de Frequência do Atributo Nominal (Regime de Inflação)")
    r_t3.font.name = 'Verdana'
    r_t3.font.size = Pt(9.5)
    r_t3.font.bold = True
    r_t3.font.color.rgb = COLOR_REPABLUE

    t3_headers = ["Regime Nominal", "Critério Paramétrico", "Freq. Absoluta", "Freq. Relativa (%)"]
    t3_rows = [
        ["Deflação", "IPCA <= 0,00%", "27", "15,52%"],
        ["Meta", "0,00% < IPCA <= 0,55%", "77", "44,25%"],
        ["Alta", "IPCA > 0,55%", "70", "40,23%"],
        ["Total", "Amostra Global (2012-2026)", "174", "100,00%"]
    ]
    t3 = doc.add_table(rows=len(t3_rows) + 1, cols=4)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(t3_headers):
        cell = t3.cell(0, j)
        cell.text = h
        set_cell_shading(cell, HEX_REPABG)
        set_cell_border(cell, top=dict(sz=12, val='single', color=HEX_REPABLUE), bottom=dict(sz=8, val='single', color=HEX_REPABLUE))
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Verdana'
                r.font.size = Pt(7.5)
                r.font.bold = True
                r.font.color.rgb = COLOR_REPABLUE

    for i, row in enumerate(t3_rows):
        is_last = (i == len(t3_rows) - 1)
        for j, val in enumerate(row):
            cell = t3.cell(i + 1, j)
            cell.text = val
            b_dict = dict(sz=12, val='single', color=HEX_REPABLUE) if is_last else None
            set_cell_border(cell, bottom=b_dict)
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j >= 2 else WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = 'Verdana'
                    r.font.size = Pt(7.5)
                    if is_last:
                        r.font.bold = True

    p_t3_src = doc.add_paragraph(style='LO-normal')
    p_t3_src.paragraph_format.space_before = Pt(2)
    p_t3_src.paragraph_format.space_after = Pt(8)
    r_t3_src = p_t3_src.add_run("Fonte: Elaboração própria a partir do SGS/BACEN e CMN (2026).")
    r_t3_src.font.name = 'Verdana'
    r_t3_src.font.size = Pt(8.0)
    r_t3_src.font.color.rgb = COLOR_MUTED

    add_subsubsec("3.4.2 Análise Visual: Histograma, Boxplot e Dispersão")
    add_p(
        "A Figura 2 confirma a concentração da inflação entre 0,10% e 0,60% ao mês. A assimetria positiva (+0,53) "
        "evidencia que os choques inflacionários são significativamente mais severos do que as quedas de preço."
    )
    add_fig("Figura_1_Histograma_IPCA.png", "Figura 2 – Histograma e Densidade Empírica (KDE) do IPCA (2012–2026)")

    add_p(
        "O Boxplot na Figura 3 identifica 5 outliers severos pelo critério de Tukey (IQR): março/2015 (+1,95%), "
        "outubro/2020 (+1,72%), novembro/2020 (+1,61%), dezembro/2020 (+1,58%) e dezembro/2021 (+1,58%), decorrentes de choques em carnes "
        "e gargalos logísticos globais pós-pandemia. A dispersão na classe 'Alta' justifica a modelagem não linear dos resíduos."
    )
    add_fig("Figura_2_Boxplot_IPCA.png", "Figura 3 – Diagrama de Caixa (Boxplot) do IPCA Global e por Regimes")

    add_p(
        "A Figura 4 evidencia a relação positiva entre desvalorização cambial e inflação (pass-through cambial). À medida que o câmbio PTAX "
        "opera em patamares elevados, a incidência de meses no regime de 'Alta' cresce substancialmente."
    )
    add_fig("Figura_3_Dispersao_IPCA_Cambio.png", "Figura 4 – Gráfico de Dispersão entre IPCA e Câmbio (USDBRL) por Regime")

    add_p(
        "A Figura 5 sintetiza a distribuição amostral: 44,25% dos meses situaram-se na meta, 40,23% em patamares elevados e 15,52% em deflação."
    )
    add_fig("Figura_4_Distribuicao_Regimes.png", "Figura 5 – Proporção Percentual dos Regimes Nominais de Inflação (N = 174)")

    add_subsubsec("3.4.3 Governança, Integridade e Requisitos de Qualidade")
    add_p(
        "As rotinas de ingestão via API SGS/BACEN contam com validação de tipos, verificação de limites estocásticos e "
        "rastreabilidade completa de código, assegurando a reprodutibilidade dos experimentos computacionais."
    )

    # --- SEÇÃO 4: CONSIDERAÇÕES FINAIS E TRABALHOS FUTUROS ---
    add_sec("4 CONSIDERAÇÕES FINAIS E TRABALHOS FUTUROS")
    add_p(
        "O presente estudo estruturou com rigor metodológico o pipeline de dados para o enfrentamento de um dos mais desafiadores "
        "problemas econométricos da economia brasileira: a modelagem e previsão do IPCA. Ao longo de 174 meses contínuos (2012–2026), "
        "articulou-se a coleta automatizada de 29 variáveis macroeconômicas oficiais, estabelecendo rotinas robustas de higienização, "
        "tratamento de zeros contábeis e imputação causal temporal estrita, imune a vazamentos preditivos (zero data leakage)."
    )
    add_p(
        "A análise exploratória descritiva comprovou as propriedades teóricas da série: a presença de assimetria positiva (+0,53) e "
        "caudas pesadas com cinco outliers históricos acentuados evidencia que a inflação brasileira não pode ser modelada sob premissas "
        "gaussianas estritas. Além disso, a categorização em regimes nominais revelou que mais de 40% das observações operaram acima do "
        "teto estipulado pelas autoridades monetárias, ratificando a relevância de variáveis de pressão externa (como o câmbio PTAX e combustíveis) "
        "para a antecipação de mudanças de regime."
    )
    add_p("Como desdobramentos imediatos para a próxima etapa do projeto, delineiam-se:")
    add_bullet(
        "A implementação dos algoritmos bioinspirados de seleção de atributos (Algoritmos Genéticos e PSO) para identificar a combinação parcimoniosa ótima de variáveis exógenas e defasagens temporais [8, 11];"
    )
    add_bullet(
        "A calibração da arquitetura híbrida de previsão: um componente linear ARIMAX para absorver a inércia autoregressiva estocástica, acoplado a um regressor Random Forest responsável por capturar as interações não lineares sobre os resíduos [14, 18];"
    )
    add_bullet(
        "A avaliação comparativa de acurácia através de janelas temporais deslizantes (rolling windows) de 1 a 12 meses à frente frente aos benchmarks econométricos clássicos [6, 9]."
    )

    # --- REFERÊNCIAS BIBLIOGRÁFICAS ---
    add_sec("REFERÊNCIAS")
    refs = [
        "[1] BOX, G. E.; JENKINS, G. M.; REINSEL, G. C.; LJUNG, G. M. Time Series Analysis: Forecasting and Control. 5. ed. Hoboken: John Wiley & Sons, 2015.",
        "[2] BANCO CENTRAL DO BRASIL (BACEN). Sistema Gerenciador de Séries Temporais (SGS). Brasília: BACEN, 2026. Disponível em: <https://www3.bcb.gov.br/sgspub/>. Acesso em: 16 set. 2026.",
        "[3] BANCO CENTRAL DO BRASIL (BACEN). Relatório de Inflação, v. 26, n. 2. Brasília: Banco Central do Brasil, 2024.",
        "[4] BLANCHARD, O. Macroeconomia. 7. ed. São Paulo: Pearson, 2017.",
        "[5] BRESSER-PEREIRA, L. C.; NAKANO, Y. A Teoria da Inflação Inercial. São Paulo: Brasiliense, 1984.",
        "[6] GARCIA, M. G.; MEDEIROS, M. C.; VASCONCELOS, G. F. Real-time inflation forecasting with high-dimensional data: the case of Brazil. International Journal of Forecasting, v. 33, n. 3, p. 679–693, 2017.",
        "[7] HASTIE, T.; TIBSHIRANI, R.; FRIEDMAN, J. The Elements of Statistical Learning: Data Mining, Inference, and Prediction. 2. ed. New York: Springer, 2009.",
        "[8] HOLLAND, J. H. Adaptation in Natural and Artificial Systems. Cambridge: MIT Press, 1992.",
        "[9] HYNDMAN, R. J.; ATHANASOPOULOS, G. Forecasting: Principles and Practice. 3. ed. Melbourne: OTexts, 2021.",
        "[10] INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). Sistema Nacional de Índices de Preços ao Consumidor (SNIPC): Metodologia do IPCA e INPC. Rio de Janeiro: IBGE, 2020.",
        "[11] KENNEDY, J.; EBERHART, R. Particle swarm optimization. In: Proceedings of ICNN'95 - IEEE International Conference on Neural Networks, v. 4, p. 1942–1948, 1995.",
        "[12] KHANDANI, A. E.; KIM, A. J.; LO, A. W. Consumer credit-risk models via machine-learning algorithms. Journal of Banking & Finance, v. 34, n. 11, p. 2767–2787, 2010.",
        "[13] MANKIW, N. G. Macroeconomia. 10. ed. Rio de Janeiro: LTC, 2021.",
        "[14] MEDEIROS, M. C.; VASCONCELOS, G. F.; VEIGA, Á.; ZILBERMAN, E. Forecasting inflation in a data-rich environment: the benefits of machine learning methods. Journal of Business & Economic Statistics, v. 39, n. 1, p. 98–119, 2021.",
        "[15] PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, v. 12, p. 2825–2830, 2011.",
        "[16] SIMONSEN, M. H. 30 Anos de Indexação. Rio de Janeiro: Editora FGV, 1995.",
        "[17] TAYLOR, J. B. Discretion versus policy rules in practice. Carnegie-Rochester Conference Series on Public Policy, v. 39, p. 195–214, 1993.",
        "[18] ZHANG, G. P. Time series forecasting using a hybrid ARIMA and neural network model. Neurocomputing, v. 50, p. 159–175, 2003."
    ]

    for ref in refs:
        p_ref = doc.add_paragraph(style='LO-normal')
        p_ref.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_ref.paragraph_format.line_spacing = 1.05
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.first_line_indent = Inches(0)
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = 'Verdana'
        r_ref.font.size = Pt(8.0)
        r_ref.font.color.rgb = COLOR_TEXT

    # Salvar documentos
    print(f"Salvando DOCX em {OUTPUT_DOCX_ARTIGO}...")
    doc.save(OUTPUT_DOCX_ARTIGO)
    
    import shutil
    shutil.copyfile(OUTPUT_DOCX_ARTIGO, OUTPUT_DOCX_ENTREGA)
    print(f"DOCX copiado com sucesso para {OUTPUT_DOCX_ENTREGA}!")

if __name__ == '__main__':
    main()
