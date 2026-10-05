import os
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
DIR_LOGOS = os.path.join(DIR_ARTIGO, 'Logos')

LOGO_UPE = os.path.join(DIR_LOGOS, 'logo_upe.png')
LOGO_POLI = os.path.join(DIR_LOGOS, 'logo_poli.png')

# Criar novo documento limpo
doc = Document()

# Configurações de Página: Padrão A4 com Margens ABNT (Sup: 3cm, Esq: 3cm, Inf: 2cm, Dir: 2cm)
for sec in doc.sections:
    sec.page_width = Inches(8.27)    # 210 mm (A4)
    sec.page_height = Inches(11.69)  # 297 mm (A4)
    sec.top_margin = Inches(1.18)    # 3.0 cm
    sec.left_margin = Inches(1.18)   # 3.0 cm
    sec.bottom_margin = Inches(0.79) # 2.0 cm
    sec.right_margin = Inches(0.79)  # 2.0 cm
    sec.header_distance = Inches(0.5)
    sec.footer_distance = Inches(0.4)
    sec.different_first_page_header_footer = True

# Configuração Global de Estilos Nativos do Word
COLOR_NAVY = RGBColor(31, 78, 121)   # #1F4E79 (Azul Acadêmico Profissional)
COLOR_TEXT = RGBColor(20, 20, 20)
COLOR_MUTED = RGBColor(100, 100, 100)

style_normal = doc.styles['Normal']
style_normal.font.name = 'Arial'
style_normal.font.size = Pt(11.0)
style_normal.font.color.rgb = COLOR_TEXT
style_normal.paragraph_format.line_spacing = 1.15
style_normal.paragraph_format.space_after = Pt(4)
style_normal.paragraph_format.space_before = Pt(0)
style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

style_h1 = doc.styles['Heading 1']
style_h1.font.name = 'Arial'
style_h1.font.size = Pt(13.0)
style_h1.font.bold = True
style_h1.font.color.rgb = COLOR_NAVY
style_h1.paragraph_format.space_before = Pt(14)
style_h1.paragraph_format.space_after = Pt(5)
style_h1.paragraph_format.keep_with_next = True
style_h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

style_h2 = doc.styles['Heading 2']
style_h2.font.name = 'Arial'
style_h2.font.size = Pt(11.5)
style_h2.font.bold = True
style_h2.font.color.rgb = COLOR_NAVY
style_h2.paragraph_format.space_before = Pt(11)
style_h2.paragraph_format.space_after = Pt(4)
style_h2.paragraph_format.keep_with_next = True
style_h2.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

style_h3 = doc.styles['Heading 3']
style_h3.font.name = 'Arial'
style_h3.font.size = Pt(11.0)
style_h3.font.bold = True
style_h3.font.color.rgb = RGBColor(50, 50, 50)
style_h3.paragraph_format.space_before = Pt(8)
style_h3.paragraph_format.space_after = Pt(3)
style_h3.paragraph_format.keep_with_next = True
style_h3.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

# Configuração do Rodapé para páginas a partir da Página 2
footer = doc.sections[0].footer
p_f = footer.paragraphs[0]
p_f.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_f.paragraph_format.space_before = Pt(0)
p_f.paragraph_format.space_after = Pt(0)

r_f_txt = p_f.add_run("Página ")
r_f_txt.font.name = "Arial"
r_f_txt.font.size = Pt(9.0)
r_f_txt.font.color.rgb = COLOR_MUTED

fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))

run_p = p_f.add_run()
run_p._r.append(fldChar1)
run_p._r.append(instrText)
run_p._r.append(fldChar2)
run_p._r.append(fldChar3)
run_p.font.name = "Arial"
run_p.font.size = Pt(9.0)
run_p.font.color.rgb = COLOR_MUTED

# Helpers de Parágrafo e Formatação
def add_p(text="", bold_prefix="", font_size=11.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, heading_level=None):
    if heading_level == 1:
        p = doc.add_paragraph(style='Heading 1')
        p.paragraph_format.space_before = Pt(space_before or 14)
        p.paragraph_format.space_after = Pt(space_after or 5)
        p.paragraph_format.alignment = align
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(13.0)
        r.font.color.rgb = COLOR_NAVY
        r.bold = True
        return p
    elif heading_level == 2:
        p = doc.add_paragraph(style='Heading 2')
        p.paragraph_format.space_before = Pt(space_before or 11)
        p.paragraph_format.space_after = Pt(space_after or 4)
        p.paragraph_format.alignment = align
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(11.5)
        r.font.color.rgb = COLOR_NAVY
        r.bold = True
        return p
    elif heading_level == 3:
        p = doc.add_paragraph(style='Heading 3')
        p.paragraph_format.space_before = Pt(space_before or 8)
        p.paragraph_format.space_after = Pt(space_after or 3)
        p.paragraph_format.alignment = align
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(11.0)
        r.font.color.rgb = RGBColor(50, 50, 50)
        r.bold = True
        return p

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.alignment = align

    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(font_size)

    if text:
        r_text = p.add_run(text)
        r_text.font.name = "Arial"
        r_text.font.size = Pt(font_size)

    return p

def add_callout(text, title="Pergunta Central de Pesquisa:"):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.space_before = Pt(6)
    pf.space_after = Pt(8)
    pf.left_indent = Inches(0.2)
    pf.right_indent = Inches(0.2)
    pPr = p._p.get_or_add_pPr()
    pBdr = parse_xml(r'<w:pBdr %s><w:left w:val="single" w:sz="24" w:space="12" w:color="1F4E79"/></w:pBdr>' % nsdecls('w'))
    shd = parse_xml(r'<w:shd %s w:fill="F4F6F9"/>' % nsdecls('w'))
    pPr.append(pBdr)
    pPr.append(shd)

    r_title = p.add_run(f"{title} ")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(10.5)
    r_title.font.color.rgb = COLOR_NAVY

    r_text = p.add_run(f'"{text}"')
    r_text.italic = True
    r_text.font.name = "Arial"
    r_text.font.size = Pt(10.5)
    r_text.font.color.rgb = RGBColor(30, 30, 30)

def add_img(img_name, caption_text, width=Inches(5.5)):
    img_path = os.path.join(DIR_GRAFICOS, img_name)
    if os.path.exists(img_path):
        p_img = add_p(align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=2)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=width)

        p_cap = add_p(text=caption_text, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=5)
        p_cap.runs[0].font.size = Pt(9.0)
        p_cap.runs[0].font.name = "Arial"
        p_cap.runs[0].italic = True

def helper_format_cell(cell, text, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex=None, width=None, text_color=None, font_size=8.5):
    if width:
        cell.width = width
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', 50), ('bottom', 50), ('left', 60), ('right', 60)]:
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
            <w:top w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>
            <w:left w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>
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
    r.font.size = Pt(font_size)
    r.bold = bold
    if text_color:
        r.font.color.rgb = text_color

def make_row_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def make_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

# =============================================================================
# CONSTRUÇÃO DA CAPA OFICIAL (PADRÃO MODELO POLI-UPE / ABNT)
# =============================================================================
print("Construindo Capa Oficial do Trabalho (Logos UPE e POLI)...")

# 1. Inserção dos Logos UPE e POLI lado a lado (Tabela sem bordas)
if os.path.exists(LOGO_UPE) and os.path.exists(LOGO_POLI):
    tbl_logo = doc.add_table(rows=1, cols=2)
    tbl_logo.alignment = WD_TABLE_ALIGNMENT.CENTER
    borders_zero = parse_xml(r'''
        <w:tblBorders %s>
            <w:top w:val="none"/>
            <w:left w:val="none"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="none"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''' % nsdecls('w'))
    tbl_logo._tbl.tblPr.append(borders_zero)
    
    c1, c2 = tbl_logo.rows[0].cells[0], tbl_logo.rows[0].cells[1]
    c1.width = Inches(2.2)
    c2.width = Inches(2.2)
    
    p_l1 = c1.paragraphs[0]
    p_l1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_l1.paragraph_format.space_before = Pt(0)
    p_l1.paragraph_format.space_after = Pt(0)
    r_l1 = p_l1.add_run()
    r_l1.add_picture(LOGO_UPE, height=Inches(1.05))
    
    p_l2 = c2.paragraphs[0]
    p_l2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_l2.paragraph_format.space_before = Pt(8)
    p_l2.paragraph_format.space_after = Pt(0)
    r_l2 = p_l2.add_run()
    r_l2.add_picture(LOGO_POLI, height=Inches(0.75))

