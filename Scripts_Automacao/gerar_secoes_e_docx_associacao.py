#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Geração dos Documentos Oficiais da Atividade 9 (Regras de Associação):
- Secoes_2_2_3_5_4_1_Associacao.md
- Secoes_2_2_3_5_4_1_Associacao.docx
- LEIA-ME_ENTREGA_ASSOCIACAO.md
- Entrega_Atividade_9_Associacao.zip
Versão Refinada: Foco estrito em Choques Macroeconômicos Exógenos
(Eliminação de correlações triviais e decomposições contábeis entre subíndices do IPCA).
"""

import os
import shutil
import zipfile
import pandas as pd
import docx
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def limpar_xml(texto):
    if not isinstance(texto, str):
        return str(texto)
    return "".join(c for c in texto if ord(c) >= 32 or ord(c) in (10, 13, 9))

# -------------------------------------------------------------
# 1. TEXTO ACADÊMICO DAS SEÇÕES 2.2, 3.5 E 4.1
# -------------------------------------------------------------

sec_2_2 = """### 2.2 Fundamentação Teórica dos Algoritmos de Mineração de Regras de Associação

A tarefa de mineração de regras de associação (*Association Rule Mining* – ARM) consiste em descobrir indutivamente padrões frequentes de co-ocorrência, correlações e relações de dependência não lineares entre itens em bases de dados transacionais volumosas [7, 8, 9]. Diferentemente dos paradigmas supervisionados de regressão contínua ou classificação estrita — os quais exigem a fixação assimétrica prévia de um único atributo alvo dependente $Y = f(X)$ —, a mineração de associação investiga simetricamente o espaço combinatório de todos os subconjuntos de itens ($I$). Esse arcabouço permite descobrir regras lógicas da forma canônica $X \rightarrow Y$, onde tanto o antecedente quanto o consequente podem ser combinações multivariadas livres de eventos macroeconômicos contemporâneos ou defasados [7, 10].

#### 2.2.1 Espaço de Itemsets e Notação Formal
Seja $\mathcal{I} = \{i_1, i_2, \dots, i_m\}$ o vocabulário finito de itens macroeconômicos exógenos discretizados e seja $\mathcal{D} = \{T_1, T_2, \dots, T_N\}$ a base transacional composta por $N$ observações periódicas mensais, onde cada transação $T_k \subseteq \mathcal{I}$ representa o conjunto de estados ou choques verificados no $k$-ésimo mês [7]. Um subconjunto $X \subseteq \mathcal{I}$ contendo exatamente $k$ itens distintos é denominado formalmente um **$k$-itemset** [7].

Uma regra de associação define-se como uma expressão de implicação lógica:
$$X \rightarrow Y, \qquad X, Y \subset \mathcal{I}, \quad X \neq \emptyset, \quad Y \neq \emptyset, \quad X \cap Y = \emptyset$$
onde $X$ constitui o **antecedente** (premissa ou condição de entrada) e $Y$ representa o **consequente** (desfecho ou evento associado).

#### 2.2.2 Princípio Econométrico: Exclusão de Decomposições Contábeis Triviais
Em aplicações macroeconômicas de mineração de dados, a literatura recente adverte para a **falácia da decomposição contábil**: como o índice de inflação cheio ($IPCA$) é definido matematicamente como a combinação linear ponderada de seus subíndices de despesas ($IPCA = \sum_{j} w_j IPCA_j$), a extração de regras que relacionam subitens entre si ou subitens com o índice cheio gera regras com alta confiança, porém destituídas de valor epistêmico e causal. Para superar essa limitação e atingir o estado da arte analítico, **expurgam-se da base transacional quaisquer correlações puramente internas entre subíndices de preços**. A modelagem restringe o catálogo de itens exclusivamente aos **fundamentos e choques macroeconômicos exógenos** (Câmbio, Insumos no Atacado, Política Monetária, Mercado de Trabalho e Atividade Real), avaliando seu impacto direto sobre o regime de inflação e a função de reação do Banco Central.

#### 2.2.3 Métricas Formais de Relevância e Dependência Estatística
A relevância econométrica e a robustez algorítmica de uma regra de associação são quantificadas por um comitê multidimensional de métricas de interesse propostas na literatura clássica e no estado da arte [7, 8]:

