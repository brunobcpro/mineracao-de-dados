# 🎓 Guia Oficial de Submissão no Google Classroom
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
