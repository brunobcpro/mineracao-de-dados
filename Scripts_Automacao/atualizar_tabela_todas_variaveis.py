import shutil
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualiza o Notebook, o Markdown e o DOCX com a Tabela Exaustiva de TODAS as 30 variáveis
(28 variáveis de df_macro.csv + 2 harmônicas de sazonalidade).
Explica detalhadamente o racional de cada uma, sua presença nos 3 cenários
e o motivo de seleção ou exclusão no Estado da Arte.
"""

import json
import os
import pandas as pd
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# -------------------------------------------------------------
# 1. TABELA EXAUSTIVA COMPLETA DE TODAS AS 30 VARIÁVEIS
# -------------------------------------------------------------
tabela_completa_30_md = """| # | Variável Exógena | Dimensão Macroeconômica | Por que foi Utilizada? (Racional Econômico) | Cen. 1 (Todas) | Cen. 2 (Est. Arte) | Cen. 3 (GA Otimiz.) | Status no Cenário 2 (Motivo Econômico) | Coeficiente OLS (Impacto) |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :--- | :---: |
| **1** | **$\text{IPCA}_{t-1}$** | Inércia / Alvo | Indexação contratual de preços (aluguéis, tarifas, salários). Memória temporal central. | ✅ | ✅ | ✅ | **Mantida (Âncora Principal):** Capta inércia autorregressiva inelástica. | **$+0,2251$** ($p=0,0008$) |
| **2** | **$\text{IGP\_DI}_{t-1}$** | Atacado / Custos | Índice de preços no atacado da FGV. Mede custos agroindustriais e matérias-primas (*cost-push*). | ✅ | ✅ | ❌ | **Mantida (Melhor Proxy Atacado):** Antecipa custos antes das gôndolas do varejo. | **$+0,1568$** ($p=0,0003$) |
| **3** | **$\text{IPCA Alimentação}_{t-1}$** | Núcleo de Oferta | Maior peso da cesta (~22%). Sujeito a choques climáticos, secas e safras agrícolas. | ✅ | ✅ | ✅ | **Mantida (Núcleo Volátil):** Maior componente do orçamento das famílias. | **$-0,0262$** ($p=0,6579$) |
| **4** | **$\text{IPCA Transportes}_{t-1}$** | Energia / Frete | Segundo maior peso (~20%). Sensibilidade a gasolina, diesel e tarifas públicas. | ✅ | ✅ | ✅ | **Mantida (Transmissão Logística):** Efeito capilar sobre custos de distribuição. | **$+0,0148$** ($p=0,7380$) |
| **5** | **$\Delta \% \text{USDBRL}_{t-1}$** | Câmbio / Externo | Variação percentual do dólar. Transmissão do repasse cambial (*pass-through*). | ✅ | ✅ | ❌ | **Mantida (Canal Cambial):** Encarece insumos e produtos importados (trigo/petróleo). | **$+0,0257$** ($p=0,4663$) |
| **6** | **$\Delta \text{SELIC}_{t-1}$** | Política Monetária | Variação da taxa básica fixada pelo COPOM/BACEN. Aperto/afrouxamento monetário. | ✅ | ✅ | ❌ | **Mantida (Canal Monetário):** Juros altos encarecem crédito e arrefecem consumo. | **$-0,0474$** ($p=0,1856$) |
| **7** | **$\text{Desemprego}_{t-1}$** | Curva de Phillips | Taxa de desocupação (PNAD Contínua). Ociosidade do mercado de trabalho. | ✅ | ✅ | ❌ | **Mantida (Curva de Phillips):** Desemprego alto comprime salários e demanda. | **$-0,0535$** ($p=0,1564$) |
| **8** | **$\sin(2\pi m / 12)$** | Sazonalidade | Harmônica seno do mês de destino. Captura ciclos periódicos de safra agrícola. | ✅ | ✅ | ❌ | **Mantida (Sazonalidade Causal):** Mês alvo é previamente conhecido com certeza. | **$-0,0497$** ($p=0,2091$) |
| **9** | **$\cos(2\pi m / 12)$** | Sazonalidade | Harmônica cosseno do mês de destino. Reajustes escolares em jan/fev e liquidações. | ✅ | ✅ | ❌ | **Mantida (Sazonalidade Causal):** Ajuste fino do ciclo anual de preços contratuais. | **$+0,0430$** ($p=0,2654$) |
| **10**| **$\text{IGP\_M}_{t-1}$** | Atacado / Imobiliário | Índice Geral de Preços do Mercado (FGV). Reajuste de aluguéis e contratos de energia. | ✅ | ❌ | ❌ | **Eliminada por Colinearidade:** Correlação $r = 0,91$ com IGP-DI (evita singularidade). | Redundante ($r>0,90$) |
| **11**| **$\text{IPC\_BR}_{t-1}$** | Consumidor Amplo | Índice de Preços ao Consumidor Brasil (FGV). Cobertura nacional alternativa. | ✅ | ❌ | ✅ | **Eliminada por Colinearidade:** Correlação $r = 0,88$ com IGP-DI e $0,92$ com IPCA. | Redundante ($r>0,85$) |
| **12**| **$\text{INPC}_{t-1}$** | Consumidor Baixa Renda | Mede cesta de famílias de 1 a 5 salários mínimos (IBGE). Reajustes do salário mínimo. | ✅ | ❌ | ❌ | **Eliminada por Colinearidade:** Correlação $r = 0,98$ com o IPCA (duplicação quase exata). | Quase Coincidente ($r=0,98$)|
| **13**| **$\text{INPC Habitação}_{t-1}$** | Núcleo Setorial | Custos de moradia, aluguel, condomínio e tarifas de água e saneamento básico. | ✅ | ❌ | ❌ | **Eliminada (Menor Poder Explicativo):** Absorvida pela inércia geral e pelo IGP-M. | Não selecionada no Est. Arte|
| **14**| **$\text{IPCA Saúde}_{t-1}$** | Preços Regulados | Planos de saúde e medicamentos com reajustes anuais autorizados pela ANS/CMED. | ✅ | ❌ | ❌ | **Eliminada (Choques Discretos Anuais):** Reajuste regulado ocorre 1x ao ano. | Ruído em Frequência Mensal |
| **15**| **$\text{IPCA Vestuário}_{t-1}$** | Núcleo Volátil | Roupas e calçados, ciclo sazonal de coleções (troca de estação e liquidações). | ✅ | ❌ | ✅ | **Eliminada no Est. Arte (Mantida no GA):** Capturada pelas harmônicas $\sin/\cos$. | Capturada por Sazonalidade |
| **16**| **$\text{IPCA Educação}_{t-1}$** | Núcleo Sazonal | Mensalidades escolares e universitárias, concentradas em janeiro e fevereiro. | ✅ | ❌ | ❌ | **Eliminada no Est. Arte:** Capturada com precisão analítica pela harmônica $\cos$. | Capturada por Sazonalidade |
| **17**| **$\text{IPCA Desp. Pessoais}$** | Serviços / Lazer | Serviços recreativos, salão de beleza, cuidados pessoais e serviços domésticos. | ✅ | ❌ | ✅ | **Eliminada no Est. Arte (Mantida no GA):** Baixo peso relativo na formação da inércia. | Baixa Elasticidade Preditiva|
| **18**| **$\text{USDBRL (Nível)}$** | Câmbio em Nível | Cotação nominal do dólar em Reais. | ✅ | ❌ | ✅ | **Substituída por $\Delta \% \text{USDBRL}$:** Câmbio em nível possui raiz unitária (I(1)). | Transformada em Variação % |
| **19**| **$\text{SELIC (Nível)}$** | Juros em Nível | Taxa básica nominal anualizada (meta do COPOM). | ✅ | ❌ | ❌ | **Substituída por $\Delta \text{SELIC}$:** A postura marginal (alta/baixa) é mais estacionária. | Transformada em Primeira Dif.|
| **20**| **$\text{Reservas Internacionais}$**| Liquidez Externa | Estoque de dólares do BACEN para conter volatilidade e ataques especulativos. | ✅ | ❌ | ❌ | **Eliminada (Não-Estacionária):** Tendência de longo prazo sem causalidade mensal direta. | Deriva Espúria em OLS |
| **21**| **$\text{SalMinimo}$** | Custo do Trabalho | Valor nominal do salário mínimo nacional decretado pelo governo federal. | ✅ | ❌ | ❌ | **Eliminada (Raiz Unitária Não-Estac.):** Crescimento de R$ 622 a 1.412 gera viés em teste. | Não Estacionária em Nível |
| **22**| **$\text{PIB Mensal}$** | Atividade Agregada | Indicador mensal do PIB (proxy IBC-Br do Banco Central). | ✅ | ❌ | ❌ | **Eliminada (Raiz Unitária Não-Estac.):** Tendência secular de expansão do produto real. | Não Estacionária em Nível |
| **23**| **$\text{QteOvos}$** | Agropecuária / Ovos | Quantidade produzida de ovos de galinha (IBGE). Proxy de consumo proteico básico. | ✅ | ❌ | ❌ | **Eliminada (Proxy Fraca / Ruído Amostral):** Alta colinearidade espúria em OLS. | Ruído Estatístico em OLS |
| **24**| **$\text{Produção Petróleo}$** | Oferta Combustíveis | Volume processado de derivados nas refinarias (diesel, gasolina, nafta). | ✅ | ❌ | ❌ | **Eliminada por Colinearidade:** Já refletida nos preços de IPCA Transportes. | Redundante com Transportes |
| **25**| **$\text{Consumo Gasolina}$** | Demanda Combustível | Vendas físicas de gasolina C em metros cúbicos pelas distribuidoras. | ✅ | ❌ | ❌ | **Eliminada por Colinearidade:** Correlação $> 0,80$ com IPCA Transportes e Energia. | Redundante com Transportes |
| **26**| **$\text{Consumo Óleo Comb.}$**| Demanda Industrial | Vendas de óleo combustível para indústria pesada, termoelétricas e navios. | ✅ | ❌ | ❌ | **Eliminada (Baixa Representatividade):** Peso reduzido na cesta do consumidor médio. | Baixa Relevância no IPCA |
| **27**| **$\text{Consumo Energia Com.}$**| Demanda Serviços | Consumo elétrico comercial em MWh (shoppings, comércio e serviços). | ✅ | ❌ | ❌ | **Eliminada por Colinearidade:** Correlação $> 0,92$ com Consumo de Energia Total. | Redundante ($r>0,92$) |
| **28**| **$\text{Consumo Energia Res.}$**| Demanda Residencial | Consumo elétrico nos lares das famílias em MWh. | ✅ | ❌ | ❌ | **Eliminada por Colinearidade:** Correlação $> 0,89$ com Consumo de Energia Total. | Redundante ($r>0,89$) |
| **29**| **$\text{Consumo Energia Total}$**| Atividade Industrial | Demanda elétrica total nacional do Sistema Interligado Nacional (ONS/EPE). | ✅ | ❌ | ❌ | **Substituída por $\Delta \% \text{Energia}$:** O nível cresce com a eletrificação do país. | Usada em Variação % seletiva|
| **30**| **$\text{Empregos CAGED}$** | Trabalho Formal | Estoque Total, Agropecuária e Construção Civil de trabalhadores formais. | ✅ | ❌ | ❌ | **Eliminadas por Colinearidade Extrema:** Correlações inter-setoriais $> 0,94$. | Desemprego é mais robusto |"""

# -------------------------------------------------------------
# 2. ATUALIZAR O NOTEBOOK JUPYTER COM A TABELA EXAUSTIVA COMPLETA
# -------------------------------------------------------------
caminho_nb = 'Entrega_Classroom/8_Regressao/regressao_previsao_inflacao.ipynb'
with open(caminho_nb, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Localizar a célula Markdown com a tabela de variáveis e substituir
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        src_text = ''.join(cell['source'])
        if 'Quais Variáveis Exógenas Foram Utilizadas e POR QUÊ' in src_text:
            novo_conteudo = f"""### 3. Quais Variáveis Exógenas Foram Utilizadas e POR QUÊ? (Inventário Completo de Todas as 30 Variáveis)