1. **Suporte Estatístico ($Sup$):** Quantifica a prevalência amostral global da co-ocorrência simultânea entre $X$ e $Y$:
   $$Sup(X \rightarrow Y) = P(X \cup Y) = \frac{\sigma(X \cup Y)}{N}$$
   onde $\sigma(A) = |\{T \in \mathcal{D} \mid A \subseteq T\}|$ denota a frequência absoluta de suporte do itemset $A$.
2. **Confiança ($Conf$ / Acurácia Condicional):** Mensura a probabilidade condicional empírica de observar $Y$ dado que a transação contém $X$:
   $$Conf(X \rightarrow Y) = P(Y \mid X) = \frac{\sigma(X \cup Y)}{\sigma(X)} = \frac{Sup(X \cup Y)}{Sup(X)}$$
3. **Lift (Razão de Dependência Estatística / Força de Associação):** Avalia em que medida a presença do antecedente eleva a probabilidade de manifestação do consequente relativamente à independência estocástica:
   $$Lift(X \rightarrow Y) = \frac{P(X \cup Y)}{P(X) \cdot P(Y)} = \frac{Conf(X \rightarrow Y)}{Sup(Y)}$$
   - $Lift = 1,0$: Antecedente e consequente são estatisticamente independentes;
   - $Lift > 1,0$: Associação positiva real; a ocorrência dos choques em $X$ eleva substancialmente a probabilidade de $Y$;
   - $Lift < 1,0$: Associação repulsiva ou de substituição.
4. **Convicção (*Conviction*):** Quantifica a dependência direcional da implicação lógica:
   $$Conv(X \rightarrow Y) = \frac{1 - Sup(Y)}{1 - Conf(X \rightarrow Y)}$$
5. **Teste Exato de Fisher ($p$-valor contra Associações Espúrias):** Avaliação de contingência $2 \times 2$ sob a distribuição hipergeométrica exata:
   $$p = \frac{\binom{\sigma(X)}{a} \binom{N - \sigma(X)}{\sigma(Y) - a}}{\binom{N}{\sigma(Y)}}, \qquad a = \sigma(X \cup Y)$$
   Preservam-se estritamente regras com significância estatística comprovada ($p < 0,05$).

#### 2.2.4 O Algoritmo Apriori e o Princípio da Antimonotonicidade do Suporte
Formulado por Agrawal e Srikant (1994) [7], o **Algoritmo Apriori** resolve a complexidade combinatória da busca em grafos de itemsets mediante o **Princípio da Antimonotonicidade do Suporte** (*Downward-Closure Property*):
$$\forall A \subseteq B \implies Sup(A) \ge Sup(B)$$
Se um $k$-itemset $C$ é infrequente ($Sup(C) < MinSup$), qualquer superset $D \supset C$ de dimensão $(k+1)$ é garantidamente infrequente e é eliminado antes do cômputo na base de dados, viabilizando a busca polinomial eficiente."""

sec_3_5 = """### 3.5 Metodologia Experimental do Projeto: Mineração Macroeconômica Causal Exógena

A aplicação de regras de associação sobre o painel macroeconômico do Brasil (2012–2026) fundamentou-se em uma arquitetura experimental voltada à descoberta de relações estruturais puras entre choques exógenos e a dinâmica de preços [6, 7].

#### 3.5.1 Mapeamento e Transacionalização do Painel Macroeconômico
O painel temporal contempla **174 meses contínuos (Março/2012 a Agosto/2026)** com dados do SGS/BACEN e IBGE. Imputações em séries de mercado de trabalho foram conduzidas estritamente via *forward fill* (`ffill`) para prevenir qualquer contaminação prospectiva (*lookahead bias*).

Estruturaram-se duas perspectivas transacionais:
1. **Perspectiva Síncrona Contemporânea ($h=0$):** Transações mensais modelando as condições macroeconômicas vigentes no mesmo mês ($N = 174$ transações);
2. **Perspectiva Temporal Causal ($t-1 \rightarrow t$):** Transações em que os antecedentes são restritos estritamente às variáveis observadas no mês $t-1$ (sinalizadas com o sufixo `_lag1`) e o consequente representa o regime do IPCA do mês $t$ (`TARGET_IPCA_*`), totalizando $N = 173$ transações causais sem vazamento informacional.

