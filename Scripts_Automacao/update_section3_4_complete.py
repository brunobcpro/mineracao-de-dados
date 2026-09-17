import docx
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement

def insert_p_before(ref_paragraph, text="", bold_prefix="", font_size=11.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, heading_level=None):
    p = OxmlElement('w:p')
    ref_paragraph._p.addprevious(p)
    new_p = docx.text.paragraph.Paragraph(p, ref_paragraph._parent)
    pf = new_p.paragraph_format
    pf.alignment = align
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.15
    
    if heading_level == 2:
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.space_before = Pt(14)
        pf.space_after = Pt(5)
        r = new_p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.bold = True
        return new_p
    elif heading_level == 3:
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.space_before = Pt(11)
        pf.space_after = Pt(4)
        r = new_p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(11.5)
        r.bold = True
        return new_p
        
    if bold_prefix:
        r_bold = new_p.add_run(bold_prefix)
        r_bold.font.name = "Arial"
        r_bold.font.size = Pt(font_size)
        r_bold.bold = True
        
    if text:
        r_text = new_p.add_run(text)
        r_text.font.name = "Arial"
        r_text.font.size = Pt(font_size)
        
    return new_p

def update_docx_file(filepath):
    print(f"Processing {filepath}...")
    doc = Document(filepath)
    
    # Locate section 3.4 start and Tabela 2 caption
    idx_3_4 = None
    idx_tab2 = None
    
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip().startswith("3.4 Pré-processamento") or p.text.strip().startswith("3.4 Pré-Processamento"):
            idx_3_4 = i
        elif p.text.strip().startswith("Tabela 2 – Dicionário de Dados Final"):
            idx_tab2 = i
            
    print(f"Found idx_3_4: {idx_3_4}, idx_tab2: {idx_tab2}")
    if idx_3_4 is None or idx_tab2 is None:
        raise ValueError(f"Could not find markers in {filepath}")
        
    p_tab2 = doc.paragraphs[idx_tab2]
    old_paragraphs = doc.paragraphs[idx_3_4:idx_tab2]
    
    # Insert new content before p_tab2
    # 3.4 Heading
    insert_p_before(p_tab2, text="3.4 Pré-processamento dos Dados e Dicionário de Dados Final", heading_level=2)
    
    # Intro
    insert_p_before(p_tab2, text="O pré-processamento de dados é a etapa fundamental que transforma as séries econômicas brutas em um painel consistente, estável e apto para alimentar os modelos econométricos e de aprendizado de máquina. Em séries macroeconômicas, dados em estado bruto frequentemente violam premissas de estacionariedade, apresentam valores faltantes decorrentes de defasagens de divulgação, exibem escalas numéricas amplamente discrepantes e contêm ruídos ou zeros pontuais que mascaram o comportamento econômico real. Para assegurar a robustez estatística das estimativas e prevenir rigorosamente o vazamento de informações futuras (data leakage), estruturou-se um pipeline de preparação organizado em três eixos metodológicos sistemáticos: Limpeza (Data Cleaning), Redução (Data Reduction) e Transformação (Data Transformation), culminando na consolidação do Dicionário de Dados Final do projeto.", space_before=2, space_after=6)
    
    # 3.4.1 Limpeza e Saneamento
    insert_p_before(p_tab2, text="3.4.1 Procedimentos de Limpeza e Saneamento de Dados (Data Cleaning)", heading_level=3)
    insert_p_before(p_tab2, text="A etapa de saneamento concentrou-se na correção de falhas de registro, padronização temporal e tratamento criterioso de inconsistências empíricas:", space_before=2, space_after=5)
    
    insert_p_before(p_tab2, 
        bold_prefix="1. Sincronização Cronológica e Agregação de Frequência: ",
        text="As séries macroeconômicas coletadas junto ao Banco Central do Brasil apresentavam frequências originais heterogêneas. Séries do mercado financeiro apuradas em base diária — especificamente a taxa de câmbio PTAX (USDBRL) e a taxa de juros Over/Selic — foram convertidas para periodicidade mensal por meio da média aritmética dos dias úteis de cada mês. Em seguida, todas as 28 variáveis foram sincronizadas sob uma grade homogênea contínua na frequência Month Start (MS), estendendo-se de março de 2012 até 2026, garantindo alinhamento cronológico perfeito e sem descontinuidades amostrais no período.",
        space_before=2, space_after=5)

    insert_p_before(p_tab2, 
        bold_prefix="2. Identificação e Tratamento de Zeros Estruturais: ",
        text="Em variáveis que mensuram fluxos físicos contínuos e estoques econômicos (como volume de refino de derivados de petróleo, consumo industrial e automotivo de combustíveis, consumo de energia elétrica, reservas internacionais e estoques de emprego formal do CAGED), constatou-se a ocorrência pontual do valor numérico zero. Na economia real, tais grandezas físicas jamais atingem valor nulo; a presença de zeros decorria de atrasos pontuais no envio de declarações contábeis e retenções no processamento dos órgãos informantes. Para evitar que esses zeros artificiais gerassem distorções graves em variações percentuais ou inviabilizassem transformações logarítmicas, esses registros espúrios foram convertidos em valores nulos (NaN) para receber tratamento adequado de imputação temporal.",
        space_before=2, space_after=5)

    insert_p_before(p_tab2, 
        bold_prefix="3. Sanitização de Inconsistências Aritméticas (±∞): ",
        text="Operações matemáticas que envolvem taxas marginais de aceleração e variações percentuais podem originar valores infinitos positivos ou negativos caso ocorra divisão por valores nulos ou infinitesimais. Esses registros inconsistentes foram detectados computacionalmente e substituídos por valores nulos (replace([np.inf, -np.inf], np.nan)), impedindo que erros numéricos corrompessem os algoritmos de padronização e os estimadores de aprendizado de máquina.",
        space_before=2, space_after=5)

    insert_p_before(p_tab2, 
        bold_prefix="4. Tratamento de Valores Nulos e Imputação Temporal sem Vazamento de Dados (Data Leakage): ",
        text="O preenchimento de dados ausentes seguiu uma metodologia estritamente orientada ao domínio temporal, evitando o emprego ingênuo de médias aritméticas globais que romperiam a inércia histórica da série: (i) para a recomposição da continuidade nas séries históricas da base macroeconômica, empregou-se a interpolação linear temporal indexada pelo índice de datas (interpolate(method='time')), combinada com preenchimento para frente e para trás (ffill() e bfill()) restrito exclusivamente às pontas da amostra, preservando a curvatura natural e a inércia estocástica dos fenômenos econômicos; (ii) para os regressores supervisionados de aprendizado de máquina (como KNN, Lasso, Random Forest e Redes Neurais), estabeleceu-se uma blindagem metodológica contra o vazamento de informações futuras (lookahead bias). Quaisquer operadores de imputação estatística (como a mediana via SimpleImputer) foram calibrados (fit) exclusivamente na partição de treinamento e aplicados (transform) de maneira cega sobre a partição de teste, assegurando que o modelo opere apenas com as informações disponíveis no momento de cada decisão.",
        space_before=2, space_after=5)

    insert_p_before(p_tab2, 
        bold_prefix="5. Diagnóstico de Outliers e Preservação de Choques Macroeconômicos Reais: ",
        text="A identificação de observações discrepantes foi executada com base no critério interquartílico de Tukey (IQR = Q3 - Q1, com limites em Q1 - 1,5*IQR e Q3 + 1,5*IQR). No contexto econômico, anomalias extremas frequentemente não derivam de erros de medição, mas representam choques macroeconômicos genuínos e altamente informativos. No período avaliado (2012 a 2026), destacam-se dois episódios de grande impacto: a deflação histórica decorrente da eclosão da pandemia de COVID-19 e das medidas de confinamento sanitário em abril e maio de 2020; e a deflação induzida pelo corte legislativo nas alíquotas de ICMS e tributos federais sobre combustíveis e energia no segundo semestre de 2022. Eliminar ou substituir artificialmente esses pontos apagaria a própria volatilidade real que os modelos preditivos precisam aprender a capturar. Por essa razão, os choques reais foram integralmente preservados para a modelagem estocástica do ARIMA e ARIMAX. Já para os algoritmos de aprendizado de máquina cuja superfície de custo é sensível a distâncias espaciais euclidianas ou à convergência de gradientes (como o KNN e redes neurais), aplicou-se uma winsorização conservadora restrita aos percentis 1% e 99%, calculados exclusivamente a partir da partição de treinamento (np.clip(X, q_01, q_99)). Esse cuidado protege os regressores contra distorções geométricas severas nos pesos sem mascarar a dinâmica macroeconômica.",
        space_before=2, space_after=6)

    # 3.4.2 Redução de Dados
    insert_p_before(p_tab2, text="3.4.2 Técnicas de Redução de Dados e Dimensionalidade (Data Reduction)", heading_level=3)
    insert_p_before(p_tab2, text="A alta dimensionalidade macroeconômica eleva o risco de sobreajuste (overfitting), instabilidade nos parâmetros e multicolinearidade severa. Para concentrar a informação preditiva nas variáveis mais explicativas, aplicaram-se duas técnicas de redução:", space_before=2, space_after=5)

    insert_p_before(p_tab2, 
        bold_prefix="1. Redução Amostral Estrutural (Truncamento Temporal pós-março de 2012): ",
        text="Conforme justificado na Seção 3.2.1, delimitou-se o horizonte histórico a partir de março de 2012. Essa redução amostral intencional eliminou as quebras estruturais severas causadas pela transição metodológica da antiga Pesquisa Mensal de Emprego (PME) para a PNAD Contínua em escala nacional e pela reformulação dos pesos de consumo da POF 2008-2009 na composição do IPCA. Ao descartar observações anteriores geradas sob regimes estatísticos distintos, garantiu-se um painel equilibrado, contemporâneo e perfeitamente balanceado até 2026.",
        space_before=2, space_after=5)

    insert_p_before(p_tab2, 
        bold_prefix="2. Seleção de Atributos por Meta-heurísticas Bioinspiradas (GA e PSO): ",
        text="Partindo do conjunto de 27 covariáveis exógenas candidatas, o projeto empregou Algoritmos Genéticos (GA) e Otimização por Enxame de Partículas (PSO) para identificar os subconjuntos mais parcimoniosos e informativos para cada família de modelo. Os algoritmos exploraram o espaço combinatório e reduziram o espaço de entrada para subconjuntos de apenas 5 variáveis-chave. No modelo campeão do estudo (o híbrido ARIMAX + Random Forest), o PSO selecionou o conjunto ótimo composto por: IPCA_Transportes, IGP_DI, Produção_Derivados_Petróleo, Consumo_Gasolina e Estoque_Empregos_Formais_Total. Essa redução superior a 80% na dimensionalidade eliminou ruídos espúrios e garantiu a menor margem de erro preditivo de toda a pesquisa (RMSE de 0,1046 e MAE de 0,0850).",
        space_before=2, space_after=6)

    # 3.4.3 Transformação de Dados
    insert_p_before(p_tab2, text="3.4.3 Transformação de Dados e Engenharia de Atributos (Data Transformation)", heading_level=3)
    insert_p_before(p_tab2, text="A etapa de transformação adequou as propriedades matemáticas das séries temporais às exigências dos modelos estocásticos e algoritmos de aprendizado computacional:", space_before=2, space_after=5)

    insert_p_before(p_tab2, 
        bold_prefix="1. Estruturação de Matrizes e Particionamento Temporal Cronológico 80/20 (Walk-Forward): ",
        text="Os dados foram organizados formalmente na variável dependente alvo y_t (o IPCA mensal a ser previsto) e na matriz de atributos preditivos X_t (as variáveis exógenas selecionadas). Para emular um ambiente operacional de previsão econômica sem antecipação de dados futuros, a base tratada foi dividida na proporção de 80% para treinamento e 20% para teste e validação de forma estritamente sequencial e cronológica (shuffle=False). Essa divisão sustenta o esquema de avaliação walk-forward (previsões dinâmicas de 1 passo à frente utilizando exclusivamente o histórico acumulado até o mês imediatamente anterior).",
        space_before=2, space_after=5)

    insert_p_before(p_tab2, 
        bold_prefix="2. Teste de Raiz Unitária e Estacionarização Automática (make_stationary): ",
        text="Modelos estocásticos lineares da família ARIMA e ARIMAX pressupõem que as séries apresentem estacionariedade (média e variância constantes no tempo). Para garantir essa condição de forma padronizada, implementou-se a rotina make_stationary, fundamentada no teste Augmented Dickey-Fuller (ADF) a 5% de significância (p < 0,05). O teste confirmou que o IPCA mensal (p = 0,0002) e os subíndices setoriais de inflação (como Transportes, Habitação, IGP-M, INPC, IPC-BR e a taxa Selic) já são estacionários em nível (I(0)). Por outro lado, as variáveis exógenas de nível com tendência estocástica e raiz unitária (como o câmbio USDBRL, PIB Mensal e séries de combustíveis) foram submetidas à primeira diferenciação sucessiva (ΔX_t = X_t - X_{t-1}), tornando-se plenamente estacionárias (p < 0,001) e eliminando riscos de regressão espúria.",
        space_before=2, space_after=5)

    insert_p_before(p_tab2, 
        bold_prefix="3. Engenharia de Defasagens Temporais (Lags): ",
        text="Na dinâmica macroeconômica, as decisões de política monetária (Taxa Selic) e os choques cambiais operam com defasagens temporais distribuídas de 6 a 12 meses até atingirem os preços ao consumidor final. Para capacitar os regressores a apreenderem esses canais de transmissão defasados, construíram-se defasagens temporais autoregressivas (lags de 1 a 3 meses) nas principais séries preditivas.",
        space_before=2, space_after=5)

    insert_p_before(p_tab2, 
        bold_prefix="4. Padronização de Escalas via StandardScaler: ",
        text="Algoritmos de aprendizado de máquina (como Lasso, Random Forest e Redes Neurais) são altamente sensíveis à escala numérica dos atributos. Sem normalização, variáveis medidas na casa dos bilhões de reais (como o PIB) dominariam os gradientes de otimização em detrimento de variações percentuais decimais (como o IPCA e a Selic). Para equalizar a influência numérica de todas as séries, aplicou-se a padronização Z-Score (z = (x - μ) / σ). A média (μ) e o desvio padrão (σ) foram calculados estritamente sobre a partição de treinamento e replicados sobre o conjunto de teste, blindando a avaliação contra qualquer vazamento prospectivo.",
        space_before=2, space_after=6)

    # 3.4.4 Dicionário de Dados Final
    insert_p_before(p_tab2, text="3.4.4 Dicionário de Dados Final do Projeto", heading_level=3)
    insert_p_before(p_tab2, text="Como síntese consolidada de todas as etapas de limpeza, tratamento de inconsistências, estacionarização e seleção bioinspirada de atributos, estruturou-se o Dicionário de Dados Final apresentado na Tabela 2. A tabela relaciona cada uma das 28 variáveis utilizadas na modelagem (a variável dependente IPCA mais as 27 variáveis exógenas tratadas), detalhando o código identificador no SGS/BACEN, tipo computacional, transformação matemática executada, resultado formal do teste ADF de estacionariedade, inclusão nos subconjuntos ótimos de seleção (GA/PSO) e a respectiva função econômica dentro dos modelos preditivos.", space_before=2, space_after=6)

    # Remove old paragraphs
    for p in old_paragraphs:
        p._element.getparent().remove(p._element)
        
    doc.save(filepath)
    print(f"Saved {filepath} successfully!")

if __name__ == "__main__":
    for f in ["Artigo_Previsao_Inflacao_Final.docx", "Artigo_Previsao_Inflacao_v5.docx", "Artigo_Previsao_Inflacao_v3.docx"]:
        update_docx_file(f)