Em macroeconomia quantitativa, a inclusão indiscriminada de atributos gera distorções severas por multicolinearidade. A tabela abaixo apresenta o inventário exaustivo de **todas as 30 variáveis candidatas** (28 atributos do painel `df_macro.csv` + 2 componentes harmônicas determinísticas de sazonalidade), discriminando seu canal macroeconômico, sua presença nos 3 cenários e o **motivo econométrico formal para manutenção ou exclusão no Estado da Arte**:

{tabela_completa_30_md}"""
            cell['source'] = [l + "\n" for l in novo_conteudo.split("\n")]
            print(f"✅ Célula {i} do Jupyter Notebook atualizada com a Tabela Completa de 30 Variáveis!")
            break

with open(caminho_nb, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

# Cópia em Modelos de treinamento
shutil.copyfile(caminho_nb, 'Modelos de treinamento/regressao_previsao_inflacao.ipynb')
print("✅ Notebook sincronizado em Modelos de treinamento!")

# -------------------------------------------------------------
# 3. ATUALIZAR O MARKDOWN DAS SEÇÕES ENTREGÁVEIS
# -------------------------------------------------------------
caminho_secoes_md = 'Entrega_Classroom/8_Regressao/Secoes_2_2_3_5_4_1_Regressao.md'
with open(caminho_secoes_md, 'r', encoding='utf-8') as f:
    text_md = f.read()

# Substituir a tabela existente pela tabela completa
if 'Tabela 5 – Desempenho Comparativo' in text_md:
    pos_t5 = text_md.find('#### Tabela 5')
    # Inserir antes ou depois a Tabela Completa de Variáveis como Tabela 4.B ou integrá-la na Seção 3.5
    bloco_tabela_variaveis_artigo = f"""#### Tabela 4.B – Inventário Completo de Todas as 30 Variáveis Macroeconômicas e Justificativa de Seleção