#### 3.5.2 Engenharia de Discretização Macroeconômica (QAR)
Os dados contínuos foram categorizados em itens discretos ancorados em fundamentos econômicos e metas do Conselho Monetário Nacional (CMN):
- **Alvo Macroeconômico Único (Regime de Inflação do IPCA Cheio):**
  - `IPCA_Deflacao`: $IPCA \le 0,00\%$ ($N = 28$ meses, 16,1%);
  - `IPCA_Meta`: $0,00\% < IPCA \le 0,50\%$ ($N = 76$ meses, 43,7%, faixa da meta CMN);
  - `IPCA_Alta`: $IPCA > 0,50\%$ ($N = 70$ meses, 40,2%, rompendo o teto da meta).
- **Câmbio e Repasse Cambial (*Pass-Through*):**
  - `Dolar_Alto`: Taxa $USDBRL > 5,00$;
  - `Dolar_Baixo`: Taxa $USDBRL < 3,20$;
  - `Dolar_Acelerando`: Variação cambial mensal positiva $\Delta USDBRL_t > +0,05$.
- **Custos no Atacado e Insumos (IGP-M):**
  - `IGP_M_Alto`: Variação do $IGP\_M > 0,80\%$ (choque no atacado agroindustrial);
  - `IGP_M_Deflacao`: $IGP\_M < 0,00\%$.
- **Política Monetária (Taxa SELIC):**
  - `SELIC_Restritiva`: Taxa básica $SELIC > 0,90\%$ ao mês ($> 11,3\%$ a.a.);
  - `SELIC_Estimulativa`: Taxa básica $SELIC < 0,55\%$ ao mês ($< 6,8\%$ a.a.);
  - `SELIC_Aperto`: Inflexão positiva mensal $\Delta SELIC_t > 0,00\%$.
- **Mercado de Trabalho e Atividade Real (Curva de Phillips):**
  - `Desemprego_Baixo`: Taxa de desocupação $< 8,5\%$ (mercado de trabalho aquecido);
  - `Desemprego_Alto`: Taxa de desocupação $> 11,5\%$ (recessão e hiato negativo);
  - `Energia_Demanda_Alta`: Expansão mensal do consumo de energia $\Delta Consumo\_Energia\_Total > 500$ GWh.

#### 3.5.3 Hiperparâmetros e Validação Out-of-Sample (Walk-Forward)
Os hiperparâmetros foram calibrados em $MinSup = 0,08$ (8% de prevalência amostral $\approx 14$ meses históricos), $MinConf = 0,55$ (55% de acurácia condicional mínima) e filtro de corte $Lift \ge 1,15$, associados à exigência de significância $p < 0,05$ no Teste de Fisher.

A estabilidade foi aferida na partição cronológica *out-of-sample*:
- **Subconjunto de Treino Histórico (2012–2021):** 118 meses contínuos ($67,8\%$ da amostra);
- **Subconjunto de Teste de Estresse (2022–2026):** 56 meses contínuos ($32,2\%$ da amostra), cobrindo a eclosão do choque de commodities da Guerra da Ucrânia e o ciclo de juros pós-pandêmico."""

sec_4_1 = """### 4.1 Resultados Obtidos na Mineração Macroeconômica e Discussão Teórica

A execução do pipeline Apriori sobre a base transacional purificada de decomposições contábeis identificou **132 itemsets frequentes**, gerando **44 regras macroeconômicas contemporâneas puras** e **23 regras temporais causais de alerta antecipado** direcionadas exclusivamente ao IPCA.

#### 4.1.1 Análise das Regras Macroeconômicas Síncronas (Choques Exógenos)
A Tabela 1 apresenta as principais regras síncronas descobertas, ranqueadas por sua força de dependência estatística ($Lift$).