# 2. Cabeçalho Institucional da Capa
p_inst = doc.add_paragraph()
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_inst.paragraph_format.space_before = Pt(14)
p_inst.paragraph_format.space_after = Pt(3)
p_inst.paragraph_format.line_spacing = 1.25

r_inst1 = p_inst.add_run("UNIVERSIDADE DE PERNAMBUCO\n")
r_inst1.bold = True
r_inst1.font.name = "Arial"
r_inst1.font.size = Pt(12.0)

r_inst2 = p_inst.add_run("ESCOLA POLITÉCNICA DE PERNAMBUCO - POLI\n")
r_inst2.bold = True
r_inst2.font.name = "Arial"
r_inst2.font.size = Pt(11.5)

r_inst3 = p_inst.add_run("CAMPUS RECIFE\n")
r_inst3.font.name = "Arial"
r_inst3.font.size = Pt(11.0)
r_inst3.font.italic = True

r_inst4 = p_inst.add_run("CURSO DE ENGENHARIA DA COMPUTAÇÃO\n")
r_inst4.bold = True
r_inst4.font.name = "Arial"
r_inst4.font.size = Pt(11.0)

r_inst5 = p_inst.add_run("DISCIPLINA: MINERAÇÃO DE DADOS\n")
r_inst5.font.name = "Arial"
r_inst5.font.size = Pt(10.5)

r_inst6 = p_inst.add_run("PROFESSOR: PROF. DR. ALEXANDRE MACIEL")
r_inst6.bold = True
r_inst6.font.name = "Arial"
r_inst6.font.size = Pt(10.5)

# 3. Autores / Membros (Centro-Superior)
p_aut = doc.add_paragraph()
p_aut.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_aut.paragraph_format.space_before = Pt(55)
p_aut.paragraph_format.space_after = Pt(0)
p_aut.paragraph_format.line_spacing = 1.35

membros = [
    "BRUNO PROTÁSIO",
    "DANIEL MENESES",
    "MARCUS VINICIUS",
    "VINICYUS EMANUEL"
]
for idx, m in enumerate(membros):
    r_m = p_aut.add_run(m + ("\n" if idx < len(membros) - 1 else ""))
    r_m.bold = True
    r_m.font.name = "Arial"
    r_m.font.size = Pt(11.5)

# 4. Título do Trabalho (Centro) - Estilo Engenharia de Computação, sem IPCA e sem "uma abordagem"
p_tit_capa = doc.add_paragraph()
p_tit_capa.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_tit_capa.paragraph_format.space_before = Pt(75)
p_tit_capa.paragraph_format.space_after = Pt(0)
p_tit_capa.paragraph_format.line_spacing = 1.25

r_tc1 = p_tit_capa.add_run("MINERAÇÃO DE SÉRIES TEMPORAIS PARA PREVISÃO DA INFLAÇÃO:\n")
r_tc1.bold = True
r_tc1.font.name = "Arial"
r_tc1.font.size = Pt(13.5)

r_tc2 = p_tit_capa.add_run("ARQUITETURA HÍBRIDA MULTIVARIADA E OTIMIZAÇÃO BIOINSPIRADA DE ATRIBUTOS")
r_tc2.bold = True
r_tc2.font.name = "Arial"
r_tc2.font.size = Pt(12.5)

# 5. Cidade e Ano (Rodapé da Capa)
p_cid = doc.add_paragraph()
p_cid.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cid.paragraph_format.space_before = Pt(95)
p_cid.paragraph_format.space_after = Pt(0)
p_cid.paragraph_format.line_spacing = 1.2

r_cid = p_cid.add_run("RECIFE\n2026")
r_cid.bold = True
r_cid.font.name = "Arial"
r_cid.font.size = Pt(11.0)

# Quebra de Página para Início do Artigo
doc.add_page_break()

# =============================================================================
# INÍCIO DO ARTIGO (PÁGINA 2) - DIRETO EM 1 INTRODUÇÃO
# =============================================================================
print("Escrevendo Seção 1 (INTRODUÇÃO) diretamente após a quebra de página...")

# =============================================================================
# 1 INTRODUÇÃO
# =============================================================================
add_p(text="1 INTRODUÇÃO", heading_level=1)

add_p(text="A trajetória dos preços em uma economia em desenvolvimento como a brasileira é marcada por uma tensão permanente entre a memória do passado e os choques imprevisíveis do presente. Ao longo de décadas, a sociedade conviveu com oscilações inflacionárias que desgastam a renda do trabalho, tornam o crédito escasso e impõem pesadas incertezas sobre o planejamento das famílias e das empresas. A consolidação da estabilidade monetária com a criação do Plano Real e a posterior adoção do regime de metas para a inflação estabeleceram um pacto institucional: manter o poder de compra da moeda através do monitoramento rigoroso do Índice Nacional de Preços ao Consumidor Amplo (IPCA), calculado mensalmente pelo Instituto Brasileiro de Geografia e Estatística (IBGE).")

add_p(text="Contudo, conduzir e antecipar essa dinâmica é uma tarefa desafiadora. O Banco Central do Brasil utiliza a taxa básica de juros (Selic) como seu principal instrumento de controle, mas as decisões de política monetária demandam entre dois e quatro trimestres para produzir efeitos plenos sobre o consumo e os investimentos. Essa defasagem temporal impede que gestores públicos e privados naveguem olhando apenas para os preços observados ontem; torna-se imperativo antecipar o comportamento futuro do índice para embasar decisões tempestivas.")

add_p(text="Historicamente, a literatura estatística abordou a previsão de preços sob a ótica univariada, partindo da premissa de que o próprio histórico de inflação sintetiza a inércia dos contratos e as expectativas dos agentes. Modelos clássicos de séries temporais assumem que as defasagens passadas e os ciclos sazonais são suficientes para projetar os próximos períodos. Entretanto, a economia brasileira é exposta a perturbações exógenas frequentes: choques cambiais que encarecem insumos importados, oscilações severas nas cotações internacionais de commodities energéticas, secas que penalizam a produção agrícola e desequilíbrios no mercado de trabalho.")

add_p(text="Surge, assim, um dilema central de modelagem: modelos estritamente univariados correm o risco de ignorar sinais antecipados cruciais emitidos por variáveis externas, enquanto abordagens multivariadas que incorporam dezenas de indicadores econômicos enfrentam o risco de ruído amostral, multicolinearidade e superajuste (overfitting). O presente projeto investiga essa fronteira empírica sob a ótica da Engenharia da Computação e da Mineração de Dados. A presente entrega foca na formulação do problema, na integração interdisciplinar com economistas e no pipeline completo de coleta, análise exploratória descritiva e pré-processamento de um robusto painel macroeconômico, preparando a base para a futura calibração de modelos preditivos e algoritmos bioinspirados de seleção de atributos.")

add_p(text="1.1 Contextualização", heading_level=2)
add_p(text="A dinâmica da inflação no Brasil conecta-se diretamente à arquitetura do Sistema Financeiro Nacional. O Conselho Monetário Nacional (CMN) define as metas anuais de inflação, cabendo ao Banco Central do Brasil (BACEN) calibrar as condições financeiras para o seu cumprimento.")
add_p(text="Para a ciência e engenharia de dados, esse cenário desdobra-se em três pilares de relevância aplicada:")
add_p(bold_prefix="• Setor Público e Governança Macroeconômica: ", text="O fornecimento de estimativas acuradas mitiga assimetrias informacionais, permitindo avaliar pressões de custos antes que se disseminem pela economia e auxiliando na ancoragem das expectativas de mercado;")
add_p(bold_prefix="• Mercado Financeiro e Atividade Corporativa: ", text="Empresas utilizam projeções de inflação para reajustar contratos de fornecimento de longo prazo, planejar orçamentos de capital e gerenciar estoques. No mercado financeiro, a correta precificação de títulos indexados à inflação (como NTN-B e debêntures) e a gestão de risco de tesouraria dependem da acurácia dessas projeções;")
add_p(bold_prefix="• Pesquisa em Engenharia e Mineração de Dados: ", text="Séries macroeconômicas de economias emergentes oferecem um ambiente de estresse para algoritmos computacionais, demandando engenharia de dados precisa para sincronizar bases heterogêneas, sanear dados ruidosos e evitar vazamento temporal.")

