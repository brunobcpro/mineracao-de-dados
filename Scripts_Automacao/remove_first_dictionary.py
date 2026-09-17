import docx
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

def adjust_document(filepath):
    print(f"--- Adjusting {filepath} ---")
    doc = Document(filepath)
    
    # 1. Locate preliminary table, its caption, and its fonte
    p_cap_prelim = None
    p_fonte_prelim = None
    tbl_prelim = None
    
    for p in doc.paragraphs:
        if "Tabela 1 – Dicionário de Dados e Inventário" in p.text:
            p_cap_prelim = p
        elif "Fonte: Autores, com base em dados compilados do SGS/Banco Central do Brasil (2026)." in p.text:
            p_fonte_prelim = p
            
    if len(doc.tables) >= 2:
        tbl_prelim = doc.tables[0]._tbl
        
    # 2. Update Section 3.2 heading
    for p in doc.paragraphs:
        if p.text.strip().startswith("3.2 Dicionário e Inventário"):
            print(f"Found heading 3.2: {p.text}")
            p.text = ""
            r = p.add_run("3.2 Base de Dados e Contextualização Macroeconômica")
            r.font.name = "Arial"
            r.font.size = Pt(12)
            r.bold = True
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(5)
            p.paragraph_format.line_spacing = 1.15
            break
            
    # 3. Update paragraph introducing the dimensions in Section 3.2
    for p in doc.paragraphs:
        if "O conjunto de dados é formado por 1 variável alvo (IPCA) e 28 variáveis externas" in p.text or \
           "O conjunto de dados é formado por 1 variável alvo (IPCA) e 28 variáveis" in p.text:
            print(f"Found dimension intro: {p.text[:60]}...")
            p.text = ""
            r = p.add_run(
                "O conjunto de dados é formado por 1 variável alvo (IPCA) e 28 variáveis exógenas (preditoras), "
                "estruturadas em quatro dimensões macroeconômicas da economia brasileira: "
                "(i) Índices de Preços e Componentes Setoriais (11 variáveis); "
                "(ii) Setor Financeiro e Câmbio (3 variáveis); "
                "(iii) Atividade Econômica e Emprego (7 variáveis); e "
                "(iv) Energia e Combustíveis (6 variáveis). "
                "As características técnicas completas, transformações matemáticas de estacionarização e a seleção "
                "definitiva de cada variável estão consolidadas no Dicionário de Dados Final (Tabela 1), apresentado "
                "na Seção 3.4.4 após a descrição das etapas de pré-processamento."
            )
            r.font.name = "Arial"
            r.font.size = Pt(11.5)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            break

    # 4. Remove preliminary table, caption, and fonte from Section 3.2
    if p_cap_prelim is not None:
        p_cap_prelim._element.getparent().remove(p_cap_prelim._element)
        print("Removed preliminary table caption.")
    if tbl_prelim is not None:
        tbl_prelim.getparent().remove(tbl_prelim)
        print("Removed preliminary table element.")
    if p_fonte_prelim is not None:
        p_fonte_prelim._element.getparent().remove(p_fonte_prelim._element)
        print("Removed preliminary table fonte.")

    # 5. Update Section 3.4.4 text and Table caption from Tabela 2 to Tabela 1
    for p in doc.paragraphs:
        if "estruturou-se o Dicionário de Dados Final apresentado na Tabela 2" in p.text:
            print("Found Section 3.4.4 table intro.")
            p.text = p.text.replace("Tabela 2", "Tabela 1")
            # re-apply formatting
            for r in p.runs:
                r.font.name = "Arial"
                r.font.size = Pt(11.5)
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            
        elif p.text.strip().startswith("Tabela 2 – Dicionário de Dados Final"):
            print("Found Table 2 caption.")
            p.text = ""
            r = p.add_run("Tabela 1 – Dicionário de Dados Final e Especificação das Variáveis Pré-Processadas")
            r.font.name = "Arial"
            r.font.size = Pt(10.5)
            r.bold = True
            p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15

    doc.save(filepath)
    print(f"Successfully saved {filepath} with single dictionary (Tabela 1)!")

if __name__ == "__main__":
    for f in ["Artigo_Previsao_Inflacao_Final.docx", "Artigo_Previsao_Inflacao_v5.docx", "Artigo_Previsao_Inflacao_v3.docx"]:
        adjust_document(f)