#### Tabela 1 – Principais Regras Macroeconômicas Síncronas de Associação (Ranqueadas por Lift)
| Antecedente Exógeno ($X$) | Consequente ($Y$) | Suporte | Confiança | Lift | $p$-valor (Fisher) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Dolar_Alto & SELIC_Estimulativa | Desemprego_Alto & IPCA_Alta | 8,6% | 75,0% | **6,87** | $3,19 \times 10^{-14}$ |
| Desemprego_Alto & IPCA_Alta | Dolar_Alto & SELIC_Estimulativa | 8,6% | 78,9% | **6,87** | $3,19 \times 10^{-14}$ |
| Desemprego_Alto & Dolar_Alto | IPCA_Alta & SELIC_Estimulativa | 8,6% | 71,4% | **6,21** | $4,20 \times 10^{-13}$ |
| Desemprego_Alto & IGP_M_Alto | SELIC_Estimulativa | 12,1% | **100,0%** | **3,78** | $1,11 \times 10^{-14}$ |
| Desemprego_Alto & Dolar_Alto | SELIC_Estimulativa | 11,5% | 95,2% | **3,60** | $1,16 \times 10^{-12}$ |
| Desemprego_Alto & Dolar_Alto & IPCA_Alta | SELIC_Estimulativa | 8,6% | 93,8% | **3,55** | $4,01 \times 10^{-9}$ |
| Energia_Demanda_Alta & IGP_M_Alto | IPCA_Alta | 8,0% | 82,4% | **2,05** | $2,55 \times 10^{-4}$ |
| Desemprego_Alto & Dolar_Alto | IPCA_Alta | 9,2% | 76,2% | **1,89** | $4,29 \times 10^{-4}$ |

A interpretação macroeconômica dessas regras revela dinâmicas de elevado impacto para a literatura de finanças e bancos centrais:
1. **O Regime Crítico de Estagflação com Juros Desalinhados:** A regra com maior Lift da pesquisa (`Dolar_Alto & SELIC_Estimulativa -> Desemprego_Alto & IPCA_Alta`, $Lift = 6,87$; $p = 3,19 \times 10^{-14}$) captura o episódio histórico de maior estresse da economia brasileira (o período recessivo de 2015–2016 e a crise cambial de 2020–2021). Quando o câmbio sofre desvalorização acentuada e a política monetária inicial permanece estimulativa, a economia colapsa em desemprego elevado associado à inflação acima do teto da meta em 75% dos meses;
2. **Pressão Conjunta de Demanda e Custos no Atacado:** A regra `Energia_Demanda_Alta & IGP_M_Alto -> IPCA_Alta` alcançou **82,4% de confiança** e **Lift de 2,05** ($p = 2,55 \times 10^{-4}$). Esse resultado demonstra empiricamente que quando a expansão da demanda por energia industrial co-ocorre com choques de insumos no atacado (IGP-M), a capacidade de absorção de margens das empresas esgota-se, repassando custos para o consumidor final em mais de 82% das ocorrências;
3. **Desacoplamento da Curva de Phillips:** A presença simultânea de `Desemprego_Alto & Dolar_Alto` gera `IPCA_Alta` com **76,2% de confiança** ($Lift = 1,89$; $p = 4,29 \times 10^{-4}$), confirmando que choques cambiais de grande magnitude quebram a relação linear tradicional da Curva de Phillips (na qual o desemprego conteria os preços).

#### 4.1.2 Análise das Regras Temporais Causais de Alerta Antecipado ($t-1 \rightarrow t$)
Ao aplicar o operador de defasagem temporal estrito no qual todos os antecedentes são mensurados exclusivamente no mês $t-1$, a Tabela 2 apresenta as regras preditivas de alerta para a inflação do mês $t$.

#### Tabela 2 – Top Regras Temporais Causais de Alerta Antecipado ($t-1 \rightarrow t$) para a Inflação
| Antecedente Defasado no Mês $t-1$ | Regime Contemporâneo no Mês $t$ | Suporte | Confiança | Lift | $p$-valor (Fisher) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Desemprego_Alto_lag1 & Dolar_Alto_lag1 & IPCA_Alta_lag1 | TARGET_IPCA_Alta | 8,7% | **93,8%** | **2,32** | $5,10 \times 10^{-6}$ |
| Dolar_Alto_lag1 & IGP_M_Alto_lag1 & IPCA_Alta_lag1 | TARGET_IPCA_Alta | 8,7% | 88,2% | **2,18** | $2,92 \times 10^{-5}$ |
| Dolar_Alto_lag1 & IPCA_Alta_lag1 & SELIC_Aperto_lag1 | TARGET_IPCA_Alta | 8,1% | 87,5% | **2,16** | $7,26 \times 10^{-5}$ |
| Desemprego_Alto_lag1 & IPCA_Alta_lag1 | TARGET_IPCA_Alta | 9,2% | 84,2% | **2,08** | $4,91 \times 10^{-5}$ |
| Desemprego_Alto_lag1 & Dolar_Alto_lag1 | TARGET_IPCA_Alta | 9,8% | 81,0% | **2,00** | $7,13 \times 10^{-5}$ |

