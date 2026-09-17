# Previsão da Inflação Brasileira (IPCA) por Mineração de Séries Temporais: Uma Abordagem Comparativa entre Modelos Univariados e Multivariados Híbridos

**FACULDADE POLI-UPE | ESCOLA POLITÉCNICA DE PERNAMBUCO**  
**DISCIPLINA: MINERAÇÃO DE DADOS**  
*Autor: Bruno Protásio | Equipe de Pesquisa em Engenharia e Ciência de Dados*  

---

## 1. Introdução do Projeto

**Tema Central:** Este projeto investiga a capacidade de previsão da inflação brasileira (IPCA) utilizando técnicas de mineração de séries temporais. Confrontamos duas estratégias: a abordagem univariada (que prevê o IPCA baseando-se apenas em seu próprio histórico) e a abordagem multivariada (que combina o histórico da inflação a variáveis macroeconômicas externas, como taxa Selic, câmbio, atividade econômica, emprego e combustíveis). Nosso objetivo é responder se a inclusão de dados externos traz ganho real de acurácia e quais indicadores econômicos são mais determinantes para antecipar a trajetória dos preços no Brasil.

A estabilidade de preços é essencial para a economia brasileira. A inflação corrói a renda das famílias, eleva os custos operacionais das empresas e aumenta as incertezas financeiras do país. O Índice Nacional de Preços ao Consumidor Amplo (IPCA), calculado mensalmente pelo IBGE, é o balizador oficial do regime de metas de inflação do Banco Central do Brasil. Por essa razão, antecipar o comportamento desse índice com precisão é uma necessidade crítica para a formulação de políticas públicas e para o planejamento financeiro corporativo.

### 1.1 Contextualização
No regime de metas de inflação, o Banco Central utiliza a taxa básica de juros (Selic) para conter pressões de preços. Como as decisões de juros levam entre 6 e 12 meses para surtir efeito pleno na economia, ter projeções de inflação confiáveis e tempestivas é pré-requisito fundamental para decisões assertivas.

A relevância da previsão da inflação sob a ótica da Mineração de Dados desdobra-se em três pilares práticos:
- **Setor Público e Regulatório:** Permite ancorar expectativas de mercado e avaliar o cumprimento das metas oficiais do Conselho Monetário Nacional (CMN);
- **Empresas e Mercado Financeiro:** Suporta a precificação de contratos de longo prazo, a gestão de estoques, orçamentos corporativos e ativos atrelados à inflação (como NTN-B e debêntures);
- **Pesquisa e Ciência de Dados:** Oferece um ambiente real e rigoroso para testar se modelos complexos de aprendizado de máquina compensam o aumento da dimensionalidade frente a modelos temporais parcimoniosos.

### 1.2 Descrição do Problema
A previsão da inflação enfrenta um dilema clássico de mineração de dados: avaliar se os preços são guiados principalmente por sua própria inércia temporal ou se a inclusão de fatores externos traz sinais antecipados cruciais:
1. **Abordagem Univariada (Apenas Histórico):** Explica o IPCA unicamente por defasagens passadas e sazonalidade, partindo da premissa de que o histórico recente sintetiza as informações mais relevantes.
2. **Abordagem Multivariada (Histórico + Fatores Externos):** Combina a inércia temporal a múltiplos indicadores macroeconômicos de preços setoriais, moeda, câmbio, emprego e energia.

Contudo, adicionar variáveis em excesso pode introduzir ruído e multicolinearidade, prejudicando os modelos. Por isso, a investigação deve responder não só se a abordagem multivariada é superior, mas quais grupos de variáveis realmente agregam valor preditivo.

> **Pergunta Central de Pesquisa:** *"A utilização de variáveis macroeconômicas exógenas melhora a acurácia da previsão do IPCA em relação a modelos puramente univariados? Quais grupos de indicadores possuem maior capacidade de antecipar a inflação brasileira?"*

### 1.3 Objetivos