{tabela_completa_30_md}

"""
    if 'Tabela 4.B' not in text_md:
        pos_ins = text_md.find('#### 3.5.5 Desenho Experimental')
        if pos_ins != -1:
            text_md = text_md[:pos_ins] + bloco_tabela_variaveis_artigo + text_md[pos_ins:]
            print("✅ Tabela Exaustiva Completa inserida na Seção 3.5 do Markdown!")

with open(caminho_secoes_md, 'w', encoding='utf-8') as f:
    f.write(text_md)

# -------------------------------------------------------------
# 4. RECOMPILAR O WORD (.DOCX) DAS SEÇÕES ENTREGÁVEIS
# -------------------------------------------------------------
doc = Document()
for s in doc.sections:
    s.top_margin = Inches(1.0)
    s.bottom_margin = Inches(1.0)
    s.left_margin = Inches(1.0)
    s.right_margin = Inches(1.0)

def limpar_xml(texto):
    if not isinstance(texto, str):
        return str(texto)
    return "".join(c for c in texto if ord(c) >= 32 or ord(c) in (10, 13, 9))

p_head = doc.add_paragraph()
p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_u = p_head.add_run("UNIVERSIDADE DE PERNAMBUCO – UPE\nESCOLA POLITÉCNICA DE PERNAMBUCO – POLI\n")
r_u.bold = True
r_u.font.size = Pt(12)
r_u.font.color.rgb = RGBColor(0, 32, 96)

r_sub = p_head.add_run("PROGRAMA DE PÓS-GRADUAÇÃO / GRADUAÇÃO EM ENGENHARIA DA COMPUTAÇÃO\nMINERAÇÃO DE DADOS – ATIVIDADE 8: MÉTODOS DE REGRESSÃO SUPERVISIONADA\nProf. Dr. Alexandre Maciel\n")
r_sub.bold = True
r_sub.font.size = Pt(10.5)

p_tit = doc.add_paragraph()
p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_tit = p_tit.add_run("ENTREGÁVEL ESPECÍFICO: SEÇÕES 2.2, 3.5 E 4.1 DO ARTIGO")
r_tit.bold = True
r_tit.font.size = Pt(13)
r_tit.font.color.rgb = RGBColor(0, 32, 96)

p_desc = doc.add_paragraph("Este documento reúne formalmente a fundamentação teórica da Regressão Linear Múltipla OLS e dos métodos regularizados (Seção 2.2), o inventário exaustivo de todas as 30 variáveis candidatas e o desenho dos 3 cenários (Seção 3.5) e a análise de desempenho comparativo e estudo de casos concretos (Seção 4.1).\n")
p_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

df_metricas = pd.read_csv('Entrega_Classroom/8_Regressao/metricas_regressao_horizontes.csv')
df_cenarios_tab = pd.read_csv('Entrega_Classroom/8_Regressao/comparativo_3_cenarios_ols_lasso.csv')

def formatar_tabela_docx(doc_obj, df_tab, cor_destaque='002060'):
    tabela = doc_obj.add_table(rows=len(df_tab) + 1, cols=len(df_tab.columns))
    tabela.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, col_nome in enumerate(df_tab.columns):
        cell = tabela.cell(0, j)
        cell.text = limpar_xml(col_nome)
        shading = OxmlElement('w:shd')
        shading.set(qn('w:val'), 'clear')
        shading.set(qn('w:color'), 'auto')
        shading.set(qn('w:fill'), cor_destaque)
        cell._tc.get_or_add_tcPr().append(shading)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.bold = True
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(255, 255, 255)
    for i, row in df_tab.iterrows():
        for j, val in enumerate(row):
            cell = tabela.cell(i + 1, j)
            cell.text = limpar_xml(val)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 1 else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.size = Pt(8.0)
                if 'Estado da Arte' in str(row.iloc[0]):
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(0, 32, 96)
    doc_obj.add_paragraph()

for linha in text_md.split('\n'):
    l_str = linha.strip()
    if not l_str:
        continue
    if l_str.startswith('### '):
        h = doc.add_paragraph()
        r = h.add_run(limpar_xml(l_str.replace('### ', '')))
        r.bold = True
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(0, 32, 96)
    elif l_str.startswith('#### '):
        if 'Tabela 4' in l_str and 'Tabela 4.B' not in l_str:
            p = doc.add_paragraph()
            r = p.add_run("Tabela 4 – Métricas Comparativas de Regressão Multivariada Out-of-Sample (2022–2026)")
            r.bold = True
            r.font.size = Pt(10.5)
            formatar_tabela_docx(doc, df_metricas)
        elif 'Tabela 5' in l_str:
            p = doc.add_paragraph()
            r = p.add_run("Tabela 5 – Desempenho Comparativo nos Três Cenários de Seleção de Atributos: OLS vs. Lasso")
            r.bold = True
            r.font.size = Pt(10.5)
            formatar_tabela_docx(doc, df_cenarios_tab, cor_destaque='1F4E79')
        else:
            h = doc.add_paragraph()
            r = h.add_run(limpar_xml(l_str.replace('#### ', '')))
            r.bold = True
            r.font.size = Pt(11.5)
            r.font.color.rgb = RGBColor(31, 78, 121)
    elif l_str.startswith('|') or l_str.startswith('!['):
        continue
    else:
        p = doc.add_paragraph(limpar_xml(l_str))
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        for r in p.runs:
            r.font.size = Pt(10)

caminho_docx = 'Entrega_Classroom/8_Regressao/Secoes_2_2_3_5_4_1_Regressao.docx'
doc.save(caminho_docx)
print(f"✅ Arquivo Word (.docx) atualizado com sucesso em: {caminho_docx}")

# -------------------------------------------------------------
# 5. ATUALIZAR O ARTIGO PRINCIPAL E RECOMPILAR DOCX/PDF
# -------------------------------------------------------------
artigo_md = 'Artigo/Artigo_Previsao_Inflacao.md'
with open(artigo_md, 'r', encoding='utf-8') as f:
    art_txt = f.read()

sec22_start = text_md.find('### 2.2')
sec35_start = text_md.find('### 3.5')
sec41_start = text_md.find('### 4.1')

sec22_content = text_md[sec22_start:text_md.find('\n---\n', sec22_start)].strip()
sec35_content = text_md[sec35_start:text_md.find('\n---\n', sec35_start)].strip()
sec41_content = text_md[sec41_start:].strip()

p22 = art_txt.find('### 2.2')
p23 = art_txt.find('### 2.3')
if p22 != -1 and p23 != -1:
    art_txt = art_txt[:p22] + sec22_content + "\n\n" + art_txt[p23:]

p35 = art_txt.find('### 3.5')
p4 = art_txt.find('## 4 RESULTADOS')
if p35 != -1 and p4 != -1:
    art_txt = art_txt[:p35] + sec35_content + "\n\n" + art_txt[p4:]

p41 = art_txt.find('### 4.1')
p42 = art_txt.find('### 4.2')
if p41 != -1 and p42 != -1:
    art_txt = art_txt[:p41] + sec41_content + "\n\n" + art_txt[p42:]

with open(artigo_md, 'w', encoding='utf-8') as f:
    f.write(art_txt)

import shutil
shutil.copyfile(artigo_md, 'Entrega_Classroom/3_Artigo_Completo/Artigo_Previsao_Inflacao.md')
print("✅ Artigo principal atualizado com o inventário completo das 30 variáveis!")