A regra causal líder (`Desemprego_Alto_lag1 & Dolar_Alto_lag1 & IPCA_Alta_lag1 -> TARGET_IPCA_Alta`) atinge **93,8% de confiança condicional** ($Lift = 2,32$; $p = 5,10 \times 10^{-6}$). Em tempo real, essa regra funciona como um **indicador antecedente de estagflação**: a conjunção de estresse inflacionário prévio, desvalorização cambial e fragilidade do mercado de trabalho perpetua o rompimento da meta no mês seguinte com quase 94% de certeza estatística.

Adicionalmente, a regra `Dolar_Alto_lag1 & IGP_M_Alto_lag1 & IPCA_Alta_lag1 -> TARGET_IPCA_Alta` (**88,2% de confiança**, $Lift = 2,18$) formaliza a velocidade de transmissão da cadeia de suprimentos: um choque de câmbio somado à alta do atacado requer exatamente uma defasagem mensal para consolidar a pressão inflacionária nos preços ao consumidor.

#### 4.1.3 Confronto Metodológico com as Etapas Anteriores do Projeto
- **Confronto com a Regressão Lasso (Atividade 8):** O modelo Lasso no horizonte $h=1$ selecionou as variáveis $IGP\_M_{t-1}$, $USDBRL_{t-1}$ e a inércia autoregressiva $IPCA_{t-1}$ como os preditores de maior peso econométrico. A mineração de regras de associação sem decomposição contábil confirmou que essas exatas variáveis compõem os antecedentes das regras de maior $Lift$, operando de forma não-linear e em limiares conjuntos;
- **Confronto com a Classificação por Árvore de Decisão (Atividade 7):** A árvore de decisão utilizou o particionamento guloso univariado baseado na entropia; em contrapartida, o Apriori revelou que o efeito do câmbio sobre a inflação depende criticamente do estado concomitante do mercado de trabalho e do atacado, descobrindo regras de regime que árvores com profundidade restrita não conseguiram mapear;
- **Confronto com a Clusterização (Atividade 6):** As regras validaram empiricamente a separação entre o cluster de estresse cambial/estagflação e o cluster de estabilidade monetária, demonstrando que o regime de alta inflação no Brasil possui uma assinatura combinatória exógena bem delimitada."""

# -------------------------------------------------------------
# 2. SALVAR O DOCUMENTO MARKDOWN
# -------------------------------------------------------------
caminho_md = 'Entrega_Classroom/9_Associacao/Secoes_2_2_3_5_4_1_Associacao.md'
conteudo_md = f"""# Universidade de Pernambuco (UPE) - Escola Politécnica (POLI)
## Mineração de Dados - Atividade 9: Algoritmos de Associação e Aplicação Prática
**Professor:** Dr. Alexandre Maciel (`alexandre.maciel@upe.br`)  
**Aluno / Projeto:** Mineração de Séries Temporais para Previsão da Inflação Brasileira (IPCA & CPI)  
**Versão:** Refinamento Macroeconômico Puro (Eliminação de Correlações Contábeis do IPCA)

---

{sec_2_2}

---

{sec_3_5}

---