add_p(text="1.2 Descrição do Problema", heading_level=2)
add_p(text="O desafio central consiste em arbitrar entre a inércia temporal e a sensibilidade a choques macroeconômicos externos:")
add_p(bold_prefix="1. A Hipótese Univariada: ", text="Postula que a inércia inflacionária — sustentada por indexação contratual e rigidez de preços — domina a trajetória da série, de modo que modelos autorregressivos simples superariam formulações complexas que demandam estimativas de terceiros;")
add_p(bold_prefix="2. A Hipótese Multivariada: ", text="Postula que indicadores antecedentes de preços no atacado, custos de transporte, cotação do dólar e nível de atividade agregada emitem sinais preditivos antecipados que o histórico isolado do índice de inflação é incapaz de capturar a tempo.")
add_p(text="A questão metodológica reside em determinar se a complexidade multivariada compensa o risco de instabilidade estatística e quais classes de variáveis econômicas trazem ganho preditivo mensurável.")

add_callout(
    text="A utilização de variáveis macroeconômicas exógenas melhora a acurácia preditiva da inflação frente a modelos puramente univariados? Quais atributos possuem maior capacidade de antecipar a trajetória da inflação brasileira?",
    title="Pergunta Central de Pesquisa:"
)

add_p(text="1.3 Objetivos", heading_level=2)
add_p(text="1.3.1 Objetivo Geral da Etapa Atual", heading_level=3)
add_p(text="Desenvolver o processo de mineração de dados focado na formulação do problema, fundamentação teórica, análise exploratória descritiva e pré-processamento integral de séries temporais da inflação brasileira e variáveis exógenas antecedentes, estruturando uma base de dados higienizada, consistente e documentada sob orientação de especialistas para fundamentar a futura calibração de modelos preditivos multivariados.")

add_p(text="1.3.2 Objetivos Específicos do Escopo Atual", heading_level=3)
add_p(bold_prefix="1. Engenharia e Coleta de Dados Macroeconômicos: ", text="Coletar e consolidar a série histórica mensal do IPCA e de 28 variáveis exógenas candidatas de março de 2012 a agosto de 2026 via API oficial do SGS/Banco Central;")
add_p(bold_prefix="2. Mapeamento de Stakeholders e Orientação Acadêmica: ", text="Mapear os envolvidos no projeto, articulando a orientação acadêmica do Prof. Dr. Alexandre Maciel (POLI/UPE) e a consultoria de domínio macroeconômico do Prof. Guilherme Martins (FCAP/UPE);")
add_p(bold_prefix="3. Fundamentação Teórica e Diferenciais Metodológicos: ", text="Estruturar a revisão da literatura e estabelecer a matriz comparativa de diferenciais frente aos modelos clássicos e recentes;")
add_p(bold_prefix="4. Caracterização Estatística e Visual dos Dados: ", text="Conduzir análise descritiva univariada e bivariada dos atributos contínuos e discretos, explorando assimetrias, outliers e comportamento sob diferentes regimes nominais de inflação;")
add_p(bold_prefix="5. Pipeline de Pré-processamento e Saneamento: ", text="Implementar rotinas sistemáticas de limpeza de nulos, alinhamento temporal em frequência uniforme (Month-Start), tratamento de inconsistências, redução amostral e codificação de atributos;")
add_p(bold_prefix="6. Estruturação do Dicionário de Dados da Base Consolidada: ", text="Documentar formalmente todos os 31 atributos consolidados, seus códigos de origem, tipagem, procedimentos de pré-processamento e relevância de negócio.")

add_p(text="1.4 Justificativa", heading_level=2)
add_p(text="Projeções de inflação influenciam a taxa de juros real da economia, os custos de captação de dívida soberana e a formação de preços no atacado e no varejo. Séries econômicas brasileiras apresentam não linearidades, quebras de regime e forte exposição a choques internacionais. Sob a perspectiva da computação aplicada, a pesquisa contribui ao estabelecer um pipeline reprodutível de engenharia de dados que transforma séries públicas brutas em um painel estruturado, alinhado e auditável, eliminando vieses e viabilizando a futura aplicação de estimadores preditivos avançados.")

add_p(text="1.5 Escopo Negativo e Delimitação da Etapa", heading_level=2)
add_p(text="Para assegurar clareza quanto à entrega atual do projeto, definem-se os seguintes limites de escopo:")
add_p(bold_prefix="• Análise de Estacionariedade e Modelagem Preditiva nesta Fase: ", text="A realização de testes de raiz unitária (ADF), transformações de diferenciação para modelos específicos, calibração de algoritmos preditivos (ARIMA, ARIMAX, Random Forest, Lasso, Arquitetura Híbrida) e otimização bioinspirada (GA e PSO) pertencem à etapa subsequente do projeto, não fazendo parte do escopo da presente entrega, que encerra-se formalmente no pré-processamento dos dados;")
add_p(bold_prefix="• Alta Frequência e Intradiário: ", text="O estudo concentra-se na frequência mensal oficial e não aborda cotações diárias ou intradiárias de preços;")
add_p(bold_prefix="• Nível Microeconômico: ", text="Não são investigadas cestas de consumo de indivíduos específicos, recortes regionais isolados ou desagregações domiciliares da POF;")
add_p(bold_prefix="• Prescrição de Política Econômica: ", text="O trabalho tem finalidade analítica e de engenharia de dados, sem emitir recomendações normativas sobre o patamar adequado de juros ou diretrizes fiscais.")

# =============================================================================
# 2 FUNDAMENTAÇÃO TEÓRICA
# =============================================================================
print("Escrevendo Seção 2 (FUNDAMENTAÇÃO TEÓRICA)...")
add_p(text="2 FUNDAMENTAÇÃO TEÓRICA", heading_level=1)

add_p(text="2.1 Área do Negócio: O Funcionamento da Inflação e a Dinâmica Econômica", heading_level=2)
add_p(text="Para compreender o desafio de antecipar a inflação, é necessário desmistificar o fenômeno em linguagem acessível a leitores de diferentes áreas e fundamentada na literatura macroeconômica.")

add_p(text="O que é a Inflação na Prática?", heading_level=3)
add_p(text="De forma intuitiva, a inflação não é apenas o encarecimento de um produto específico, como o tomate ou a energia elétrica; ela representa o aumento contínuo e generalizado no nível de preços de bens e serviços de uma economia ao longo do tempo [4, 13]. O efeito prático mais imediato é a perda do poder de compra da moeda: se uma nota de R$ 100 permitia comprar um conjunto completo de mantimentos no início do ano e, meses depois, adquire apenas uma fração desses mesmos produtos, a moeda perdeu valor relativo [13].")

add_p(text="Como o IPCA Mede Essa Realidade?", heading_level=3)
add_p(text="No Brasil, a inflação oficial é mensurada pelo Índice Nacional de Preços ao Consumidor Amplo (IPCA), calculado pelo IBGE desde 1979 e adotado formalmente como bússola do sistema de metas [10]. Para mensurá-lo, o IBGE não calcula uma média simples de preços: constrói-se uma 'cesta média de consumo' ponderada, que reflete como as famílias com renda entre 1 e 40 salários mínimos distribuem seus gastos [10]. Despesas com alimentação, habitação e transporte possuem peso predominante no orçamento das famílias brasileiras; portanto, variações nesses grupos provocam impactos assimétricos sobre o índice geral.")