#### 1.3.1 Objetivo Geral
Desenvolver, comparar e validar modelos preditivos de mineração de dados em séries temporais para a previsão do IPCA brasileiro, confrontando o desempenho das abordagens univariada e multivariada e identificando os atributos macroeconômicos mais relevantes.

#### 1.3.2 Objetivos Específicos
1. **Engenharia de Dados:** Coletar, higienizar e consolidar a série histórica mensal do IPCA e de 28 variáveis exógenas de março de 2012 a agosto de 2026 via API oficial do SGS/Banco Central;
2. **Categorização Setorial:** Agrupar as variáveis exógenas em quatro dimensões macroeconômicas: Índices de Preços, Setor Financeiro/Câmbio, Atividade/Emprego e Energia/Combustíveis;
3. **Modelagem de Referência (*Baseline*):** Calibrar modelos univariados clássicos (ARIMA) para estabelecer a base mínima de comparação;
4. **Modelagem Multivariada e Híbrida:** Implementar modelos lineares (ARIMAX, Lasso) e arquiteturas híbridas (ARIMAX + Random Forest) que modelam conjuntamente a tendência linear e os resíduos não lineares;
5. **Seleção Inteligente de Atributos:** Aplicar meta-heurísticas bioinspiradas (Algoritmo Genético - GA e Otimização por Enxame de Partículas - PSO) para encontrar os subconjuntos ótimos de variáveis;
6. **Validação Temporal Walk-Forward:** Avaliar as previsões com divisão sequencial 80% treino e 20% teste em horizonte de 1 passo à frente, prevenindo rigorosamente o vazamento de dados futuros (*lookahead bias*).

### 1.4 Justificativa e Impacto
Compreender a previsibilidade da inflação contribui diretamente para a redução de riscos econômicos no país. Para os agentes econômicos, antecipar variações nos preços viabiliza decisões financeiras conscientes e reduz custos de incerteza. Para a ciência de dados, este projeto preenche uma lacuna prática ao comparar sistematicamente modelos lineares e não lineares sob rigoroso esquema de validação walk-forward em uma economia emergente caracterizada por volatilidade e choques exógenos frequentes.

### 1.5 Escopo Negativo
Para manter o foco metodológico, este trabalho delimita claramente o que não faz parte do seu escopo:
- **Previsões em Alta Frequência:** O estudo analisa dados mensais e não desenvolve previsões diárias ou intradiárias de preços;
- **Análise Microeconômica Individual:** Não são avaliadas cestas de consumo de indivíduos ou domicílios específicos;
- **Recomendação de Políticas Públicas:** O objetivo é puramente preditivo e comparativo, sem proposição prescritiva de política monetária.

---

## 2. Fundamentação Teórica e Trabalhos Relacionados

### 2.1 Dinâmica Macroeconômica da Inflação no Brasil
A dinâmica dos preços no Brasil é orientada por três canais fundamentais: (i) a inércia inflacionária, que propaga variações passadas por contratos indexados; (ii) os choques de oferta e custos, com destaque para a oscilação do dólar (repasse cambial) e cotações de commodities energéticas; e (iii) as pressões de demanda agregada, refletidas no nível de desemprego e na atividade econômica. Essa pluralidade de estímulos justifica testar se conjuntos específicos de variáveis agregam poder preditivo superior ao simples histórico do índice.

### 2.2 Mineração de Séries Temporais e Seleção de Atributos
Séries temporais econômicas contêm desafios particulares: tendência estocástica, quebras estruturais e relacionamentos lineares e não lineares simultâneos. Além disso, incluir dezenas de covariáveis macroeconômicas pode saturar os modelos (a chamada maldição da dimensionalidade). Por isso, o uso de meta-heurísticas de busca estocástica, como Algoritmos Genéticos (GA) e Enxame de Partículas (PSO), destaca-se na literatura como solução eficiente para identificar subconjuntos de variáveis compactos e preditivos.