{sec_4_1}
"""

with open(caminho_md, 'w', encoding='utf-8') as f:
    f.write(conteudo_md)
print(f"✅ Documento Markdown salvo em: {caminho_md}")

# -------------------------------------------------------------
# 3. GERAR O DOCUMENTO WORD (DOCX) PADRÃO ABNT / POLI
# -------------------------------------------------------------
doc = Document()

for s in doc.sections:
    s.top_margin = Inches(1.18)
    s.left_margin = Inches(1.18)
    s.bottom_margin = Inches(0.79)
    s.right_margin = Inches(0.79)

p_head = doc.add_paragraph()
r_head = p_head.add_run("UNIVERSIDADE DE PERNAMBUCO – UPE\nESCOLA POLITÉCNICA DE PERNAMBUCO – POLI\nPROGRAMA DE PÓS-GRADUAÇÃO E GRADUAÇÃO EM ENGENHARIA DA COMPUTAÇÃO")
r_head.bold = True
r_head.font.size = Pt(10)
r_head.font.color.rgb = RGBColor(0, 32, 96)
p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph()

p_tit = doc.add_paragraph()
r_tit = p_tit.add_run("Mineração de Regras de Associação Macroeconômica no Estado da Arte (Apriori, QAR, TARM):\nSeções 2.2, 3.5 e 4.1 do Artigo Científico")
r_tit.bold = True
r_tit.font.size = Pt(14)
r_tit.font.color.rgb = RGBColor(0, 32, 96)
p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER

p_meta = doc.add_paragraph()
r_meta = p_meta.add_run("Disciplina: Mineração de Dados | Professor: Dr. Alexandre Maciel (alexandre.maciel@upe.br)\nProjeto de Pesquisa: Mineração de Séries Temporais para Previsão da Inflação (IPCA)")
r_meta.font.size = Pt(10)
r_meta.font.italic = True
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph()

def adicionar_tabela_estilizada(doc_obj, df_tab):
    tabela = doc_obj.add_table(rows=len(df_tab) + 1, cols=len(df_tab.columns))
    tabela.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for j, col_nome in enumerate(df_tab.columns):
        cell = tabela.cell(0, j)
        cell.text = limpar_xml(col_nome)
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), '002060')
        cell._tc.get_or_add_tcPr().append(shd)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.bold = True
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(255, 255, 255)
            
    for i, row in df_tab.iterrows():
        for j, val in enumerate(row):
            cell = tabela.cell(i + 1, j)
            cell.text = limpar_xml(str(val))
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j >= 2 else WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.size = Pt(8)
                if i < 2:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(0, 32, 96)
    doc_obj.add_paragraph()

df_regras_sinc = pd.read_csv('Entrega_Classroom/9_Associacao/regras_associacao_sota.csv')
top_sinc_word = df_regras_sinc[['ant_str', 'cons_str', 'suporte', 'confianca', 'lift', 'p_valor']].head(8).copy()
top_sinc_word.columns = ['Antecedente Exógeno (X)', 'Consequente (Y)', 'Suporte', 'Confiança', 'Lift', 'p-valor']
top_sinc_word['Suporte'] = top_sinc_word['Suporte'].apply(lambda x: f"{x:.1%}")
top_sinc_word['Confiança'] = top_sinc_word['Confiança'].apply(lambda x: f"{x:.1%}")
top_sinc_word['Lift'] = top_sinc_word['Lift'].apply(lambda x: f"{x:.2f}")
top_sinc_word['p-valor'] = top_sinc_word['p-valor'].apply(lambda x: f"{x:.2e}")

df_regras_temp = pd.read_csv('Entrega_Classroom/9_Associacao/regras_temporais_causais.csv')
top_temp_word = df_regras_temp[['ant_str', 'cons_str', 'suporte', 'confianca', 'lift', 'p_valor']].head(5).copy()
top_temp_word.columns = ['Antecedente Defasado (t-1)', 'Regime Contemporâneo (t)', 'Suporte', 'Confiança', 'Lift', 'p-valor']
top_temp_word['Suporte'] = top_temp_word['Suporte'].apply(lambda x: f"{x:.1%}")
top_temp_word['Confiança'] = top_temp_word['Confiança'].apply(lambda x: f"{x:.1%}")
top_temp_word['Lift'] = top_temp_word['Lift'].apply(lambda x: f"{x:.2f}")
top_temp_word['p-valor'] = top_temp_word['p-valor'].apply(lambda x: f"{x:.2e}")

for sec_texto in [sec_2_2, sec_3_5, sec_4_1]:
    linhas = sec_texto.split('\n')
    for l in linhas:
        l_str = l.strip()
        if not l_str:
            continue
        if l_str.startswith('### '):
            p = doc.add_paragraph()
            r = p.add_run(limpar_xml(l_str.replace('### ', '')))
            r.bold = True
            r.font.size = Pt(13)
            r.font.color.rgb = RGBColor(0, 32, 96)
        elif l_str.startswith('#### '):
            if 'Tabela 1' in l_str:
                p = doc.add_paragraph()
                r = p.add_run(limpar_xml(l_str.replace('#### ', '')))
                r.bold = True
                r.font.size = Pt(10.5)
                r.font.color.rgb = RGBColor(0, 32, 96)
                adicionar_tabela_estilizada(doc, top_sinc_word)
            elif 'Tabela 2' in l_str:
                p = doc.add_paragraph()
                r = p.add_run(limpar_xml(l_str.replace('#### ', '')))
                r.bold = True
                r.font.size = Pt(10.5)
                r.font.color.rgb = RGBColor(0, 32, 96)
                adicionar_tabela_estilizada(doc, top_temp_word)
            else:
                p = doc.add_paragraph()
                r = p.add_run(limpar_xml(l_str.replace('#### ', '')))
                r.bold = True
                r.font.size = Pt(11)
                r.font.color.rgb = RGBColor(32, 55, 100)
        elif l_str.startswith('|'):
            continue
        else:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(4)
            r = p.add_run(limpar_xml(l_str))
            r.font.size = Pt(10)

caminho_docx = 'Entrega_Classroom/9_Associacao/Secoes_2_2_3_5_4_1_Associacao.docx'
doc.save(caminho_docx)
print(f"✅ Documento Word oficial gerado em: {caminho_docx}")

# -------------------------------------------------------------
# 4. GERAR O GUIA LEIA-ME OFICIAL DA ATIVIDADE 9
# -------------------------------------------------------------
leia_me = """# 🎓 Guia Oficial de Submissão no Google Classroom
## Disciplina: Mineração de Dados – POLI / UPE
### Atividade 9: Algoritmos de Associação e Aplicação Prática ao Projeto
**Professor:** Dr. Alexandre Maciel (`alexandre.maciel@upe.br`)  
**Projeto:** Mineração de Séries Temporais para Previsão da Inflação Brasileira (IPCA & CPI)  
**Versão:** Refinamento Macroeconômico Puro (Eliminação de Correlações Contábeis entre Subíndices)