add_p(text="Os Três Grandes Motores da Inflação Brasileira", heading_level=3)
add_p(text="A literatura econômica contemporânea e a experiência empírica brasileira identificam três forças fundamentais que movimentam os preços:")
add_p(bold_prefix="1. A Inércia e a Memória da Moeda: ", text="O Brasil atravessou décadas de inflação crônica antes do Plano Real, o que consolidou mecanismos formais e informais de 'indexação' [5, 16]. Na prática, diversos preços da economia — como aluguéis residenciais, tarifas públicas, pedágios, mensalidades escolares e convenções coletivas de trabalho — são reajustados periodicamente pela inflação passada. Isso gera um comportamento de persistência ou 'memória temporal': a inflação de hoje carrega em si a taxa observada no passado, perpetuando o ciclo mesmo na ausência de novos choques [5, 16];")
add_p(bold_prefix="2. Choques de Oferta e Custos (Câmbio e Commodities): ", text="Quando ocorrem perturbações externas, como a alta internacional do petróleo ou a desvalorização cambial do Real frente ao Dólar americano, os insumos de importação tornam-se imediatamente mais onerosos [3, 6]. O aumento nos preços dos combustíveis eleva o custo do frete rodoviário, que encarece a distribuição de alimentos e bens de consumo, produzindo o mecanismo clássico de repasse cambial (pass-through) para o consumidor final [6];")
add_p(bold_prefix="3. Pressões de Demanda e o Hiato do Produto: ", text="Quando a atividade econômica se expande aceleradamente, impulsionando a contratação de trabalhadores e o aumento da renda agregada acima da capacidade física das fábricas e prestadores de serviço de ofertar bens, surge escassez relativa [4, 17]. Os produtores ajustam os preços para cima para equilibrar o mercado, relação descrita classicamente pelo mecanismo da Curva de Phillips [4, 17].")

add_p(text="O Banco Central e o 'Termostato' da Política Monetária", heading_level=3)
add_p(text="Para evitar desarranjos na estabilidade de preços, o Conselho Monetário Nacional (CMN) define uma meta percentual anual. O Banco Central atua como regulador do sistema por meio do Comitê de Política Monetária (COPOM), utilizando a taxa básica de juros (Selic) como instrumento regulador [3, 17].")
add_p(text="A taxa Selic funciona de maneira análoga a um termostato econômico:")
add_p(bold_prefix="• Elevação da Taxa Selic: ", text="Quando a inflação ameaça ultrapassar o teto da meta, o Banco Central eleva a taxa Selic. O crédito fica mais caro, o custo de oportunidade de poupar aumenta, as empresas adiam investimentos e as famílias reduzem o consumo financiado. Essa desaceleração da demanda arrefece a alta dos preços [3, 13];")
add_p(bold_prefix="• Redução da Taxa Selic: ", text="Por outro lado, se a economia se retrai e a inflação converge para níveis muito baixos, o BACEN pode reduzir a taxa Selic para reativar a atividade produtiva.")
add_p(text="O ponto crítico desse processo é a existência de defasagens temporais de transmissão (transmission lags): uma decisão tomada pelo COPOM hoje leva entre 6 e 12 meses para se propagar pelos canais de crédito, câmbio e expectativas até afetar os preços finais [3, 17]. Por esse motivo, as autoridades monetárias e os analistas de mercado dependem de modelos preditivos tempestivos, capazes de antecipar a trajetória da inflação no horizonte relevante.")

# 2.2 Mineração de Dados (Pula / Etapa Posterior)
add_p(text="2.2 Mineração de Dados", heading_level=2)
p_nota = add_p(text="*(Nota: O detalhamento conceitual e matemático dos algoritmos computacionais de aprendizado de máquina, redes neurais e operadores genéticos será incorporado nesta subseção na etapa subsequente do projeto, permanecendo este tópico reservado para a fundamentação algorítmica específica).*")
p_nota.runs[0].font.color.rgb = COLOR_MUTED
p_nota.runs[0].italic = True

# 2.3 Trabalhos Relacionados
add_p(text="2.3 Trabalhos Relacionados e Análise de Diferenciais", heading_level=2)
add_p(text="A literatura sobre modelagem da inflação organiza-se em três paradigmas metodológicos principais:")
add_p(bold_prefix="1. Modelagem Paramétrica Box-Jenkins: ", text="A abordagem clássica de séries temporais de Box e Jenkins [1] consolidou o uso de processos autorregressivos integrados de médias móveis (ARIMA). Tais formulações capturam adequadamente a inércia estocástica e a sazonalidade, mas partem de hipóteses rígidas de linearidade e não respondem com tempestividade a choques de oferta exógenos [1, 9];")
add_p(bold_prefix="2. Arquiteturas Híbridas Lineares e Não Lineares: ", text="Zhang [18] introduziu a formulação híbrida canônica que decompõe uma série temporal na soma de uma componente linear com uma componente residual não linear (y_t = L_t + N_t). Ao aplicar redes neurais aos resíduos do ARIMA, Zhang demonstrou que a modelagem conjunta supera estimadores isolados. Contudo, suas aplicações originais concentraram-se em séries univariadas sem covariáveis macroeconômicas exógenas [18];")
add_p(bold_prefix="3. Machine Learning Multivariado de Alta Dimensionalidade: ", text="Estudos contemporâneos de econometria aplicada, como Garcia et al. [6] e Medeiros et al. [14], avaliaram o emprego de métodos de regularização (como Lasso e Elastic Net) e algoritmos ensemble (Random Forest) alimentados por grandes painéis de dados econômicos. Embora demonstrem que dados externos contêm sinal preditivo, tais estudos frequentemente enfrentam o custo da multicolinearidade e da perda de aderência quando não há uma modelagem prévia da inércia autoregressiva estrutural [6, 14].")

add_p(text="Para evidenciar com precisão como o presente projeto se insere nessa fronteira e quais lacunas metodológicas preenche, a Tabela 1 sintetiza uma análise comparativa baseada em critérios funcionais e computacionais, confrontando os trabalhos da literatura com a abordagem proposta para o projeto.")

# Inserção da Tabela 1 (Matriz de Trabalhos Relacionados e Diferenciais)
p_cap1 = add_p(text="Tabela 1 – Matriz Comparativa de Trabalhos Relacionados e Diferenciais Metodológicos do Projeto", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=3)
p_cap1.runs[0].bold = True
p_cap1.runs[0].font.size = Pt(9.5)
p_cap1.paragraph_format.keep_with_next = True

dados_tab_comp = [
    [
        "Estrutura de Modelagem",
        "Linear univariada estrita (ARIMA / SARIMA).",
        "Híbrida aditiva univariada (ARIMA linear + RNA nos resíduos).",
        "Regressores puramente não lineares ou regularizados (Lasso, RF).",
        "Híbrida aditiva multivariada (ARIMAX com exógenas + RF nos resíduos)."
    ],
    [
        "Espaço de Variáveis Exógenas",
        "Ausente (apenas o histórico passado da própria série y_t).",
        "Ausente (opera unicamente com defasagens da série dependente).",
        "Amplo painel multivariado sem filtragem otimizada de atributos.",
        "28 covariáveis estruturadas em 4 pilares macroeconômicos fundamentais."
    ],
    [
        "Seleção Inteligente de Atributos",
        "Inexistente (seleção via critérios AIC/BIC em ordens p, d, q).",
        "Inexistente (foco apenas no ajuste de resíduos temporais).",
        "Penalização paramétrica passiva (L1/Lasso) ou importância em árvores.",
        "Meta-heurísticas bioinspiradas ativas (Algoritmo Genético e PSO) para seleção global."
    ],
    [
        "Tratamento de Choques Não Lineares",
        "Incapaz de modelar quebras estruturais ou choques de custos exógenos.",
        "Modela não linearidades endógenas, mas cego a choques externos (câmbio/petróleo).",
        "Captura interações não lineares, mas negligencia a inércia autoregressiva pura.",
        "ARIMAX ancora a inércia estocástica e a Random Forest absorve os choques exógenos residuais."
    ],
    [
        "Prevenção de Vazamento (Data Leakage)",
        "Divisão amostral simples ou estimação em toda a amostra.",
        "Divisão estática simples de treino e teste.",
        "Frequentemente adota validação cruzada k-fold sem preservação estrita da ordem temporal.",
        "Validação sequencial dinâmica Walk-Forward de 1 passo (h=1) com reestimação cronológica."
    ],
    [
        "Contextualização Econômica Aplicada",
        "Foco estatístico genérico em séries sintéticas ou industriais.",
        "Aplicações empíricas clássicas em séries padronizadas internacionais.",
        "Avaliação em mercados desenvolvidos com baixa volatilidade e sem indexação.",
        "Painel brasileiro contemporâneo (2012–2026, 174 meses), com validação de economista da FCAP/UPE."
    ]
]