### 2.3 Trabalhos Relacionados
A literatura científica sobre modelagem da inflação organiza-se em três eixos principais:
1. **Modelos Lineares Tradicionais:** A metodologia clássica de Box e Jenkins [1] (ARIMA e SARIMA) permanece como a base de referência para capturar autocorrelação temporal e sazonalidade em séries de preços;
2. **Arquiteturas Híbridas (Linear + Não Linear):** Zhang [3] propôs a combinação entre ARIMA (para capturar a estrutura linear) e Redes Neurais / Random Forest (para modelar os resíduos não lineares), demonstrando reduções substanciais de erro em comparação a modelos isolados [4];
3. **Meta-heurísticas na Seleção de Atributos:** Estudos recentes utilizam Algoritmos Genéticos e PSO para selecionar variáveis macroeconômicas em bases de alta dimensionalidade, provando que modelos com 5 a 7 atributos bem selecionados superam modelos com todas as variáveis [5, 6].

---

## 3. Planejamento, Governança e Dados do Projeto

### 3.1 Stakeholders do Projeto
O desenvolvimento deste trabalho conecta-se a quatro grupos principais de interesse:
- **Comunidade Acadêmica:** Estudantes e pesquisadores de ciência de dados aplicados a problemas econômicos reais;
- **Mercado Financeiro e Investidores:** Gestores de fundos e analistas de risco que necessitam de projeções para títulos indexados à inflação (NTN-B/IPCA+);
- **Setor Corporativo:** Departamentos de planejamento orçamentário que utilizam projeções do IPCA para reajustes salariais e contratos de fornecimento;
- **Setor Público:** Órgãos governamentais e formuladores de políticas públicas que monitoram a evolução de preços.

### 3.2 Base de Dados e Contextualização Macroeconômica
A base de dados empírica foi construída por meio da coleta automatizada de séries temporais oficiais disponibilizadas na API pública do Sistema Gerenciador de Séries Temporais do Banco Central (SGS/BACEN). O horizonte histórico abrange observações mensais contínuas (frequência Month Start - MS) de março de 2012 a agosto de 2026, totalizando 174 meses sem lacunas amostrais.

O conjunto de dados consolida 1 variável dependente alvo (IPCA) e 28 variáveis exógenas (preditoras), estruturadas em quatro dimensões macroeconômicas funcionais da economia brasileira:
- **Índices de Preços e Desagregações Setoriais (11 variáveis):** Subíndices do IPCA (Alimentação, Transportes, Habitação, Saúde, Vestuário, Educação e Despesas Pessoais) e índices gerais de preços (INPC, IGP-M, IGP-DI e IPC-BR);
- **Setor Financeiro, Moeda e Câmbio (3 variáveis):** Taxa básica de juros (Selic Over), taxa de câmbio média PTAX (USDBRL) e reservas internacionais;
- **Atividade Econômica e Mercado de Trabalho (7 variáveis):** PIB Mensal a preços correntes, taxa de desocupação (PNAD Contínua), salário mínimo nacional, estoques de empregos formais ativos do CAGED (Total, Agropecuária e Construção Civil) e produção física de ovos;
- **Energia e Combustíveis (6 variáveis):** Volume de refino de derivados de petróleo, consumo aparente de gasolina automotiva, consumo de óleo combustível e consumo faturado de energia elétrica (Comercial, Residencial e Total).

Para evitar redundância de inventários no texto, a especificação técnica completa de cada variável (código SGS, unidade, teste de estacionariedade ADF e seleção por meta-heurísticas) está detalhada de forma consolidada no Dicionário de Dados Final (Tabela 2), apresentado na Seção 3.4.4 após a descrição dos procedimentos de pré-processamento.

