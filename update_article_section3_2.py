import docx
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import shutil

def set_cell_margins(cell, top=70, bottom=70, left=70, right=70):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading)

def set_cell_borders(cell, top="CCCCCC", bottom="CCCCCC", left="CCCCCC", right="CCCCCC"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{top}"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="{left}"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{bottom}"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="{right}"/>
        </w:tcBorders>
    ''')
    tcPr.append(tcBorders)

def add_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def set_repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

# Load document from clean backup
doc = Document("Artigo_Previsao_Inflacao_v3_backup.docx")

# Find the insertion point: index of paragraph starting with 3.2 and "Referências Bibliográficas"
start_idx = None
ref_idx = None

for i, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith("3.2 Inventário") or p.text.strip().startswith("3.2 Dicionário"):
        start_idx = i
    elif "Referências Bibliográficas" in p.text:
        ref_idx = i

print(f"Found start_idx: {start_idx}, ref_idx: {ref_idx}")

# Collect paragraphs to remove
paragraphs_to_remove = doc.paragraphs[start_idx:ref_idx]
ref_p = doc.paragraphs[ref_idx]

# Helper function to insert paragraph before ref_p
def insert_p_before(ref_paragraph, text="", bold_prefix="", font_size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, heading_level=None):
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
        pf.space_after = Pt(6)
        r = new_p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.bold = True
        return new_p
    elif heading_level == 3:
        pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf.space_before = Pt(12)
        pf.space_after = Pt(4)
        r = new_p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(12)
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

# Data rows for table 1
table_data = [
    ("Date", "—", "Temporal", "AAAA-MM-DD", "Date", "Índice Temporal", "Data de referência mensal da observação."),
    ("IPCA", "4447", "Índice de Preços", "% a.m.", "Float", "Variável Alvo (y)", "Índice Nacional de Preços ao Consumidor Amplo (Meta oficial de inflação do BACEN)."),
    ("IPCA_Transportes", "1639", "Desagregação IPCA", "% a.m.", "Float", "Atributo Exógeno", "Variação de transportes públicos, veículos automotores e combustíveis."),
    ("IPCA Alimentação_bebidas", "1635", "Desagregação IPCA", "% a.m.", "Float", "Atributo Exógeno", "Variação de alimentos consumidos no domicílio e alimentação fora do lar."),
    ("INPC_Habitação", "1636", "Desagregação IPCA", "% a.m.", "Float", "Atributo Exógeno", "Variação de aluguel residencial, condomínio, gás e energia elétrica domiciliar."),
    ("IPCA_Saúde_cuidados_pessoais", "1641", "Desagregação IPCA", "% a.m.", "Float", "Atributo Exógeno", "Variação de produtos farmacêuticos, planos de saúde e serviços pessoais."),
    ("IPCA_Vestuário", "1638", "Desagregação IPCA", "% a.m.", "Float", "Atributo Exógeno", "Variação mensal de artigos de vestuário, calçados e tecidos."),
    ("IPCA_Educação", "1643", "Desagregação IPCA", "% a.m.", "Float", "Atributo Exógeno", "Variação de mensalidades escolares, ensino superior, cursos e material didático."),
    ("IPCA_Despesas_Pessoais", "1642", "Desagregação IPCA", "% a.m.", "Float", "Atributo Exógeno", "Variação de serviços recreativos, culturais, tabacaria e serviços diversos."),
    ("USDBRL", "3696", "Setor Financeiro", "R$ / US$", "Float", "Atributo Exógeno", "Taxa de câmbio PTAX de venda do Dólar Americano (canal de pass-through)."),
    ("SELIC", "4390", "Setor Financeiro", "% a.m.", "Float", "Atributo Exógeno", "Taxa de juros média nominal fixada pelo COPOM (Taxa Over/Selic)."),
    ("Reservas Internacionais", "3546", "Setor Externo", "US$ Mi", "Float", "Atributo Exógeno", "Montante total de liquidez internacional custodiada pela autoridade monetária."),
    ("INPC", "188", "Índice de Preços", "% a.m.", "Float", "Atributo Exógeno", "Índice Nacional de Preços ao Consumidor (famílias de 1 a 5 salários mínimos)."),
    ("IGP_M", "189", "Índice de Preços", "% a.m.", "Float", "Atributo Exógeno", "Índice Geral de Preços do Mercado (FGV) - indicador antecedente do atacado."),
    ("IGP_DI", "190", "Índice de Preços", "% a.m.", "Float", "Atributo Exógeno", "Índice Geral de Preços - Disponibilidade Interna (FGV)."),
    ("IPC_BR", "191", "Índice de Preços", "% a.m.", "Float", "Atributo Exógeno", "Índice de Preços ao Consumidor - Brasil (FGV)."),
    ("PIB Mensal", "4380", "Atividade Econômica", "R$ Mi", "Float", "Atributo Exógeno", "Estimativa mensal do Produto Interno Bruto a preços correntes."),
    ("Desemprego", "24369", "Mercado de Trabalho", "%", "Float", "Atributo Exógeno", "Taxa de desocupação mensal da população civil (PNAD Contínua/IBGE)."),
    ("SalMinimo", "1619", "Mercado de Trabalho", "R$", "Float", "Atributo Exógeno", "Valor nominal fixado por lei federal para o Salário Mínimo nacional."),
    ("Estoque_Empregos_Formais_Total", "28763", "Emprego Formal", "Vínculos", "Int", "Atributo Exógeno", "Estoque total de postos de trabalho formais celetistas ativos (CAGED)."),
    ("Estoque_Empregos_Formais_Agropecuária", "28764", "Emprego Formal", "Vínculos", "Int", "Atributo Exógeno", "Estoque de postos formais ativos no setor agropecuário (CAGED)."),
    ("Estoque_Empregos_Formais_Construção", "28770", "Emprego Formal", "Vínculos", "Int", "Atributo Exógeno", "Estoque de postos formais ativos no setor da construção civil (CAGED)."),
    ("QteOvos", "1310", "Agropecuária", "Mil Dúz.", "Float", "Atributo Exógeno", "Produção física de ovos de galinha (indicador da oferta alimentar)."),
    ("Produção_Derivados_Petróleo", "1391", "Energia / Insumos", "Mil m³", "Float", "Atributo Exógeno", "Volume de derivados de petróleo produzidos nas refinarias do país."),
    ("Consumo_Gasolina", "1393", "Combustíveis", "Mil m³", "Float", "Atributo Exógeno", "Consumo aparente mensal de gasolina automotiva no país."),
    ("Consumo_Óleo_Combustível", "1395", "Combustíveis", "Mil m³", "Float", "Atributo Exógeno", "Consumo industrial aparente mensal de óleo combustível."),
    ("Consumo_Energia_Comercial", "1402", "Energia Elétrica", "GWh", "Float", "Atributo Exógeno", "Consumo mensal de energia elétrica faturado na classe comercial."),
    ("Consumo_Energia_Residencial", "1403", "Energia Elétrica", "GWh", "Float", "Atributo Exógeno", "Consumo mensal de energia elétrica faturado na classe residencial."),
    ("Consumo_Energia_Total", "1406", "Energia Elétrica", "GWh", "Float", "Atributo Exógeno", "Consumo global de energia elétrica de todas as classes consumidoras.")
]

# Remove previous paragraphs
for p in paragraphs_to_remove:
    p._element.getparent().remove(p._element)

# Now, insert all new content sequentially before ref_p!
insert_p_before(ref_p, text="3.2 Dicionário e Inventário de Dados do Projeto", heading_level=2)

insert_p_before(ref_p, text="A base de dados empírica empregada neste trabalho foi construída a partir da coleta automatizada de séries temporais oficiais disponibilizadas pelo Banco Central do Brasil (BACEN), por intermédio de sua API pública integrada ao Sistema Gerenciador de Séries Temporais (SGS/BACEN). O horizonte temporal estende-se de março de 2012 até 2026, compreendendo observações mensais contínuas na frequência Month Start (MS), sem lacunas amostrais.", space_before=4, space_after=6)

insert_p_before(ref_p, text="O conjunto de dados consolida 1 variável dependente alvo (target) e 28 variáveis preditivas exógenas (atributos exógenos), estruturadas em quatro dimensões macroeconômicas funcionais da economia brasileira: (i) Índices de Preços e Desagregações Setoriais (11 variáveis); (ii) Setor Financeiro, Moeda e Câmbio (3 variáveis); (iii) Atividade Econômica e Mercado de Trabalho (7 variáveis); e (iv) Energia e Combustíveis (6 variáveis). A Tabela 1 apresenta o dicionário completo de dados do projeto, detalhando os identificadores oficiais no SGS/BACEN, tipagem computacional, unidades de medida, papel metodológico e a respectiva descrição econômica.", space_before=0, space_after=8)

# Table caption
p_cap = insert_p_before(ref_p, text="Tabela 1 – Dicionário de Dados e Inventário de Atributos Macroeconômicos", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=4)
p_cap.runs[0].bold = True
p_cap.runs[0].font.size = Pt(10.5)

# Insert table before ref_p
tbl = doc.add_table(rows=len(table_data) + 1, cols=7)
ref_p._p.addprevious(tbl._tbl)

col_widths = [Inches(1.2), Inches(0.55), Inches(1.0), Inches(0.75), Inches(0.5), Inches(0.9), Inches(1.6)]
headers = ["Atributo", "Código SGS", "Dimensão Econômica", "Unidade", "Tipo", "Papel no Modelo", "Descrição e Significado Econômico"]

# Format header row
hdr_row = tbl.rows[0]
set_repeat_header(hdr_row)
add_cant_split(hdr_row)
for j, h_text in enumerate(headers):
    cell = hdr_row.cells[j]
    cell.text = h_text
    cell.width = col_widths[j]
    set_cell_margins(cell, top=70, bottom=70, left=70, right=70)
    set_cell_shading(cell, "EAECEF")
    set_cell_borders(cell, top="999999", bottom="999999", left="D0D5DD", right="D0D5DD")
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0
    for r in p.runs:
        r.font.name = "Arial"
        r.font.size = Pt(8.5)
        r.bold = True

# Populate data rows
for i, row_data in enumerate(table_data):
    row = tbl.rows[i + 1]
    add_cant_split(row)
    bg_color = "FAFAFA" if i % 2 == 1 else "FFFFFF"
    for j, val in enumerate(row_data):
        cell = row.cells[j]
        cell.text = str(val)
        cell.width = col_widths[j]
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        set_cell_shading(cell, bg_color)
        set_cell_borders(cell, top="E2E8F0", bottom="E2E8F0", left="E2E8F0", right="E2E8F0")
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        if j in [0, 5, 6]:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        elif j in [1, 3, 4]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
        for r in p.runs:
            r.font.name = "Arial"
            r.font.size = Pt(8.0)
            if j == 0 and val == "IPCA":
                r.bold = True
            elif j == 5 and "Alvo" in val:
                r.bold = True

# Fonte note below table
p_fonte = insert_p_before(ref_p, text="Fonte: Autores, com base em dados compilados do SGS/Banco Central do Brasil (2026).", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=3, space_after=12)
p_fonte.runs[0].font.size = Pt(9.5)
p_fonte.runs[0].italic = True

# Subsection 3.2.1: Delimitação Temporal e Justificativa Metodológica
insert_p_before(ref_p, text="3.2.1 Delimitação Temporal e Justificativa Metodológica (2012 a 2026)", heading_level=3)
insert_p_before(ref_p, text="A determinação de março de 2012 como marco inicial para a série temporal do projeto não é arbitrária, decorrendo de uma rigorosa exigência metodológica para salvaguardar a consistência econométrica e evitar quebras estruturais (structural breaks) artificiais nos modelos. Três fatores institucionais e estatísticos fundamentam essa escolha:", space_before=2, space_after=6)

insert_p_before(ref_p, text="1. Transição Metodológica na Medição do Desemprego (PME versus PNAD Contínua): Até o início de 2012, a taxa oficial de desemprego no Brasil era aferida pelo IBGE através da Pesquisa Mensal de Emprego (PME). A PME possuía um escopo geográfico restrito a apenas seis regiões metropolitanas (Recife, Salvador, Belo Horizonte, Rio de Janeiro, São Paulo e Porto Alegre) e adotava critérios conceituais mais estritos quanto à busca ativa por ocupação. Em janeiro/março de 2012, o IBGE introduziu a Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua), estendendo a cobertura para a totalidade do território nacional e alinhando os critérios aos padrões internacionais da Organização Internacional do Trabalho (OIT). Devido à profunda divergência de escopo e metodologia, as séries históricas da PME e da PNAD Contínua não são comparáveis nem passiveis de empilhamento direto. Retroagir a série temporal antes de março de 2012 geraria uma quebra estrutural severa na dinâmica de desocupação, distorcendo o sinal da Curva de Phillips e inserindo ruído espúrio nos algoritmos de aprendizado supervisionado.", space_before=0, space_after=6)

insert_p_before(ref_p, text="2. Atualização Estrutural da Cesta de Ponderação do IPCA (POF 2008-2009): Em janeiro de 2012, o IBGE passou a aplicar uma nova estrutura de ponderação na composição do IPCA e do INPC, refletindo os hábitos de consumo mapeados pela Pesquisa de Orçamentos Familiares (POF 2008-2009). Essa revisão metodológica alterou significativamente os pesos relativos de grupos críticos, especialmente Transportes e Alimentação e Bebidas, reorganizando a forma de agregação dos subitens no Sistema Gerenciador de Séries Temporais do Banco Central. Dessa forma, as séries desagregadas a partir de 2012 refletem a dinâmica contemporânea estável da estrutura de consumo das famílias.", space_before=0, space_after=6)

insert_p_before(ref_p, text="3. Padronização de Séries Desagregadas do BACEN e Painel Balanceado: Diversos indicadores setoriais fundamentais adotados neste projeto — tais como séries desagregadas de consumo de combustíveis, consumo de energia elétrica por classe e séries compatibilizadas de estoque do emprego formal — iniciaram sua disponibilização regular e contínua no formato moderno do SGS a partir de 2012. Fixar o recorte entre março de 2012 e 2026 permitiu construir um painel de dados perfeitamente balanceado (balanced panel), sem necessidade de imputações artificiais ou interpolações em longos intervalos de dados faltantes estruturais, assegurando a robustez estocástica do pipeline preditivo.", space_before=0, space_after=8)

# Subsection 3.2.2: Variável Alvo
insert_p_before(ref_p, text="3.2.2 Variável Alvo e Dinâmica Inflacionária (IPCA)", heading_level=3)
insert_p_before(ref_p, text="O Índice Nacional de Preços ao Consumidor Amplo (IPCA), mensurado mensalmente pelo Instituto Brasileiro de Geografia e Estatística (IBGE), reflete o padrão de consumo de famílias urbanas com rendimento de 1 a 40 salários mínimos, constituindo a medida oficial para o acompanhamento do regime de metas de inflação do Conselho Monetário Nacional (CMN). No pipeline deste trabalho, o IPCA configura a variável dependente alvo (y_t). A série histórica exibe uma expressiva componente autorregressiva inercial associada a mecanismos de indexação da economia brasileira (como contratos de concessão pública, aluguéis e tarifas), combinada com choques residuais não lineares provocados por desequilíbrios exógenos de oferta e custos.", space_before=2, space_after=6)

# Subsection 3.2.3: Índices de Preços e Desagregações
insert_p_before(ref_p, text="3.2.3 Índices de Preços e Desagregações Setoriais", heading_level=3)
insert_p_before(ref_p, text="As desagregações setoriais do IPCA representam as forças desagregadas que originam a inflação cheia. Em particular, os grupos IPCA Alimentação e Bebidas e IPCA Transportes concentram juntos mais de 40% da ponderação total da cesta de consumo das famílias. O subíndice de alimentação é fortemente vulnerável a intempéries climáticas e flutuações das safras agrícolas, ao passo que o subíndice de transportes reage de imediato aos repasses de preços de combustíveis fósseis e reajustes tarifários urbanos. A incorporação desses subgrupos permite aos regressores de aprendizado de máquina discernir a propagação de choques setoriais específicos antes que eles contaminem os demais componentes da economia.", space_before=2, space_after=6)
insert_p_before(ref_p, text="De forma complementar, os índices gerais da Fundação Getulio Vargas (IGP-M e IGP-DI) desempenham papel de indicadores antecedentes (leading indicators). Uma vez que 60% de sua composição repousa no Índice de Preços ao Produtor Amplo (IPA), esses indicadores capturam repasses de custos no estágio atacadista e agrícola com antecedência em relação ao momento em que as pressões atingem o varejo ao consumidor final no IPCA. Paralelamente, o INPC e o IPC-BR fornecem a métrica da inflação incidente sobre as famílias de menor poder aquisitivo (1 a 5 salários mínimos), balizando a elasticidade-renda e a sensibilidade dos itens de primeira necessidade.", space_before=0, space_after=6)

# Subsection 3.2.4: Setor Financeiro, Moeda e Câmbio
insert_p_before(ref_p, text="3.2.4 Setor Financeiro, Moeda e Câmbio", heading_level=3)
insert_p_before(ref_p, text="A taxa de câmbio PTAX (USDBRL) constitui um dos principais determinantes da dinâmica inflacionária por meio do mecanismo de pass-through cambial. Depreciações do Real encarecem prontamente matérias-primas importadas, fertilizantes, defensivos, derivados de trigo e combustíveis, deflagrando pressões de custos que atingem tanto bens comercializáveis quanto preços administrados. Por sua vez, a Taxa Selic atua como o instrumento central de política monetária do Banco Central do Brasil, moderando as pressões de demanda agregada através de quatro canais de transmissão (custo do crédito, propensão à poupança, ancoragem das expectativas e valorização cambial por atratividade de juros), com defasagens observadas entre 6 e 12 meses. O montante de Reservas Internacionais sinaliza a liquidez do país e a capacidade de intervenção do BACEN para mitigar choques externos de volatilidade.", space_before=2, space_after=6)

# Subsection 3.2.5: Atividade Econômica e Mercado de Trabalho
insert_p_before(ref_p, text="3.2.5 Atividade Econômica e Mercado de Trabalho", heading_level=3)
insert_p_before(ref_p, text="O nível de aquecimento da economia real é mensurado pela estimativa do PIB Mensal a preços correntes, fundamental para o cálculo do hiato do produto — elemento orientador da inflação de demanda. No âmbito do mercado de trabalho, a taxa de desocupação da PNAD Contínua e o Salário Mínimo nominal fundamentam a relação teórica da Curva de Phillips na economia brasileira. Condições de pleno emprego e valorizações reais do piso salarial impulsionam a renda disponível e geram pressões de custos no setor de serviços, caracterizado pela reduzida exposição ao comércio exterior e por custos dominados pela folha de pagamento.", space_before=2, space_after=6)
insert_p_before(ref_p, text="O estoque de postos celetistas do Cadastro Geral de Empregados e Desempregados (CAGED), tanto no agregado total quanto nos recortes da Agropecuária e Construção Civil, mensura o grau de estabilidade contratual das famílias e o potencial de demanda futura por crédito consignado e imobiliário. Por fim, a série de Produção de Ovos (QteOvos) representa uma proxy física contínua da atividade agroindustrial avícola, indicando condições de oferta de proteína animal e custos de insumos na cadeia de nutrição doméstica.", space_before=0, space_after=6)

# Subsection 3.2.6: Energia e Combustíveis
insert_p_before(ref_p, text="3.2.6 Energia e Combustíveis", heading_level=3)
insert_p_before(ref_p, text="Considerando a matriz logística nacional intensiva em transporte rodoviário, as variáveis de refino e consumo de derivados de petróleo (Consumo de Gasolina, Consumo de Óleo Combustível e Produção de Derivados) funcionam como termômetros do transporte de cargas e insumos produtivos, cujas oscilações de preço se difundem horizontalmente na economia. Ademais, as métricas físicas de consumo elétrico (Consumo Comercial, Residencial e Total) operam como sensores de alta frequência do nível de ocupação comercial e residencial sem a distorção nominal decorrente de reajustes tarifários.", space_before=2, space_after=6)

# Subsection 3.2.7: Pré-processamento e Estacionariedade
insert_p_before(ref_p, text="3.2.7 Pré-processamento, Alinhamento Temporal e Teste de Estacionariedade", heading_level=3)
insert_p_before(ref_p, text="Para salvaguardar a robustez metodológica dos experimentos e mitigar viés de antecipação (lookahead bias) ou vazamento de informações (data leakage), todas as variáveis foram devidamente sincronizadas de acordo com as respectivas datas de divulgação formal das séries. Nas variáveis cuja cotação original ocorria em frequência diária (taxa Selic e taxa de câmbio), realizou-se a agregação pela média aritmética mensal dos dias úteis.", space_before=2, space_after=6)
insert_p_before(ref_p, text="Para adequação às premissas dos modelos estocásticos lineares (ARIMA e ARIMAX) e aos algoritmos híbridos de aprendizado de máquina, cada série temporal foi submetida ao teste estatístico de raiz unitária Augmented Dickey-Fuller (ADF) sob nível de significância de alfa = 0,05. As séries com comportamento não estacionário em nível foram submetidas à primeira diferenciação sucessiva (Delta X_t = X_t - X_{t-1}), assegurando propriedades estocásticas de média e variância constantes durante o treinamento sequencial walk-forward.", space_before=0, space_after=12)

# Save document
output_filename = "Artigo_Previsao_Inflacao_v3.docx"
doc.save(output_filename)
print("Updated document saved successfully!")