headers_tab1 = ["Dimensão Metodológica / Requisito", "Modelos Clássicos (Box & Jenkins, 2015) [1]", "Híbridos Tradicionais (Zhang, 2003) [18]", "Machine Learning Multivariado (Medeiros et al., 2021) [14]", "Abordagem Proposta (ARIMAX Híbrido + Meta-heurísticas)"]
widths_tab1 = [Inches(1.2), Inches(1.1), Inches(1.1), Inches(1.2), Inches(1.4)]

tbl1 = doc.add_table(rows=len(dados_tab_comp) + 1, cols=5)
tbl1.alignment = WD_TABLE_ALIGNMENT.CENTER
make_row_header(tbl1.rows[0])

for j, h_text in enumerate(headers_tab1):
    helper_format_cell(tbl1.rows[0].cells[j], h_text, bold=True, bg_hex="1F4E79", text_color=RGBColor(255, 255, 255), width=widths_tab1[j], font_size=8.0)

for i, row in enumerate(dados_tab_comp):
    make_row_cant_split(tbl1.rows[i + 1])
    row_cells = tbl1.rows[i + 1].cells
    bg = "F9FAFB" if (i % 2 == 1) else None
    for j, val in enumerate(row):
        is_bold = (j == 0 or j == 4)
        align = WD_ALIGN_PARAGRAPH.LEFT if (j == 0) else WD_ALIGN_PARAGRAPH.JUSTIFY
        t_color = COLOR_NAVY if (j == 4) else None
        helper_format_cell(row_cells[j], val, bold=is_bold, align=align, bg_hex=bg, width=widths_tab1[j], text_color=t_color, font_size=8.0)

add_p(text="Fonte: Elaboração própria com base na revisão sistemática da literatura (2026).", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=6)

# =============================================================================
# 3 MATERIAIS E MÉTODOS
# =============================================================================
print("Escrevendo Seção 3 (MATERIAIS E MÉTODOS)...")
add_p(text="3 MATERIAIS E MÉTODOS", heading_level=1)

add_p(text="3.1 Stakeholders Envolvidos", heading_level=2)
add_p(text="A condução e a validação do projeto contam com a participação e o direcionamento de diferentes partes interessadas (stakeholders), articulando a liderança acadêmica na disciplina, a consultoria de domínio macroeconômico e a aplicabilidade prática:")

add_p(bold_prefix="1. Professor da Disciplina e Orientador Metodológico: ", text="")
add_p(text="• Prof. Dr. Alexandre Maciel (Escola Politécnica de Pernambuco – POLI/UPE): Docente responsável pela disciplina de Mineração de Dados no curso de Engenharia da Computação. Atua como o principal stakeholder acadêmico e orientador metodológico do projeto, tendo como responsabilidades:")
add_p(text="    - Orientar e avaliar a conformidade técnica do projeto com os preceitos científicos de Descoberta de Conhecimento em Bases de Dados (KDD) e Mineração de Dados;")
add_p(text="    - Avaliar o rigor do pipeline de engenharia de dados, garantindo reprodutibilidade e prevenção de vazamento temporal (lookahead bias);")
add_p(text="    - Validar as decisões de saneamento, tratamento de dados ausentes e estruturação formal do Dicionário de Dados;")
add_p(text="    - Avaliar a aderência do artigo aos padrões institucionais e critérios de avaliação da POLI-UPE.")

add_p(bold_prefix="2. Stakeholder Especialista de Domínio (Consultoria Macroeconômica): ", text="")
add_p(text="• Prof. Guilherme Martins (Faculdade de Ciências da Administração de Pernambuco – FCAP/UPE): Economista e docente da UPE, atuando como o consultor especialista de domínio do projeto. Sua responsabilidade e interesse residem em:")
add_p(text="    - Validar a pertinência teórica das 28 variáveis exógenas candidatas à luz da teoria macroeconômica e das peculiaridades do mercado brasileiro;")
add_p(text="    - Orientar sobre a dinâmica dos mecanismos de transmissão de preços (pass-through cambial, inércia de contratos e tarifas públicas reguladas);")
add_p(text="    - Assegurar que os procedimentos de pré-processamento preservem a integridade e o significado econômico das séries históricas;")
add_p(text="    - Avaliar a consistência das conclusões exploratórias frente à política monetária conduzida pelo BACEN e pelo COPOM.")

add_p(bold_prefix="3. Stakeholders de Aplicação e Beneficiários Finais (Decisores Econômicos): ", text="")
add_p(text="• Analistas de Mercado Financeiro e Gestores de Ativos: Interessados em dados macroeconômicos saneados e consistentes para precificação de títulos públicos indexados (como NTN-B e debêntures incentivadas) e gestão de riscos de carteira;")
add_p(text="• Departamentos de Planejamento e Controladorias Corporativas: Necessidade de parâmetros preditivos confiáveis de custos para elaboração de orçamentos anuais, reajustes contratuais com fornecedores e planejamento de estoques;")
add_p(text="• Sociedade e Gestores de Políticas Públicas: Beneficiários indiretos de estudos transparentes e reprodutíveis que analisam as pressões de custos sobre itens de consumo essencial (alimentação, energia e transporte).")

add_p(text="3.2 Descrição da Base de Dados", heading_level=2)
add_p(text="A base empírica foi coletada automaticamente da API do Sistema Gerenciador de Séries Temporais do Banco Central (SGS/BACEN). O painel compreende 174 observações mensais contínuas (frequência Month Start - MS), de março de 2012 a agosto de 2026.")
add_p(text="A variável dependente alvo (y_t) é o IPCA mensal (SGS código 4447). As 28 variáveis exógenas candidatas foram agrupadas em quatro categorias macroeconômicas:")
add_p(bold_prefix="• Índices de Preços e Desagregações Setoriais (11 variáveis): ", text="Subíndices do IPCA (Alimentação, Transportes, Habitação, Saúde, Vestuário, Educação e Despesas Pessoais) e índices gerais (INPC, IGP-M, IGP-DI e IPC-BR);")
add_p(bold_prefix="• Setor Financeiro, Moeda e Câmbio (3 variáveis): ", text="Taxa Selic Over, taxa de câmbio nominal PTAX (USDBRL) e reservas internacionais;")
add_p(bold_prefix="• Atividade Econômica e Mercado de Trabalho (7 variáveis): ", text="PIB Mensal a preços correntes, taxa de desocupação (PNAD Contínua), salário mínimo nacional, estoques de empregos formais ativos do CAGED (Total, Agropecuária e Construção Civil) e produção física de ovos;")
add_p(bold_prefix="• Energia e Combustíveis (6 variáveis): ", text="Refino de petróleo, consumo aparente de gasolina automotiva, consumo de óleo combustível e demanda faturada de energia elétrica (Comercial, Residencial e Total).")

add_p(text="3.2.1 Delimitação Temporal e Justificativa Metodológica (2012 a 2026)", heading_level=3)
add_p(text="O marco temporal inicial em março de 2012 foi adotado devido a três fatores metodológicos fundamentados com o stakeholder economista:")
add_p(bold_prefix="1. Transição da Medição do Desemprego: ", text="Implantação da PNAD Contínua pelo IBGE em substituição à antiga PME, eliminando quebra estrutural severa nos dados de mercado de trabalho;")
add_p(bold_prefix="2. Nova Ponderação da Cesta do IPCA: ", text="Atualização dos pesos da cesta de consumo com base na POF 2008-2009;")
add_p(bold_prefix="3. Painel Balanceado no SGS/BACEN: ", text="Disponibilidade ininterrupta do painel balanceado de séries setoriais.")

add_p(text="3.3 Análise Descritiva dos Dados", heading_level=2)
add_p(text="A análise descritiva investigou a dispersão, a assimetria e os valores extremos antes da modelagem preditiva. Para atender aos critérios formais de mineração de dados, foram caracterizados um atributo numérico contínuo e um atributo nominal institucionalmente fundamentado:")
add_p(bold_prefix="1. Atributo Numérico Contínuo (IPCA): ", text="Variação percentual mensal da inflação oficial (SGS 4447);")
add_p(bold_prefix="2. Atributo Nominal Categórico (Regime de Inflação): ", text="Discretização da série contínua em três classes balizadas pelas metas do CMN: Deflação (IPCA < 0,00%), Meta / Estável (0,00% ≤ IPCA ≤ 0,50%) e Alta / Acima da Meta (IPCA > 0,50%).")