#### 3.2.1 Delimitação Temporal e Justificativa Metodológica (2012 a 2026)
A escolha de março de 2012 como ponto inicial do painel fundamenta-se em três critérios metodológicos rigorosos:
1. **Transição da Medição do Desemprego pelo IBGE:** Em março de 2012, o IBGE implementou a Pesquisa Nacional por Amostra de Domicílios Contínua (PNAD Contínua), substituindo a antiga Pesquisa Mensal de Emprego (PME), restrita a 6 regiões metropolitanas. Usar dados anteriores geraria quebra estrutural severa na série de emprego;
2. **Nova Ponderação da Cesta do IPCA:** Em janeiro de 2012, o IBGE atualizou os pesos de consumo com base na POF 2008-2009, alterando a composição dos gastos das famílias brasileiras;
3. **Painel Balanceado no SGS/BACEN:** Diversas séries desagregadas do Banco Central só passaram a ser apuradas de maneira contínua e sem interrupções a partir de 2012.

---

### 3.3 Análise Exploratória dos Dados e Caracterização dos Atributos
A análise exploratória de dados (EDA) avalia a distribuição dos valores, a presença de assimetria, a dispersão estatística e os valores extremos (*outliers*) da série histórica antes da calibração dos modelos preditivos. Para atender aos critérios metodológicos da disciplina, selecionamos e caracterizamos um atributo contínuo numérico primordial e um atributo categórico nominal institucionalmente fundamentado.

#### 3.3.1 Seleção e Justificativa dos Atributos Numérico e Nominal
1. **Atributo Numérico Contínuo (`IPCA`):** Consiste na taxa percentual mensal de variação da inflação oficial (SGS/BACEN código 4447). Trata-se da variável dependente alvo (*target*, $y$) que os modelos irão prever.
2. **Atributo Nominal Categórico (`Regime de Inflação`):** Construído com base no Regime de Metas para a Inflação estipulado pelo Conselho Monetário Nacional (CMN/BACEN). Discretizamos a série mensal contínua em três classes qualitativas mutuamente exclusivas:
   - **Deflação** ($IPCA < 0{,}00\%$): Meses com queda atípica generalizada de preços provocada por choques pontuais de demanda ou desonerações fiscais;
   - **Meta / Estável** ($0{,}00\% \le IPCA \le 0{,}50\%$): Meses compatíveis com o centro da meta oficial anualizada do BACEN (equivalente a taxas mensais de 0,25% a 0,50% a.m.);
   - **Alta / Acima da Meta** ($IPCA > 0{,}50\%$): Meses com pressão inflacionária excessiva que demandam aperto de política monetária.

#### 3.3.2 Distribuição de Frequências e Métricas Descritivas
A análise da amostra atualizada (março de 2012 a agosto de 2026, com 174 meses contínuos) aponta a predominância de meses dentro da meta oficial, conforme demonstrado na Tabela 1.

#### Tabela 1 – Distribuição de Frequência do Atributo Nominal (Regime de Inflação)
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Deflação** | $IPCA < 0{,}00\%$ | 27 | 15,52% | 27 | 15,52% |
| **Meta / Estável** | $0{,}00\% \le IPCA \le 0{,}50\%$ | 77 | 44,25% | 104 | 59,77% |
| **Alta / Acima da Meta** | $IPCA > 0{,}50\%$ | 70 | 40,23% | 174 | 100,00% |
| **Total Geral Amostral** | **Horizonte 2012–2026** | **174** | **100,00%** | **174** | **100,00%** |

Principais estimadores estatísticos do IPCA contínuo na amostra:
- **Média e Mediana:** Média de 0,4324% ao mês e mediana de 0,4150% ao mês;
- **Dispersão:** Desvio padrão amostral de 0,4719% e variância de 0,2226;
- **Assimetria e Curtose:** Assimetria positiva (+0,5287), indicando cauda direita alongada por choques de alta, e curtose de +0,3736 (fracamente leptocúrtica);
- **Valores Extremos:** Mínimo histórico de -0,7400% (junho/2023) e máximo de +1,9500% (dezembro/2019);
- **Quartis e Intervalo Interquartílico:** $Q_1 = 0{,}0800\%$, $Q_3 = 0{,}6775\%$ e $IQR = 0{,}5975$ p.p.