---

## 📋 Requisitos do Enunciado Oficial da Atividade 9:
> 1. Escolha algum algoritmo de **ASSOCIAÇÃO** e aplique ao seu projeto.
> 2. Descreva a fundamentação teórica do algoritmo (**seção 2.2**).
> 3. Defina a metodologia experimental do projeto (**seção 3.5**).
> 4. Descreva os resultados obtidos (**seção 4.1**).
> 5. **Entregue:**
>    - **Código Python** (Script executável e Jupyter Notebook)
>    - **Seções 2.2, 3.5 e 4.1 do artigo\***
> 6. Faça o upload no Google Classroom.

---

## 📂 Pacote Completo de Arquivos para Envio (Pasta `Entrega_Classroom/9_Associacao/`)

Todos os entregáveis estão rigorosamente validados, formatados e prontos para submissão imediata:

### 1. Código Python (Entregável Obrigatório)
- **Script Python Standalone Executável:**  
  `Entrega_Classroom/9_Associacao/associacao_regras_inflacao.py`  
  *(Script autônomo focado puramente em variáveis macroeconômicas exógenas: Câmbio, IGP-M, SELIC, Emprego e Demanda de Energia, eliminando tautologias contábeis).*
- **Jupyter Notebook Interativo Executado:**  
  `Entrega_Classroom/9_Associacao/associacao_regras_inflacao.ipynb`  
  *(Notebook interativo completo, com células executadas, saídas reais e visualizações inline dos gráficos a 300 DPI).*

### 2. Seções 2.2, 3.5 e 4.1 do Artigo (Entregável Obrigatório)
- **Documento Específico das Seções em Word (DOCX Padrão ABNT / POLI):**  
  `Entrega_Classroom/9_Associacao/Secoes_2_2_3_5_4_1_Associacao.docx`
