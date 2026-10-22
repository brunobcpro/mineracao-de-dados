# 🎓 Guia Oficial de Submissão no Google Classroom
## Disciplina: Mineração de Dados – POLI / UPE
### Atividade 8: Métodos de Regressão Supervisionada
**Professor:** Dr. Alexandre Maciel (`alexandre.maciel@upe.br`)

---

## 📋 Requisitos do Enunciado Oficial:
> **ATIVIDADE 8 (REGRESSÃO):**
> 1. Escolha algum algoritmo de **REGRESSÃO** e aplique ao seu projeto.
> 2. Descreva a fundamentação teórica do algoritmo (**seção 2.2**).
> 3. Defina a metodologia experimental do projeto (**seção 3.5**).
> 4. Descreva os resultados obtidos (**seção 4.1**).
> 5. **Entregue:**
>    - **Código Python** (Script executável e Jupyter Notebook)
>    - **Seções 2.2, 3.5 e 4.1 do artigo\***
> 6. Faça o upload no Google Classroom.

---

## 📂 Pacote Completo de Arquivos para Envio (Pasta `Entrega_Classroom/8_Regressao/`)

Todos os entregáveis estão rigorosamente validados, formatados e prontos para submissão imediata:

### 1. Código Python (Entregável Obrigatório)
- **Script Python Standalone Executável:**  
  `Entrega_Classroom/8_Regressao/regressao_previsao_inflacao.py`  
  *(Script autônomo e modular que executa o pipeline preditivo causal, realiza a padronização Z-score, treina os 6 regressores nos horizontes h=1, h=3 e h=12, calcula todas as métricas econométricas e gera os gráficos).*
- **Jupyter Notebook Interativo Executado:**  
  `Entrega_Classroom/8_Regressao/regressao_previsao_inflacao.ipynb`  
  *(Notebook interativo completo, com blocos de código formatados, saídas numéricas, visualização inline e interpretações).*

### 2. Seções 2.2, 3.5 e 4.1 do Artigo (Entregável Obrigatório)
- **Documento Específico das Seções em Word (DOCX Padrão ABNT / POLI):**  
  `Entrega_Classroom/8_Regressao/Secoes_2_2_3_5_4_1_Regressao.docx`
- **Documento Específico das Seções em Markdown:**  
  `Entrega_Classroom/8_Regressao/Secoes_2_2_3_5_4_1_Regressao.md`
- **Artigo Completo Integrado (Word DOCX - Template Oficial REPA):**  
  `Entrega_Classroom/3_Artigo_Completo/Artigo_Previsao_Inflacao.docx`
- **Artigo Completo Integrado (PDF Oficial):**  
  `Entrega_Classroom/3_Artigo_Completo/Artigo_Previsao_Inflacao.pdf`

### 3. Figuras e Gráficos em Alta Resolução (300 DPI)
- `Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_14_Comparativo_Regressores_Horizontes.png`
- `Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_15_Serie_Temporal_Real_vs_Predito_Regressao.png`
- `Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_16_Coeficientes_Lasso_Sparsity_Horizontes.png`
- `Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_17_Dispersao_Residuos_Diagnostico.png`

---

## 🔬 Destaques Macroeconômicos e Metodológicos (Diferencial Científico)
1. **Horizontes de Previsão Relevantes para o Mercado:**  
   - $h=1$ mês: *Nowcasting* / liquidação mensal de derivativos DAP da B3 e títulos NTN-B.
   - $h=3$ meses: Planejamento tático trimestral e ciclo de reuniões do COPOM.
   - $h=12$ meses: Horizonte relevante de política monetária do Banco Central (Meta de Inflação do CMN).
2. **Prevenção Estrita de Vazamento de Dados (*Data Leakage*):**  
   - Adoção de **Projeção Direta (*Direct Multi-Step Forecasting*)**, imune à propagação de erros de especificação recursiva.
   - Divisão cronológica *out-of-sample*: Treino de 2012 a 2021 (118 meses); Teste cego de estresse de 2022 a 2026 (55 meses).
3. **Liderança dos Modelos Regularizados:**  
   - O **Lasso (L1)** atingiu o menor erro de previsão geral com **MAE de 0,2671 p.p.** e **RMSE de 0,3282 p.p.** ($R^2 = +0,4216$), superando a Persistência (MAE 0,3167) e a Média Histórica (MAE 0,3594).
4. **Validação da Teoria Econômica (Transição da Inércia para os Juros):**  
   - No curto prazo ($h=1$), o IPCA é impulsionado pela inércia própria (+0,164) e repasse de custos de atacado do IGP-DI (+0,141).
   - No horizonte de política monetária ($h=12$), a **taxa SELIC atua com coeficiente de -0,2135**, comprovando empiricamente o canal de transmissão monetária do BACEN.