#### 3.3.3 Análise Visual: Histograma, Boxplot e Gráfico de Dispersão
- **Histograma (Figura 1):** A distribuição da inflação concentra-se entre 0,10% e 0,60% ao mês. A proximidade entre média e mediana reforça a regularidade central, enquanto a assimetria positiva (+0,53) demonstra que choques inflacionários são mais acentuados do que quedas de preço.
- **Boxplot (Figura 2):** Identifica 5 outliers pelo critério de Tukey: dezembro/2019 (+1,95%), outubro/2020 (+1,72%), novembro/2020 (+1,61%), dezembro/2020 (+1,58%) e dezembro/2021 (+1,58%), correspondendo a choques de carnes e restrições de cadeias globais durante a pandemia. A variabilidade da classe "Alta" é muito mais ampla do que na classe "Meta", justificando o emprego de modelos híbridos.
- **Gráfico de Dispersão (Figura 3):** Evidencia a relação positiva entre desvalorização cambial e inflação (*pass-through*). À medida que a cotação do dólar sobe, a proporção de observações no regime de "Alta" aumenta perceptivelmente.
- **Distribuição dos Regimes (Figura 4):** 44,25% dos meses situaram-se dentro da meta, 40,23% em patamares elevados e 15,52% em deflação.

#### 3.3.4 Governança, Integridade e Requisitos de Qualidade
O tratamento dos dados segue rigorosamente a Lei Geral de Proteção de Dados Pessoais (LGPD – Lei nº 13.709/2018). As séries temporais empregadas são dados macroeconômicos públicos e agregados (SGS/BACEN, IBGE, FGV e Ministério do Trabalho), sem identificadores individuais. Sob a perspectiva de engenharia de dados, garantimos: (i) prevenção estrita de vazamento prospectivo (*lookahead bias*); (ii) completude amostral de 100% sem lacunas no período de 2012 a 2026; e (iii) reprodutibilidade científica por meio de scripts Python automatizados.

---

## 3.4 Pré-processamento dos Dados e Dicionário de Dados Final
O pré-processamento transforma as séries econômicas brutas em um painel equilibrado, consistente e apto a alimentar os estimadores lineares e não lineares. Esse fluxo é organizado em três etapas fundamentais: Limpeza, Redução e Transformação.

### 3.4.1 Limpeza e Saneamento de Dados (Data Cleaning)
1. **Sincronização Cronológica:** Séries diárias do mercado financeiro (taxa de câmbio PTAX e taxa Selic) foram convertidas para médias mensais de dias úteis e alinhadas sob frequência contínua Month Start (MS) de março de 2012 a agosto de 2026;
2. **Tratamento de Zeros Estruturais:** Em fluxos e estoques contínuos (refino de petróleo, consumo de combustíveis, energia e estoque do CAGED), zeros espúrios causados por atrasos de declaração contábil foram substituídos por valores nulos (NaN) para não distorcer variações percentuais;
3. **Sanitização Numérica:** Valores infinitos positivos ou negativos ($\pm\infty$) decorrentes de potenciais divisões aritméticas foram substituídos por NaN;
4. **Imputação Temporal sem Vazamento de Dados:** Valores faltantes foram tratados via interpolação linear temporal contínua indexada por datas (`interpolate(method='time')`). Para regressores de Machine Learning, qualquer imputação estatística é calibrada no treino e aplicada de forma cega no teste;
5. **Diagnóstico de Outliers e Preservação de Choques Reais:** Choques genuínos (deflação da COVID-19 em 2020 e desonerações tributárias em 2022) foram integralmente preservados para os modelos ARIMA e ARIMAX, enquanto modelos de aprendizado de máquina contam com winsorização conservadora (percentis 1% e 99% no treino) para evitar distorções espaciais nos pesos.