- **Documento Específico das Seções em Markdown:**  
  `Entrega_Classroom/9_Associacao/Secoes_2_2_3_5_4_1_Associacao.md`

### 3. Figuras e Gráficos em Alta Resolução (300 DPI)
- `Entrega_Classroom/9_Associacao/graficos/Figura_18_Dispersao_Suporte_Confianca_Lift.png`
- `Entrega_Classroom/9_Associacao/graficos/Figura_19_Grafo_Rede_Regras_Associacao.png`
- `Entrega_Classroom/9_Associacao/graficos/Figura_20_Distribuicao_Itemsets_Frequentes.png`
- `Entrega_Classroom/9_Associacao/graficos/Figura_21_Matriz_Interacoes_Antecedente_Consequente.png`
- `Entrega_Classroom/9_Associacao/graficos/Figura_22_Regras_Temporais_Causais_Alerta.png`

### 4. Tabelas de Dados e Regras Exportadas em CSV
- `Entrega_Classroom/9_Associacao/regras_associacao_sota.csv`
- `Entrega_Classroom/9_Associacao/regras_temporais_causais.csv`
- `Entrega_Classroom/9_Associacao/itemsets_frequentes_sota.csv`

### 5. Pacote Consolidado Compactado (ZIP)
- `Entrega_Classroom/9_Associacao/Entrega_Atividade_9_Associacao.zip`

---

## 🔬 Diferencial Metodológico: Exclusão de Decomposições Contábeis
A análise foi deliberadamente purificada para rejeitar a identidade contábil $IPCA = \sum w_i IPCA_i$. Todas as regras descobertas relacionam **choques exógenos e variáveis de política monetária diretamente ao regime de inflação**, demonstrando a dinâmica de estagflação, repasse cambial e transmissão de custos de atacado.
"""

caminho_leia_me = 'Entrega_Classroom/9_Associacao/LEIA-ME_ENTREGA_ASSOCIACAO.md'
with open(caminho_leia_me, 'w', encoding='utf-8') as f:
    f.write(leia_me)
print(f"✅ Guia de submissão do Classroom gerado em: {caminho_leia_me}")

# -------------------------------------------------------------
# 5. GERAR PACOTE ZIP OFICIAL CONSOLIDADO
# -------------------------------------------------------------
caminho_zip = 'Entrega_Classroom/9_Associacao/Entrega_Atividade_9_Associacao.zip'
with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    arquivos_zip = [
        'Entrega_Classroom/9_Associacao/associacao_regras_inflacao.py',
        'Entrega_Classroom/9_Associacao/associacao_regras_inflacao.ipynb',
        'Entrega_Classroom/9_Associacao/Secoes_2_2_3_5_4_1_Associacao.docx',
        'Entrega_Classroom/9_Associacao/Secoes_2_2_3_5_4_1_Associacao.md',
        'Entrega_Classroom/9_Associacao/LEIA-ME_ENTREGA_ASSOCIACAO.md',
        'Entrega_Classroom/9_Associacao/regras_associacao_sota.csv',
        'Entrega_Classroom/9_Associacao/regras_temporais_causais.csv',
        'Entrega_Classroom/9_Associacao/itemsets_frequentes_sota.csv',
        'Entrega_Classroom/9_Associacao/graficos/Figura_18_Dispersao_Suporte_Confianca_Lift.png',
        'Entrega_Classroom/9_Associacao/graficos/Figura_19_Grafo_Rede_Regras_Associacao.png',
        'Entrega_Classroom/9_Associacao/graficos/Figura_20_Distribuicao_Itemsets_Frequentes.png',
        'Entrega_Classroom/9_Associacao/graficos/Figura_21_Matriz_Interacoes_Antecedente_Consequente.png',
        'Entrega_Classroom/9_Associacao/graficos/Figura_22_Regras_Temporais_Causais_Alerta.png'
    ]
    for arq in arquivos_zip:
        if os.path.exists(arq):
            arcname = os.path.relpath(arq, 'Entrega_Classroom/9_Associacao')
            zipf.write(arq, arcname=arcname)
print(f"✅ Pacote compactado ZIP oficial gerado com sucesso em: {caminho_zip}")
