# 📈 Mineração de Dados e Otimização para Previsão da Inflação (IPCA & CPI)

> **Projeto de Pesquisa / Trabalho de Conclusão e Iniciação Científica**  
> Modelagem Preditiva Híbrida (Linear + Não Linear), Meta-heurísticas Bioinspiradas (GA e PSO) e Processamento de Linguagem Natural (NLP) aplicados a Séries Macroeconômicas do Brasil e dos Estados Unidos.

---

## 🗺️ Estrutura e Organização do Repositório

O projeto está organizado em módulos funcionais e padronizados para facilitar a navegação no **Finder**, no **VS Code** e no terminal:

```
mineracao-de-dados/
│
├── 📄 README.md                            # Guia mestre do repositório (este arquivo)
├── 📄 RELATORIO_CONSOLIDADO_PROJETO.md      # Relatório técnico completo de arquitetura e resultados
│
├── 📂 Artigo/                               # 📑 Artigo Científico Oficial e Manuscrito em Word
│   ├── Artigo_Previsao_Inflacao.docx          # Versão oficial principal (sem redundâncias e com seções 3.2, 3.3 e 3.4)
│   ├── Artigo_Previsao_Inflacao.md            # Versão em Markdown para leitura rápida no VS Code
│   └── Historico_Versoes/                     # Arquivo histórico de versões preliminares (v1 a v5)
│
├── 📂 Entrega_Classroom/                    # 🎓 Pacote Oficial de Entrega da Atividade Acadêmica
│   ├── LEIA-ME_INSTRUCOES_ENTREGA.md       # Guia passo a passo de submissão no Google Classroom
│   ├── 1_Codigo_Python/                    # Script reproduzível (analise_exploratoria_entrega.py)
│   ├── 2_Secao_3_3_Artigo/                 # Documento individual da Seção 3.3 (DOCX e MD)
│   ├── 3_Artigo_Completo/                  # Artigo completo integrado com a Seção 3.3
│   ├── 4_Graficos_Alta_Resolucao/          # Figuras a 300 DPI (Histograma, Boxplot, Dispersão, Regimes)
│   └── 5_Tabelas_e_Dados/                  # Base de dados até agosto/2026 e tabelas de frequência CSV
│
├── 📂 Dados/                                # 📊 Ingestão e Bases Macroeconômicas
│   ├── README.md                           # Guia metodológico e governança das fontes oficiais
│   ├── df_macro.csv                        # Base consolidada do Brasil (Março/2012 a Agosto/2026)
│   ├── Brasil/                             # Coleta SGS/BACEN (extracao_macro_sgs.py e df_macro.csv)
│   └── USA/                                # Coleta FRED/Federal Reserve (dados_macroeconomicos_usa.csv)
│
├── 📂 Extracao_topicos/                     # 📰 Mineração de Texto e NLP em Atas do COPOM
│   ├── extracao_pdf.ipynb                  # Pipeline BERTopic, SentenceTransformers e SQLite
│   └── Relatorio-COPOM/                    # 69 Atas oficiais do COPOM em PDF (2016 a 2025)
│
├── 📂 Feature selection/                    # 🧬 Seleção de Atributos por Meta-heurísticas
│   ├── Brasil/                             # GA (Algoritmo Genético) e PSO para a base brasileira
│   └── USA/                                # GA e PSO para a base norte-americana
│
├── 📂 Modelos de treinamento/               # 🤖 Modelagem Preditiva e Hibridização
│   ├── ARIMA + ARIMA hibrido_/             # Modelos univariados clássicos e resíduos com Random Forest
│   ├── ARIMAX + ARIMAX hibrido_/           # Modelos multivariados ARIMAX + RF e ARIMAX + RNA
│   ├── Lasso.ipynb / Random Forest.ipynb   # Modelos puros de Machine Learning
│   └── USA/                                # Modelos equivalentes aplicados ao CPI norte-americano
│
└── 📂 Scripts_Automacao/                   # ⚙️ Utilitários de Formatação e Pipeline do Artigo
    ├── gerar_analise_e_secao3_3.py         # Pipeline de análise exploratória e injeção no Word
    ├── update_section3_4_complete.py       # Script de formatação da Seção 3.4
    ├── update_article_section3_2.py        # Script de formatação da Seção 3.2
    └── remove_first_dictionary.py          # Script utilitário de higienização de tabelas
```

---

## ⚡ Comandos Rápidos

### 1. Extrair os dados atualizados do Banco Central (SGS/BACEN)
```bash
python3 Dados/Brasil/extracao_macro_sgs.py
```

### 2. Rodar a Análise Exploratória e Gerar Gráficos e Seção 3.3
```bash
python3 Scripts_Automacao/gerar_analise_e_secao3_3.py
```

### 3. Executar o Script de Entrega da Atividade
```bash
cd Entrega_Classroom/1_Codigo_Python
python3 analise_exploratoria_entrega.py
```

---

## 📌 Principais Metodologias Empregadas

1. **Engenharia de Séries Temporais:** Transformação de séries em nível para primeira diferença estacionária via teste Dickey-Fuller Aumentado (`ADF`), interpolação temporal de dados contínuos sem vazamento prospectivo (*lookahead bias*).
2. **Meta-heurísticas de Seleção de Variáveis:** Algoritmos Genéticos (**GA**) e Otimização por Enxame de Partículas (**PSO**) discretos que reduzem de ~30 variáveis macroeconômicas para os 5 atributos de maior relevância preditiva.
3. **Arquiteturas Híbridas (Linear + Não Linear):**
   $$\hat{y}_t = \hat{L}_t (\text{ARIMAX}) + \hat{N}_t (\text{Random Forest / RNA})$$
   Redução de mais de 70% no erro quadrático médio (RMSE) comparado a modelos isolados.