### 3.4.2 Técnicas de Redução de Dados e Dimensionalidade (Data Reduction)
1. **Redução Amostral Estrutural (Truncamento pós-2012):** O descarte intencional de registros anteriores a março de 2012 eliminou quebras estruturais severas da transição PME para PNAD Contínua e da reformulação da cesta da POF;
2. **Seleção de Atributos por Meta-heurísticas (GA e PSO):** Dos 27 atributos exógenos candidatos, Algoritmos Genéticos (GA) e Enxame de Partículas (PSO) selecionaram os subconjuntos ótimos de 5 variáveis-chave. No modelo campeão (ARIMAX + Random Forest), o PSO selecionou: `IPCA_Transportes`, `IGP_DI`, `Produção_Derivados_Petróleo`, `Consumo_Gasolina` e `Estoque_Empregos_Formais_Total`, reduzindo a dimensionalidade em mais de 80% e alcançando o menor erro do estudo (RMSE de 0,1046).

### 3.4.3 Transformação de Dados e Engenharia de Atributos (Data Transformation)
1. **Particionamento Temporal Cronológico 80/20:** A base tratada foi dividida estritamente em ordem cronológica (sem embaralhamento) em 80% para treino e 20% para teste, suportando o esquema walk-forward (previsões dinâmicas de 1 passo à frente);
2. **Teste ADF e Estacionarização Automática:** Modelos ARIMA pressupõem séries estacionárias. O teste Augmented Dickey-Fuller (ADF a 5%) confirmou que o IPCA e os subíndices de preços são I(0) (estacionários em nível). Séries com raiz unitária (como PIB, Câmbio e Combustíveis) foram submetidas à primeira diferenciação sucessiva ($\Delta X_t = X_t - X_{t-1}$), eliminando regressão espúria;
3. **Engenharia de Defasagens Temporais (Lags):** Criamos defasagens autoregressivas de 1 a 3 meses para capturar o tempo de transmissão de decisões de juros e oscilações cambiais até os preços ao consumidor;
### 3.4.4 Dicionário de Dados Final do Projeto
Como síntese de todas as etapas de saneamento, estacionarização e seleção bioinspirada, a Tabela 2 apresenta o Dicionário de Dados Final do projeto, especificando cada atributo, seu código SGS, tipo computacional, transformação matemática aplicada, resultado do teste ADF e papel metodológico nos modelos preditivos.

---

## Referências Bibliográficas

- [1] BOX, G. E.; JENKINS, G. M.; REINSEL, G. C.; LJUNG, G. M. *Time Series Analysis: Forecasting and Control*. 5. ed. Hoboken: John Wiley & Sons, 2015.
- [2] BANCO CENTRAL DO BRASIL (BACEN). *Sistema Gerenciador de Séries Temporais (SGS)*. Disponível em: <https://www3.bcb.gov.br/sgspub/>. Acesso em: 16 set. 2026.
- [3] ZHANG, G. P. Time series forecasting using a hybrid ARIMA and neural network model. *Neurocomputing*, v. 50, p. 159–175, 2003.
- [4] KHANDANI, A. E.; KIM, A. J.; LO, A. W. Consumer credit-risk models via machine-learning algorithms. *Journal of Banking & Finance*, v. 34, n. 11, p. 2767–2787, 2010.
- [5] KENNEDY, J.; EBERHART, R. Particle swarm optimization. In: *Proceedings of ICNN'95 - International Conference on Neural Networks*, v. 4, p. 1942–1948, 1995.
- [6] HOLLAND, J. H. *Adaptation in Natural and Artificial Systems: An Introductory Analysis with Applications to Biology, Control, and Artificial Intelligence*. Cambridge: MIT Press, 1992.
- [7] INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). *Sistema Nacional de Índices de Preços ao Consumidor (SNIPC): Metodologia do IPCA e INPC*. Rio de Janeiro: IBGE, 2020.
- [8] HYNDMAN, R. J.; ATHANASOPOULOS, G. *Forecasting: Principles and Practice*. 3. ed. Melbourne: OTexts, 2021.
- [9] HASTIE, T.; TIBSHIRANI, R.; FRIEDMAN, J. *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*. 2. ed. New York: Springer, 2009.
- [10] PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, v. 12, p. 2825–2830, 2011.