add_p(text="3.3.1 Distribuição de Frequências e Métricas Descritivas", heading_level=3)
add_p(text="A análise da amostra atualizada (174 meses contínuos) aponta a predominância de meses dentro da meta oficial, conforme demonstrado na Tabela 2.")

# Inserção da Tabela 2 (Frequências)
p_cap2 = add_p(text="Tabela 2 – Distribuição de Frequência do Atributo Nominal (Regime de Inflação)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=5, space_after=3)
p_cap2.runs[0].bold = True
p_cap2.runs[0].font.size = Pt(9.5)
p_cap2.paragraph_format.keep_with_next = True

dados_tab2 = [
    ["Deflação", "IPCA < 0,00%", "27", "15,52%", "27", "15,52%"],
    ["Meta / Estável", "0,00% ≤ IPCA ≤ 0,50%", "77", "44,25%", "104", "59,77%"],
    ["Alta / Acima da Meta", "IPCA > 0,50%", "70", "40,23%", "174", "100,00%"],
    ["Total Geral Amostral", "Horizonte 2012–2026", "174", "100,00%", "174", "100,00%"]
]
widths_tab2 = [Inches(1.4), Inches(1.2), Inches(0.9), Inches(0.9), Inches(0.9), Inches(1.0)]
tbl2 = doc.add_table(rows=len(dados_tab2) + 1, cols=6)
tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_tab2 = ["Classe Nominal", "Faixa Paramétrica", "Freq. Absoluta (fi)", "Freq. Relativa (%)", "Freq. Acumulada (Fi)", "Freq. Rel. Acum. (%)"]

make_row_header(tbl2.rows[0])
for j, h_text in enumerate(headers_tab2):
    helper_format_cell(tbl2.rows[0].cells[j], h_text, bold=True, bg_hex="1F4E79", text_color=RGBColor(255, 255, 255), width=widths_tab2[j])

for i, row in enumerate(dados_tab2):
    make_row_cant_split(tbl2.rows[i + 1])
    row_cells = tbl2.rows[i + 1].cells
    is_tot = (i == len(dados_tab2) - 1)
    bg = "F2F4F7" if is_tot else ("F9FAFB" if (i % 2 == 1) else None)
    for j, val in enumerate(row):
        is_bold = (j == 0 or is_tot)
        align = WD_ALIGN_PARAGRAPH.LEFT if (j == 0) else WD_ALIGN_PARAGRAPH.CENTER
        helper_format_cell(row_cells[j], val, bold=is_bold, align=align, bg_hex=bg, width=widths_tab2[j])

add_p(text="Fonte: Elaboração própria com base no SGS/BACEN (2026).", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=5)

add_p(text="Principais estimadores estatísticos do IPCA contínuo na amostra:")
add_p(bold_prefix="• Média e Mediana: ", text="Média de 0,4324% ao mês e mediana de 0,4150% ao mês;")
add_p(bold_prefix="• Dispersão: ", text="Desvio padrão amostral de 0,4719% e variância de 0,2226;")
add_p(bold_prefix="• Assimetria e Curtose: ", text="Assimetria positiva (+0,5287), acusando cauda direita alongada por choques inflacionários, e curtose de +0,3736;")
add_p(bold_prefix="• Valores Extremos: ", text="Mínimo histórico de -0,7400% (junho/2023) e máximo de +1,9500% (dezembro/2019);")
add_p(bold_prefix="• Quartis e Intervalo Interquartílico: ", text="Q1 = 0,0800%, Q3 = 0,6775% e IQR = 0,5975 p.p.")

add_p(text="3.3.2 Análise Visual: Histograma, Boxplot e Gráfico de Dispersão", heading_level=3)
add_p(text="A caracterização visual dos dados foi conduzida através de gráficos gerados a partir do histórico consolidado:")

add_img("Figura_1_Histograma_IPCA.png", "Figura 1 – Histograma e Densidade Empírica (KDE) do IPCA (2012 a 2026)")
add_p(text="A Figura 1 confirma que a distribuição da inflação concentra-se entre 0,10% e 0,60% ao mês. A proximidade entre média e mediana reforça a regularidade central, enquanto a assimetria positiva (+0,53) demonstra que choques inflacionários são mais acentuados do que quedas de preço.")

add_img("Figura_2_Boxplot_IPCA.png", "Figura 2 – Diagrama de Caixa (Boxplot) do IPCA: Amostra Global e por Regimes de Inflação")
add_p(text="O Boxplot univariado na Figura 2 identifica 5 outliers pelo critério de Tukey (IQR): dezembro/2019 (+1,95%), outubro/2020 (+1,72%), novembro/2020 (+1,61%), dezembro/2020 (+1,58%) e dezembro/2021 (+1,58%), decorrentes de choques em carnes e restrições de cadeias de suprimentos globais. A dispersão na classe 'Alta' é muito mais ampla do que na classe 'Meta', justificando a modelagem não linear dos resíduos.")

add_img("Figura_3_Dispersao_IPCA_Cambio.png", "Figura 3 – Gráfico de Dispersão entre IPCA e Taxa de Câmbio (USDBRL) por Regime Nominal")
add_p(text="O gráfico de dispersão da Figura 3 evidencia a relação positiva entre desvalorização cambial e inflação (mecanismo de pass-through cambial). À medida que a cotação do dólar sobe, a frequência de meses no regime de 'Alta' aumenta perceptivelmente.")

add_img("Figura_4_Distribuicao_Regimes.png", "Figura 4 – Proporção Percentual dos Regimes Nominais de Inflação (N = 174 meses)")
add_p(text="A Figura 4 sintetiza a distribuição amostral: 44,25% dos meses situaram-se na meta, 40,23% em patamares elevados e 15,52% em deflação (provocada por desonerações tributárias temporárias e contrações severas de demanda).")

add_p(text="3.3.3 Governança, Integridade e Requisitos de Qualidade", heading_level=3)
add_p(text="O tratamento dos dados segue rigorosamente a Lei Geral de Proteção de Dados Pessoais (LGPD – Lei nº 13.709/2018). As séries temporais empregadas são dados macroeconômicos públicos e agregados (SGS/BACEN, IBGE, FGV e Ministério do Trabalho), sem identificadores individuais. Sob a perspectiva de engenharia de dados, garantimos: (i) prevenção estrita de vazamento prospectivo (lookahead bias); (ii) completude amostral de 100% sem lacunas no período de 2012 a 2026; e (iii) reprodutibilidade científica por meio de scripts Python automatizados.")

# 3.4 Pré-processamento dos Dados
add_p(text="3.4 Pré-processamento dos Dados", heading_level=2)
add_p(text="O pré-processamento de dados constitui a etapa culminante da presente entrega. Nesta fase, as séries temporais brutas foram submetidas a rotinas sistemáticas de engenharia de dados para transformá-las em um painel estruturado, consistente e livre de inconsistências, sem qualquer vazamento de dados futuros.")

add_p(text="3.4.1 Procedimentos de Limpeza e Saneamento de Dados (Data Cleaning)", heading_level=3)
add_p(text="O pipeline de limpeza executado compreendeu quatro procedimentos principais:")
add_p(bold_prefix="1. Sincronização Cronológica: ", text="Séries divulgadas em periodicidade diária no mercado financeiro (taxa de câmbio nominal PTAX e taxa Selic Over) foram convertidas para médias mensais de dias úteis e sincronizadas sob frequência contínua Month Start (MS) de março de 2012 a agosto de 2026;")
add_p(bold_prefix="2. Tratamento de Zeros Estruturais: ", text="Em séries contínuas de fluxos e estoques físicos (refino de petróleo, consumo de combustíveis, demanda de energia e estoques de emprego do CAGED), zeros espúrios gerados por atrasos de apuração de órgãos governamentais foram identificados e substituídos por valores nulos (NaN);")
add_p(bold_prefix="3. Sanitização Numérica: ", text="Verificação sistemática contra potenciais valores infinitos (±inf) ou divisões por zero, assegurando que todas as entradas pertencem ao espaço numérico real Float64;")
add_p(bold_prefix="4. Imputação Temporal de Dados Ausentes: ", text="Valores faltantes pontuais em séries mensais foram tratados via interpolação linear temporal contínua indexada pelo calendário (interpolate(method='time')). A preservação da ordem cronológica garante a integridade histórica dos dados sem distorções.")

add_p(text="3.4.2 Técnicas de Redução de Dados e Engenharia de Atributos", heading_level=3)
add_p(bold_prefix="1. Redução Amostral Estrutural (Truncamento pós-2012): ", text="Conforme validado junto ao consultor de domínio, descartaram-se os dados anteriores a março de 2012 para eliminar quebras estruturais metodológicas severas (transição da PME para PNAD Contínua e revisão dos pesos da cesta do IPCA pela POF 2008-2009);")
add_p(bold_prefix="2. Discretização do Atributo Nominal: ", text="Construção da variável categórica 'Regime de Inflação' com base nas faixas institucionais do CMN, permitindo a segmentação exploratória de períodos de normalidade, estresse e deflação;")
add_p(bold_prefix="3. Codificação de Sazonalidade Harmônica: ", text="Criação dos atributos sazonais mes_sin = sin(2πm / 12) e mes_cos = cos(2πm / 12), viabilizando a captura contínua e suave de ciclos anuais sem o custo de inflar a dimensionalidade com 11 variáveis dummy binárias.")

add_p(text="3.4.3 Dicionário de Dados da Base Consolidada Pré-Processada", heading_level=3)
add_p(text="Como resultado final de todo o fluxo de coleta, higienização e saneamento, a Tabela 3 consolida o Dicionário de Dados da base pré-processada, especificando para cada um dos 31 atributos o seu código de origem, tipo de dado, tratamento recebido no pré-processamento, pilar macroeconômico e papel de negócio validado pelo Prof. Guilherme Martins.")

# Inserção da Tabela 3 (Dicionário Final de Pré-processamento - 31 variáveis)
p_cap3 = add_p(text="Tabela 3 – Dicionário de Dados da Base Consolidada Pré-Processada (174 Meses, 2012–2026)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=5, space_after=3)
p_cap3.runs[0].bold = True
p_cap3.runs[0].font.size = Pt(9.5)
p_cap3.paragraph_format.keep_with_next = True

headers_tab3 = ["Atributo", "Código / Fonte", "Tipo / Unidade", "Tratamento no Pré-processamento", "Pilar Econômico", "Papel / Descrição Econômica"]
widths_tab3 = [Inches(1.20), Inches(0.85), Inches(0.75), Inches(1.30), Inches(1.00), Inches(1.40)]

dados_dicionario_preproc = [
    ["IPCA", "SGS 4447 (IBGE)", "Float64 (% a.m.)", "Interpolação de nulos; alinhamento Month-Start (MS)", "Preços Setoriais", "Variável dependente alvo (Target y_t) - Inflação oficial sob regime de metas."],
    ["IPCA_Transportes", "SGS 1639 (IBGE)", "Float64 (% a.m.)", "Sincronização MS; tratamento de nulos via interpolação", "Preços Setoriais", "Covariável exógena - Choques de preços de combustíveis e tarifas de mobilidade."],
    ["IPCA_Alimentação_bebidas", "SGS 1635 (IBGE)", "Float64 (% a.m.)", "Sincronização MS; tratamento de nulos via interpolação", "Preços Setoriais", "Covariável exógena - Choques climáticos e safras no consumo domiciliar."],
    ["INPC_Habitação", "SGS 1636 (IBGE)", "Float64 (% a.m.)", "Sincronização MS; tratamento de nulos via interpolação", "Preços Setoriais", "Covariável exógena - Pressões de aluguel e tarifas de energia residencial."],
    ["IPCA_Saúde_cuidados_pessoais", "SGS 1641 (IBGE)", "Float64 (% a.m.)", "Sincronização MS; tratamento de nulos via interpolação", "Preços Setoriais", "Covariável exógena - Repasse de custos médicos e planos de saúde regulados."],
    ["IPCA_Vestuário", "SGS 1638 (IBGE)", "Float64 (% a.m.)", "Sincronização MS; tratamento de nulos via interpolação", "Preços Setoriais", "Covariável exógena - Sazonalidade de coleções e liquidações do varejo."],
    ["IPCA_Educação", "SGS 1643 (IBGE)", "Float64 (% a.m.)", "Sincronização MS; tratamento de nulos via interpolação", "Preços Setoriais", "Covariável exógena - Reajustes concentrados em início de ano letivo."],
    ["IPCA_Despesas_Pessoais", "SGS 1642 (IBGE)", "Float64 (% a.m.)", "Sincronização MS; tratamento de nulos via interpolação", "Preços Setoriais", "Covariável exógena - Sensibilidade de demanda de serviços recreativos e pessoais."],
    ["USDBRL (Câmbio PTAX)", "SGS 3696 (BACEN)", "Float64 (R$/US$)", "Conversão diária para média mensal de dias úteis; MS", "Câmbio / Finanças", "Covariável exógena - Mecanismo de pass-through cambial e importações."],
    ["SELIC", "SGS 4390 (BACEN)", "Float64 (% a.m.)", "Conversão de taxa diária para média mensal; MS", "Câmbio / Finanças", "Covariável exógena - Taxa básica de juros da política monetária do COPOM."],
    ["Reservas_Internacionais", "SGS 3546 (BACEN)", "Float64 (US$ Milhões)", "Alinhamento mensal MS; saneamento de lacunas", "Câmbio / Finanças", "Covariável exógena - Liquidez externa e blindagem a choques globais."],
    ["INPC", "SGS 188 (IBGE)", "Float64 (% a.m.)", "Sincronização MS; interpolação linear de nulos", "Preços Setoriais", "Covariável exógena - Inflação incidente em famílias de 1 a 5 salários mínimos."],
    ["IGP_M", "SGS 189 (FGV)", "Float64 (% a.m.)", "Sincronização MS; alinhamento de competência", "Preços Setoriais", "Covariável exógena - Indicador antecedente de custos no atacado (FGV)."],
    ["IGP_DI", "SGS 190 (FGV)", "Float64 (% a.m.)", "Sincronização MS; verificação de integridade", "Preços Setoriais", "Covariável exógena - Preços ao produtor e insumos de disponibilidade interna."],
    ["IPC_BR", "SGS 191 (FGV)", "Float64 (% a.m.)", "Sincronização MS; saneamento de inconsistências", "Preços Setoriais", "Covariável exógena - Índice de preços ao consumidor abrangente da FGV."],
    ["PIB_Mensal", "SGS 4380 (BACEN)", "Float64 (R$ Milhões)", "Tratamento de atrasos de divulgação; sincronização MS", "Atividade Econômica", "Covariável exógena - Proxy de nível de atividade econômica mensal e hiato."],
    ["Desemprego (PNAD)", "SGS 24369 (IBGE)", "Float64 (% da PEA)", "Truncamento pós-2012; interpolação de quebras", "Mercado de Trabalho", "Covariável exógena - Dinâmica da desocupação formal (Curva de Phillips)."],
    ["Salario_Minimo", "SGS 1619 (Governo)", "Float64 (R$ correntes)", "Sincronização MS; preservação de reajustes federais anuais", "Mercado de Trabalho", "Covariável exógena - Custos de contratação básica no setor terciário."],
    ["Estoque_Empregos_Total", "SGS 28763 (CAGED)", "Float64 (Mil vínculos)", "Zeros contábeis substituídos por NaN; interpolação", "Mercado de Trabalho", "Covariável exógena - Saldo mensal de geração de emprego formal no Brasil."],
    ["Estoque_Agropecuária", "SGS 28764 (CAGED)", "Float64 (Mil vínculos)", "Substituição de zeros por NaN; sincronização contínua", "Mercado de Trabalho", "Covariável exógena - Dinâmica do emprego rural e safras do agronegócio."],
    ["Estoque_Construção", "SGS 28770 (CAGED)", "Float64 (Mil vínculos)", "Alinhamento cronológico; saneamento de inconsistências", "Mercado de Trabalho", "Covariável exógena - Nível de atividade e investimentos na construção civil."],
    ["Qte_Ovos", "SGS 1310 (IBGE)", "Float64 (Mil dúzias)", "Interpolação de atrasos; alinhamento de frequência MS", "Atividade Econômica", "Covariável exógena - Proxy física da oferta agropecuária de ciclo rápido."],
    ["Produção_Derivados_Petróleo", "SGS 1391 (ANP)", "Float64 (Mil m³)", "Alinhamento MS; interpolação linear de lacunas", "Energia / Combustíveis", "Covariável exógena - Volume de refino de petróleo e oferta energética."],
    ["Consumo_Gasolina", "SGS 1393 (ANP)", "Float64 (m³)", "Sincronização MS; zeros de atraso tratados como NaN", "Energia / Combustíveis", "Covariável exógena - Consumo automotivo e pressão de curto prazo em transporte."],
    ["Consumo_Óleo_Combustível", "SGS 1395 (ANP)", "Float64 (t)", "Alinhamento temporal e interpolação de competência", "Energia / Combustíveis", "Covariável exógena - Indicador logístico do transporte rodoviário pesado."],
    ["Consumo_Energia_Comercial", "SGS 1402 (EPE)", "Float64 (MWh)", "Sincronização MS; zeros tratados como NaN", "Energia / Combustíveis", "Covariável exógena - Carga elétrica no comércio (termômetro em tempo real)."],
    ["Consumo_Energia_Residencial", "SGS 1403 (EPE)", "Float64 (MWh)", "Alinhamento MS; interpolação temporal contínua", "Energia / Combustíveis", "Covariável exógena - Padrão de consumo elétrico das famílias brasileiras."],
    ["Consumo_Energia_Total", "SGS 1406 (EPE)", "Float64 (MWh)", "Sincronização mensal MS; verificação de integridade", "Energia / Combustíveis", "Covariável exógena - Demanda física global de energia elétrica produtiva."],
    ["Regime de Inflação", "IBGE / CMN", "Categórico Nominal", "Discretização paramétrica: Deflação, Meta e Alta", "Governança / CMN", "Atributo nominal derivado - Caracterização qualitativa da trajetória."],
    ["mes_sin", "Engenharia Temporal", "Float64 (Adimensional)", "Harmônica periódica senoidal: sin(2πm / 12)", "Sazonalidade", "Covariável sazonal contínua - Captura de ciclos periódicos anuais."],
    ["mes_cos", "Engenharia Temporal", "Float64 (Adimensional)", "Harmônica periódica cossenoidal: cos(2πm / 12)", "Sazonalidade", "Covariável sazonal contínua - Captura de ciclos periódicos anuais."]
]

tbl3_final = doc.add_table(rows=len(dados_dicionario_preproc) + 1, cols=6)
tbl3_final.alignment = WD_TABLE_ALIGNMENT.CENTER
make_row_header(tbl3_final.rows[0])

for j, h_text in enumerate(headers_tab3):
    helper_format_cell(tbl3_final.rows[0].cells[j], h_text, bold=True, bg_hex="1F4E79", text_color=RGBColor(255, 255, 255), width=widths_tab3[j], font_size=8.0)

for i, row in enumerate(dados_dicionario_preproc):
    make_row_cant_split(tbl3_final.rows[i + 1])
    row_cells = tbl3_final.rows[i + 1].cells
    bg = "F9FAFB" if (i % 2 == 1) else None
    for j, val in enumerate(row):
        is_bold = (j == 0)
        align = WD_ALIGN_PARAGRAPH.LEFT if (j == 0 or j == 5) else WD_ALIGN_PARAGRAPH.CENTER
        helper_format_cell(row_cells[j], val, bold=is_bold, align=align, bg_hex=bg, width=widths_tab3[j], font_size=8.0)

add_p(text="Fonte: Elaboração própria com base no pipeline computacional desenvolvido e validado com os stakeholders (2026).", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=6)

# =============================================================================
# REFERÊNCIAS BIBLIOGRÁFICAS (DIRETO APÓS O PRÉ-PROCESSAMENTO)
# =============================================================================
print("Escrevendo Referências Bibliográficas imediatamente após o Pré-processamento...")
add_p(text="Referências Bibliográficas", heading_level=1)

referencias = [
    "[1] BOX, G. E.; JENKINS, G. M.; REINSEL, G. C.; LJUNG, G. M. Time Series Analysis: Forecasting and Control. 5. ed. Hoboken: John Wiley & Sons, 2015.",
    "[2] BANCO CENTRAL DO BRASIL (BACEN). Sistema Gerenciador de Séries Temporais (SGS). Disponível em: <https://www3.bcb.gov.br/sgspub/>. Acesso em: 16 set. 2026.",
    "[3] BANCO CENTRAL DO BRASIL (BACEN). Relatório de Inflação. v. 26, n. 2. Brasília: Banco Central do Brasil, 2024.",
    "[4] BLANCHARD, O. Macroeconomia. 7. ed. São Paulo: Pearson, 2017.",
    "[5] BRESSER-PEREIRA, L. C.; NAKANO, Y. A Teoria da Inflação Inercial. São Paulo: Brasiliense, 1984.",
    "[6] GARCIA, M. G.; MEDEIROS, M. C.; VASCONCELOS, G. F. Real-time inflation forecasting with high-dimensional data: the case of Brazil. International Journal of Forecasting, v. 33, n. 3, p. 679–693, 2017.",
    "[7] HASTIE, T.; TIBSHIRANI, R.; FRIEDMAN, J. The Elements of Statistical Learning: Data Mining, Inference, and Prediction. 2. ed. New York: Springer, 2009.",
    "[8] HOLLAND, J. H. Adaptation in Natural and Artificial Systems: An Introductory Analysis with Applications to Biology, Control, and Artificial Intelligence. Cambridge: MIT Press, 1992.",
    "[9] HYNDMAN, R. J.; ATHANASOPOULOS, G. Forecasting: Principles and Practice. 3. ed. Melbourne: OTexts, 2021.",
    "[10] INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). Sistema Nacional de Índices de Preços ao Consumidor (SNIPC): Metodologia do IPCA e INPC. Rio de Janeiro: IBGE, 2020.",
    "[11] KENNEDY, J.; EBERHART, R. Particle swarm optimization. In: Proceedings of ICNN'95 - International Conference on Neural Networks, v. 4, p. 1942–1948, 1995.",
    "[12] KHANDANI, A. E.; KIM, A. J.; LO, A. W. Consumer credit-risk models via machine-learning algorithms. Journal of Banking & Finance, v. 34, n. 11, p. 2767–2787, 2010.",
    "[13] MANKIW, N. G. Macroeconomia. 10. ed. Rio de Janeiro: LTC, 2021.",
    "[14] MEDEIROS, M. C.; VASCONCELOS, G. F.; VEIGA, Á.; ZILBERMAN, E. Forecasting inflation in a data-rich environment: the benefits of machine learning methods. Journal of Business & Economic Statistics, v. 39, n. 1, p. 98–119, 2021.",
    "[15] PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, v. 12, p. 2825–2830, 2011.",
    "[16] SIMONSEN, M. H. 30 Anos de Indexação. Rio de Janeiro: Editora FGV, 1995.",
    "[17] TAYLOR, J. B. Discretion versus policy rules in practice. Carnegie-Rochester Conference Series on Public Policy, v. 39, p. 195–214, 1993.",
    "[18] ZHANG, G. P. Time series forecasting using a hybrid ARIMA and neural network model. Neurocomputing, v. 50, p. 159–175, 2003."
]

for ref in referencias:
    p_ref = add_p(text=ref, font_size=9.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=2, space_after=3)
    p_ref.paragraph_format.line_spacing = 1.05

# Salvar como Artigo Principal oficial
caminho_principal = os.path.join(DIR_ARTIGO, 'Artigo_Previsao_Inflacao.docx')
caminho_entrega_artigo = os.path.join(BASE_DIR, 'Entrega_Classroom', '3_Artigo_Completo', 'Artigo_Previsao_Inflacao.docx')

doc.save(caminho_principal)
print(f"Artigo Principal Word salvo com sucesso em: {caminho_principal}")

doc.save(caminho_entrega_artigo)
print(f"Cópia da Entrega Word atualizada com sucesso em: {caminho_entrega_artigo}")
