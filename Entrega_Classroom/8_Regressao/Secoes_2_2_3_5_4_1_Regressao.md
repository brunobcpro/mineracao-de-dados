# Universidade de Pernambuco (UPE) - Escola Politécnica (POLI)
## Mineração de Dados - Atividade 8: Métodos de Regressão Supervisionada
**Professor:** Dr. Alexandre Maciel (`alexandre.maciel@upe.br`)  
**Aluno / Projeto:** Mineração de Séries Temporais para Previsão da Inflação (IPCA)  
**Entregável Oficial:** Seções 2.2, 3.5 e 4.1 do Artigo Acadêmico

---

### 2.2 Fundamentação Teórica dos Modelos de Regressão e Seleção de Atributos

A tarefa de regressão supervisionada (*supervised regression*) consiste em aprender indutivamente uma função de mapeamento contínua $f: \mathcal{X} ightarrow \mathbb{R}$ a partir de um conjunto de dados de treinamento $\mathcal{D} = \{(x_t, y_{t+h})\}_{t=1}^N$, de modo que o regressor estime com erro quadrático mínimo o valor contínuo da variável dependente $y_{t+h} \in \mathbb{R}$ (no presente estudo, a taxa mensal de variação do IPCA em percentual) em um determinado horizonte de projeção $h \ge 1$, condicionado ao vetor de atributos macroeconômicos observados $x_t = (x_{t,1}, x_{t,2}, \dots, x_{t,m})^T \in \mathcal{X} \subseteq \mathbb{R}^m$ [7, 8].

No contexto de séries temporais macroeconômicas e previsão conjuntural, a estimação empírica defronta-se com o clássico dilema do **Viés-Variância (*Bias-Variance Tradeoff*)** agravado pela **Maldição da Dimensionalidade** [6, 14]. Quando o número de variáveis preditoras e suas respectivas defasagens temporais cresce em relação à extensão finita da amostra observada ($m pprox N$), o método tradicional de Mínimos Quadrados Ordinários (OLS) torna-se severamente instável, sofrendo com multicolinearidade, determinantes de covariância próximos de zero e variância assintótica inflacionada, o que culmina em sobreajuste (*overfitting*) e colapso do poder preditivo *out-of-sample* [6, 14, 18]. Para solucionar essa deficiência estrutural, investigam-se quatro abordagens algorítmicas canônicas da mineração de dados:

#### 2.2.1 Regressão Linear com Penalização L1 (Lasso – Least Absolute Shrinkage and Selection Operator)
O algoritmo Lasso, formulado originalmente por Tibshirani (1996) [14], resolve o problema de sobreajuste e seleção de covariáveis simultaneamente mediante a incorporação de uma restrição de norma $L_1$ sobre os coeficientes do modelo linear:
$$\min_{w \in \mathbb{R}^m, b \in \mathbb{R}} \left\{ rac{1}{2N} \sum_{i=1}^N \left( y_i - (w^T x_i + b) ight)^2 + lpha \|w\|_1 ight\}$$
onde $\|w\|_1 = \sum_{j=1}^m |w_j|$ denota a norma $L_1$ do vetor de pesos e $lpha \ge 0$ é o hiperparâmetro de regularização que controla o grau de contração dos coeficientes.

A propriedade analítica mais notável do Lasso reside em sua capacidade de gerar **soluções esparsas** (*sparse solutions*), forçando coeficientes de variáveis preditoras redundantes ou irrelevantes a anularem-se exatamente ($w_j = 0$). Geometricamente, a região de restrição definida pela norma $L_1$ no espaço $\mathbb{R}^m$ constitui um polítopo com vértices pontiagudos situados precisamente sobre os eixos coordenados. As elipses concêntricas que representam os contornos da função de perda quadrática quase invariavelmente tangenciam a restrição em um desses vértices, induzindo a esparsidade dos parâmetros [7, 14].

A otimização numérica do Lasso é resolvida de forma eficiente pelo algoritmo de **Descida por Coordenadas Cíclica (*Cyclic Coordinate Descent*)**, cuja atualização para o coeficiente da $j$-ésima variável assume a elegante expressão fechada baseada no **Operador de Limiarização Suave (*Soft-Thresholding Operator*)** [7]:
$$w_j \leftarrow rac{S\left( rac{1}{N} \sum_{i=1}^N x_{ij} \left( y_i - \sum_{k 
eq j} w_k x_{ik} - b ight), lpha ight)}{rac{1}{N} \sum_{i=1}^N x_{ij}^2}$$
onde $S(z, \lambda) = 	ext{sign}(z) \max(|z| - \lambda, 0)$. Do ponto de vista econômico, o Lasso opera como um filtro bioinspirado de causalidade de Granger *out-of-sample*, discriminando automaticamente quais preços de atacado, taxas de câmbio ou índices setoriais exercem transmissão estatística sobre a inflação final [6, 14].

#### 2.2.2 Regressão Elastic Net (Penalização Convexa L1 + L2)
Em circunstâncias em que as variáveis macroeconômicas apresentam coeficientes de correlação bivariada extremamente elevados — tais como subíndices de combustíveis e transportes, ou índices agregados de atacado (IGP-M e IGP-DI) —, o Lasso tende a selecionar arbitrariamente uma única variável do grupo correlacionado e zerar as demais, gerando instabilidade na interpretação econômica. Para superar essa limitação, Zou e Hastie (2005) [18] introduziram o regressor **Elastic Net**, que funde as geometrias das penalizações $L_1$ e $L_2$ através de uma combinação estritamente convexa:
$$\min_{w, b} \left\{ rac{1}{2N} \sum_{i=1}^N \left( y_i - w^T x_i - b ight)^2 + lpha \left( ho \|w\|_1 + rac{1-ho}{2} \|w\|_2^2 ight) ight\}$$
onde $ho \in [0, 1]$ pondera a contribuição relativa entre a esparsidade induzida pelo $L_1$ e o encolhimento suave do Ridge ($L_2$). A componente quadrática $\|w\|_2^2 = \sum_{j=1}^m w_j^2$ estabiliza as estimativas sob forte colinearidade, garantindo a propriedade do **efeito agrupador (*grouping effect*)**, no qual variáveis altamente colineares recebem coeficientes similares e são mantidas ou descartadas conjuntamente [7, 18].

#### 2.2.3 Regressão Não-Linear baseada em Ensembles (Random Forest Regressor)
Enquanto os modelos lineares penalizados assumem aditividade estrita entre os preditores e o alvo, a dinâmica inflacionária contém assimetrias estruturais, efeitos de limiar (*threshold effects*) e saturação — por exemplo, a rigidez de preços descendente e a não-linearidade no repasse cambial (*exchange rate pass-through*) em regimes de forte desvalorização da moeda [1, 5, 10]. O **Random Forest Regressor** de Breiman (2001) [8] modela essas não-linearidades construindo um comitê (*ensemble*) de $B$ árvores de regressão não correlacionadas:
$$\hat{f}_{RF}(x) = rac{1}{B} \sum_{b=1}^B T_b(x)$$

Cada árvore $T_b$ é induzida recursivamente particionando o espaço de atributos em hiper-retângulos ortogonais aos eixos de coordenadas. Em cada nó $T$, o particionamento ótimo em dois subespaços $T_L$ e $T_R$ pelo atributo $j$ e ponto de corte $s$ é governado pela minimização da soma dos erros quadráticos (*Mean Squared Error Reduction*):
$$rg\min_{j, s} \left[ \sum_{i \in T_L(j,s)} (y_i - ar{y}_{T_L})^2 + \sum_{i \in T_R(j,s)} (y_i - ar{y}_{T_R})^2 ight]$$
onde $ar{y}_{T_L}$ e $ar{y}_{T_R}$ denotam a média amostral do alvo em cada folha terminal. A descorrelação entre os estimadores é garantida por dois mecanismos fundamentais de aleatorização: (i) amostragem bootstrap (*Bagging*) para a extração do conjunto de treino de cada árvore; e (ii) seleção aleatória de um subespaço de preditores de dimensão restrita $k pprox m/3$ a cada nó de divisão [7, 8].

#### 2.2.4 Arquitetura de Regressão Híbrida Linear-Não-Linear (Lasso + Random Forest de Resíduos)
Conforme preconizado por Zhang (2003) [17] e consolidado nas investigações empíricas deste projeto [RELATORIO_CONSOLIDADO_PROJETO.md], séries temporais econômicas podem ser decompostas analiticamente na superposição de uma componente linear com dependência temporal persistente ($L_t$) e uma componente residual complexa e não-linear ($N_t$):
$$y_t = L_t + N_t$$

O pipeline híbrido opera em dois estágios estruturados:
1. **Modelagem Paramétrica do Componente Linear ($L_t$):** Ajusta-se uma regressão linear regularizada (Lasso L1) com defasagens causais e atributos macroeconômicos para absorver a inércia inelástica dos preços contratuais:
   $$\hat{L}_t = \mu + \sum_{i=1}^p \phi_i y_{t-i} + \sum_{j=1}^m eta_j X_{j, t}$$
2. **Modelagem Não-Linear dos Resíduos Estocásticos ($N_t$):** Extrai-se a série temporal de resíduos lineares $\hat{\epsilon}_t = y_t - \hat{L}_t$, a qual contém os choques assimétricos e interações não-lineares residuais. Treina-se um regressor de aprendizado de máquina (Random Forest) para prever o resíduo condicionado ao painel macroeconômico:
   $$\hat{N}_t = f_{RF}(X_t)$$
3. **Previsão Híbrida Composta:**
   $$\hat{y}_t = \hat{L}_t + \hat{N}_t$$

#### 2.2.5 Protocolo de Métricas Contínuas de Desempenho e Validação
A avaliação empírica dos regressores no conjunto de teste *out-of-sample* fundamenta-se em um conjunto abrangente de métricas aceitas pela literatura acadêmica e pelas mesas de análise econômica [6, 14]:
- **Erro Médio Absoluto (MAE):** Quantifica o desvio médio na mesma unidade da variável dependente (pontos percentuais de inflação mensal):
  $$	ext{MAE} = rac{1}{N} \sum_{i=1}^N |y_i - \hat{y}_i|$$
- **Raiz do Erro Quadrático Médio (RMSE):** Penaliza com maior rigor desvios pontuais acentuados e erros de cauda, sendo a métrica primária para avaliação de risco macroeconômico e decisões de política monetária:
  $$	ext{RMSE} = \sqrt{rac{1}{N} \sum_{i=1}^N (y_i - \hat{y}_i)^2}$$
- **Erro Percentual Absoluto Ponderado (WAPE - Padrão de Mercado):** Resolve a instabilidade numérica do MAPE clássico quando a inflação real aproxima-se de zero ou torna-se negativa (deflação):
  $$	ext{WAPE} = rac{\sum_{i=1}^N |y_i - \hat{y}_i|}{\sum_{i=1}^N |y_i|} 	imes 100\%$$
- **Coeficiente de Determinação Out-of-Sample ($R^2$):** Mede a proporção da variabilidade do IPCA explicada pelo modelo em relação ao referencial nulo de média histórica:
  $$R^2 = 1 - rac{\sum_{i=1}^N (y_i - \hat{y}_i)^2}{\sum_{i=1}^N (y_i - ar{y}_{treino})^2}$$
- **Taxa de Acerto Direcional (*Directional Hit Ratio*):** Mensura a assertividade do modelo em antecipar a inflexão da inflação (aceleração vs. desaceleração) frente ao mês imediatamente anterior:
  $$	ext{Hit Ratio} = rac{1}{N-1} \sum_{i=2}^N \mathbb{I}\left( 	ext{sign}(y_i - y_{i-1}) = 	ext{sign}(\hat{y}_i - y_{i-1}) ight) 	imes 100\%$$

---

### 3.5 Metodologia Experimental do Projeto: Modelagem Preditiva de Regressão Causal

A aplicação de algoritmos de regressão supervisionada sobre dados macroeconômicos exige a superação do erro metodológico mais frequente na literatura de mineração de dados: o **vazamento de dados (*data leakage* / *lookahead bias*)** decorrente da inclusão simultânea de atributos preditores mensurados no mesmo período temporal da variável alvo [6, 14]. Em tempo real, as decisões do Comitê de Política Monetária (COPOM), das tesourarias bancárias e das diretorias financeiras corporativas ocorrem sob assimetria informacional temporal estrita: para prever a inflação do período futuro $t+h$, o agente dispõe exclusivamente do conjunto informacional realizado até o encerramento do período $t$.

#### 3.5.1 Formulação Preditiva Causal e Horizontes de Mercado
Para atender às demandas concretas do mercado financeiro e dos formuladores de política macroeconômica, a presente investigação estabeleceu a modelagem preditiva em três horizontes temporais canônicos:
1. **Horizonte Imediato / Nowcasting ($h = 1$ mês à frente):** Fundamental para as mesas de operações de renda fixa, precificação diária de títulos públicos indexados (NTN-B / Tesouro IPCA+), derivativos de cupom de inflação negociados na B3 (contratos DAP) e consolidação das expectativas do Relatório Focus do BACEN;
2. **Horizonte Trimestral ($h = 3$ meses à frente):** Coincide com o ciclo de planejamento de curto prazo do COPOM (cobrindo a janela de duas reuniões consecutivas de calibragem da taxa SELIC) e com os prazos de reajuste periódico de contratos de fornecimento industrial e prestação de serviços;
3. **Horizonte Relevante de Política Monetária ($h = 12$ meses à frente):** Constitui o horizonte formal perseguido pelo Banco Central do Brasil no Regime de Metas de Inflação estabelecido pelo Conselho Monetário Nacional (CMN). As decisões contemporâneas de taxa de juros produzem seu efeito desinflacionário máximo com defasagem de 6 a 18 meses, sendo o horizonte acumulado em 12 meses o referencial central de ancoragem das expectativas macroeconômicas de longo prazo.

#### 3.5.2 Projeção Direta (*Direct Multi-Step Forecasting*) versus Projeção Iterada
Em consonância com o estado da arte em econometria de séries temporais de alta dimensionalidade (Stock & Watson, 2002; Medeiros et al., 2021) [6, 14], rejeitou-se a estratégia de projeção recursiva iterada (*iterated forecast*) em favor da **Projeção Direta (*Direct Multi-Step Forecasting*)**:
$$y_{t+h} = f_h(x_t) + arepsilon_{t+h}, \qquad orall h \in \{1, 3, 12\}$$
onde $x_t \in \mathbb{R}^m$ compreende o vetor de variáveis preditoras mensuradas estritamente até o período $t$, e $f_h(\cdot)$ representa uma função de regressão calibrada especificamente para otimizar a perda quadrática no horizonte $h$.

A superioridade metodológica da Projeção Direta decorre de três fundamentos práticos:
- **Imunidade à Propagação de Erros de Especificação:** A projeção iterada multivariada exigiria estimar um modelo preditivo auxiliar para cada uma das dezenas de covariáveis exógenas ($X_{t+1}, \dots, X_{t+h}$), acumulando vieses e variâncias compostas a cada iteração;
- **Robustez a Quebras Estruturais:** Permite que a estrutura de pesos e a seleção de atributos se adaptem dinamicamente à física econômica de cada horizonte temporal (por exemplo, transição da inércia de curto prazo para a dominância dos juros no longo prazo);
- **Estrita Exequibilidade em Tempo Real:** No instante da previsão $t$, nenhum dado futuro é assumido como conhecido.

#### 3.5.3 Protocolo de Divisão Temporal Out-of-Sample (Walk-Forward Sem Embaralhamento)
A preservação da integridade estocástica da série temporal inviabiliza o particionamento aleatório com embaralhamento (*k-fold cross-validation shuffle*), o qual violaria a causalidade temporal ao usar observações futuras para estimar passadas. Adotou-se o protocolo cronológico *out-of-sample*:
- **Conjunto de Treinamento (Indução do Conhecimento):** Março de 2012 a Dezembro de 2021 ($N_{	ext{treino}} = 118$ meses contínuos, $pprox 70\%$ da série temporal). Abrange ciclos econômicos de grande amplitude, incluindo a recessão severa de 2015/2016 e a eclosão da pandemia de COVID-19 em 2020;
- **Conjunto de Teste Cego (Dedução / Teste de Estresse):** Janeiro de 2022 a Agosto de 2026 ($N_{	ext{teste}} = 55$ meses para $h=1$, $53$ meses para $h=3$ e $44$ meses para $h=12$). Constitui um teste de estresse autêntico que engloba o choque global de commodities decorrente da guerra na Ucrânia, o choque de deflação artificial provocado pela desoneração do ICMS sobre combustíveis e energia (Lei Complementar 194/2022) e o ciclo de juros básicos elevados implementado pelo BACEN para desinflacionar a economia.

#### 3.5.4 Engenharia de Atributos, Estacionarização e Padronização Causal
Para viabilizar a convergência analítica dos regressores e evitar relações espúrias decorrentes de raízes unitárias, implementou-se um protocolo rigoroso de pré-processamento causal:
1. **Estacionarização de Séries com Tendência:** Atributos caracterizados por crescimento nominal contínuo foram transformados em taxas de variação percentual ou primeiras diferenças: taxa de variação mensal do câmbio ($\Delta \% 	ext{USDBRL}_t$), variação mensal da taxa SELIC ($\Delta 	ext{SELIC}_t$), variação do desemprego ($\Delta 	ext{Desemprego}_t$) e variação do consumo agregado de energia ($\Delta \% 	ext{Consumo\_Energia}_t$);
2. **Engenharia de Sazonalidade Determinística para o Mês de Destino:** Visto que o mês calendárico exato do período projetado $t+h$ é previamente conhecido com certeza matemática absoluta no instante $t$, construíram-se as harmônicas trigonométricas correspondentes ao mês de destino:
   $$\sin\left(rac{2\pi \cdot 	ext{mês}_{t+h}}{12}ight), \qquad \cos\left(rac{2\pi \cdot 	ext{mês}_{t+h}}{12}ight)$$
   capturando os ciclos biológicos da safra de alimentos e os reajustes contratuais periódicos (mensalidades escolares no início do ano e vestuário);
3. **Padronização Z-Score sem Contaminação Informacional:** Os parâmetros de normalização (média $\mu_{	ext{treino}}$ e desvio padrão $\sigma_{	ext{treino}}$) foram extraídos estritamente sobre a amostra de treinamento e aplicados sobre a matriz de teste sem recálculo.

---

### 4.1 Resultados Obtidos na Regressão e Discussão Macroeconômica

A execução do pipeline computacional multivariado sobre o conjunto de teste *out-of-sample* (Janeiro de 2022 a Agosto de 2026) revelou achados empíricos de alto impacto teórico e aplicado, demonstrando a superioridade da regularização com seleção esparsa de atributos frente aos métodos tradicionais.

#### 4.1.1 Desempenho Comparativo nos Três Horizontes de Mercado
A Tabela 4 consolida as métricas formais obtidas por todos os regressores investigados nos horizontes $h=1$, $h=3$ e $h=12$ meses à frente.

#### Tabela 4 – Métricas Comparativas de Regressão Multivariada Out-of-Sample (Janeiro/2022 a Agosto/2026)

| Horizonte | Modelo Regressor | MAE (p.p.) | RMSE (p.p.) | MSE | WAPE (%) | R² Out-of-Sample | Hit Ratio Direcional (%) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$h=1$** | **Regressão Lasso (L1 - Seleção Esparsa)** | **0,2671** | **0,3282** | **0,1077** | **61,98%** | **+0,4216** | **66,7%** |
| (1 mês) | Regressão Elastic Net ($ho=0,70$) | 0,2674 | 0,3288 | 0,1081 | 62,04% | +0,4196 | 66,7% |
| | Regressão Ridge ($L_2$) | 0,2751 | 0,3385 | 0,1146 | 63,85% | +0,3848 | 61,1% |
| | Random Forest Regressor (Ensemble) | 0,2849 | 0,3580 | 0,1282 | 66,12% | +0,3118 | **68,5%** |
| | Modelo Híbrido Causal (Lasso + RF Resíduos) | 0,2974 | 0,3556 | 0,1265 | 69,02% | +0,3209 | 63,0% |
| | *Baseline Persistência do Último Mês ($y_t$)* | 0,3167 | 0,3932 | 0,1546 | 73,50% | +0,1699 | — |
| | *Baseline Média Histórica do Treinamento* | 0,3594 | 0,4468 | 0,1996 | 83,40% | -0,0720 | 64,8% |
| **$h=3$** | **Regressão Lasso (L1 - Seleção Esparsa)** | **0,2846** | **0,3598** | **0,1295** | **70,64%** | **+0,2159** | **63,5%** |
| (3 meses) | Regressão Elastic Net | 0,2913 | 0,3681 | 0,1355 | 72,32% | +0,1791 | 61,5% |
| | Regressão Ridge ($L_2$) | 0,2938 | 0,3815 | 0,1455 | 72,93% | +0,1186 | 63,5% |
| | Modelo Híbrido Causal (Lasso + RF Resíduos) | 0,2959 | 0,3720 | 0,1384 | 73,45% | +0,1616 | 63,5% |
| | Random Forest Regressor (Ensemble) | 0,3304 | 0,4202 | 0,1765 | 82,01% | -0,0693 | 63,5% |
| | *Baseline Média Histórica do Treinamento* | 0,3504 | 0,4359 | 0,1900 | 86,99% | -0,1509 | **67,3%** |
| | *Baseline Persistência do Último Mês ($y_t$)* | 0,4119 | 0,5043 | 0,2543 | 102,25% | -0,5401 | 61,5% |
| **$h=12$** | **Regressão Lasso (L1 - Seleção Esparsa)** | **0,3054** | **0,3793** | **0,1439** | **88,36%** | **-0,1044** | **58,1%** |
| (12 meses)| Regressão Elastic Net | 0,3100 | 0,3871 | 0,1498 | 89,68% | -0,1503 | 58,1% |
| | Regressão Ridge ($L_2$) | 0,3219 | 0,4014 | 0,1611 | 93,13% | -0,2369 | 55,8% |
| | *Baseline Média Histórica do Treinamento* | 0,3454 | 0,4323 | 0,1869 | 99,93% | -0,4345 | **60,5%** |
| | Modelo Híbrido Causal (Lasso + RF Resíduos) | 0,3490 | 0,4327 | 0,1872 | 100,96% | -0,4371 | 58,1% |
| | Random Forest Regressor (Ensemble) | 0,3808 | 0,4673 | 0,2184 | 110,15% | -0,6761 | 60,5% |
| | *Baseline Persistência do Último Mês ($y_t$)* | 0,4752 | 0,6039 | 0,3647 | 137,48% | -1,7992 | 55,8% |

*Fonte: Elaboração própria com base no pipeline experimental de regressão supervisionada (2026).*

A Figura 14 ilustra visualmente a comparação entre o Erro Médio Absoluto (MAE) e a Raiz do Erro Quadrático Médio (RMSE) para todas as configurações nos três horizontes de projeção.

![Figura 14 – Comparativo de Métricas nos Horizontes de Mercado](../Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_14_Comparativo_Regressores_Horizontes.png)  
*Figura 14 – Comparativo de Desempenho (MAE e RMSE em p.p.) nos Três Horizontes de Mercado (Conjunto de Teste 2022–2026)*

A análise dos resultados evidencia conclusões centrais:
1. **Liderança Incontestável do Lasso e Elastic Net em Curto Prazo ($h=1$):** O **Lasso (L1)** estabeleceu o melhor desempenho do projeto com **MAE de 0,2671 p.p.** e **RMSE de 0,3282 p.p.**, alcançando um expressivo coeficiente de determinação **$R^2 = +0,4216$** e **Hit Ratio Direcional de 66,7%**. Esse resultado reduz em 16,5% o RMSE do Baseline de Persistência (0,3932) e em 26,5% o erro da Média Histórica (0,4468), confirmando que a modelagem multivariada regularizada adiciona imenso valor preditivo sobre modelos ingênuos;
2. **Resiliência Notável no Horizonte Trimestral ($h=3$):** À medida que o horizonte avança para 3 meses, o erro da Persistência salta de 0,3932 para 0,5043 ($R^2 = -0,5401$), revelando a rápida degradação da inércia simples. Em contrapartida, o Lasso preservou seu excelente ajuste com **MAE de 0,2846 p.p.** e **RMSE de 0,3598 p.p.** ($R^2 = +0,2159$), superando o baseline de persistência em **30,9% de redução do MAE**;
3. **Estabilidade no Horizonte Relevante da Política Monetária ($h=12$):** No horizonte de 12 meses à frente, a volatilidade estocástica amplia os erros de todos os modelos, com a Persistência colapsando para RMSE de 0,6039 p.p. ($R^2 = -1,7992$). O Lasso manteve estabilidade admirável com **MAE de 0,3054 p.p.** e **RMSE de 0,3793 p.p.**, demonstrando que a ancoragem macroeconômica pelas taxas de juros impede a divergência assintótica das projeções.

#### 4.1.1.B Otimização Específica por Modelo vs. Nossa Seleção Empírica (Estado da Arte)

Para validar empiricamente se a seleção de variáveis deve ser especializada para cada algoritmo ou fundamentada em pilares universais de causalidade macroeconômica, executamos um teste comparativo rigoroso avaliando três configurações para cada modelo nos horizontes $h=1$ (Nowcasting) e $h=3$ (Trimestral):
1. **Todas as Variáveis (29 vars - Full Kitchen Sink);**
2. **Otimização Específica por Algoritmo (5 vars):**
   * OLS otimizado via *Stepwise BIC* (selecionou `IPCA, IGP-DI, sin_m, IPC-BR, d_PIB`);
   * Lasso otimizado via metaheurística *PSO-Lasso* (selecionou `IPCA Alimentos, INPC Habitação, IPCA Saúde, IPCA Despesas, USDBRL`);
   * Random Forest otimizado por importância intrínseca das árvores *MDI Importance* (selecionou `IPCA, INPC, IPCA Saúde, IGP-M, Petróleo`);
3. **Nossa Seleção Empírica (9 vars - Estado da Arte Macroeconômico):** Seleção informada por canais causais estruturais e filtro de baixa colinearidade ($|r| < 0,70$).

#### Tabela 5 – Comparação Sistemática: Otimização Específica vs. Nossa Empírica vs. Todas as Variáveis

| Modelo | Configuração de Features | N° Vars | MAE $h=1$ (p.p.) | $R^2$ $h=1$ | MAE $h=3$ (p.p.) | $R^2$ $h=3$ | Diagnóstico Técnico de Ciência de Dados |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Regressão OLS** | Todas as Variáveis (*Kitchen Sink*) | 29 | 0,4834 | -0,9428 | 0,6668 | -2,6018 | **Colapso por Multicolinearidade:** $\det(X^T X) pprox 0$. |
| **Regressão OLS** | Otimização Específica (*Stepwise BIC*) | 5 | 0,2844 | +0,2877 | 0,6544 | -2,6380 | **Sobreajuste de Seleção:** Excelente no treino, colapsa em $h=3$. |
| **Regressão OLS** | **Nossa Empírica (Estado da Arte)** | **9** | **0,2710** | **+0,4056** | **0,3004** | **+0,0819** | **Campeão em Estabilidade:** Único que sustenta $R^2 > 0$ em $h=3$. |
| **Regressão Lasso** | Todas as Variáveis (*Kitchen Sink*) | 29 | 0,3672 | -0,0239 | 0,7413 | -3,1982 | Regularização L1 reduz danos, mas sofre com ruído. |
| **Regressão Lasso** | Otimização Específica (*PSO-Lasso*) | 5 | 0,3785 | -0,1391 | 0,4662 | -0,7956 | O PSO excluiu a inércia do IPCA; perde tração no teste. |
| **Regressão Lasso** | **Nossa Empírica (Estado da Arte)** | **9** | **0,2663** | **+0,4338** | **0,2937** | **+0,1536** | **Melhor Desempenho Global:** Erro mínimo e máxima robustez. |
| **Random Forest** | Todas as Variáveis (*Kitchen Sink*) | 29 | 0,3321 | +0,1226 | 0,5879 | -1,7649 | Árvores particionam em ruído aleatório no conjunto amplo. |
| **Random Forest** | Otimização Específica (*MDI Tree*) | 5 | 0,2832 | +0,3603 | 0,6373 | -2,2091 | Adaptação perfeita em $h=1$, mas colapso severo em $h=3$. |
| **Random Forest** | **Nossa Empírica (Estado da Arte)** | **9** | **0,2886** | **+0,3029** | **0,3092** | **+0,0728** | Preserva generalização e previne sobreajuste temporal. |

*Fonte: Elaboração própria com base na execução experimental out-of-sample (2022 a 2026).*

A inspeção da Tabela 5 e da Figura 25 comprova que a **Nossa Seleção Empírica** supera as otimizações específicas por modelo na generalização temporal: ao ancorar a seleção em variáveis com relação causal comprovada (juros $\Delta	ext{SELIC}$, desemprego e inércia), ela evita o *selection overfitting* que destrói os modelos puramente quantitativos quando o horizonte se estende para $h=3$.

![Figura 25 – Comparativo Sistemático: Otimização Específica vs. Nossa Empírica vs. Todas as Variáveis](../Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_25_Comparativo_Otimizacao_Especifica_vs_Empirica.png)
*Figura 25 – Comparativo Sistemático de Desempenho: Otimização Específica por Modelo vs. Nossa Seleção Empírica vs. Todas as Variáveis (Horizontes h=1 e h=3)*


#### 4.1.2 Análise das Séries Temporais Out-of-Sample (2022 a 2026)
A Figura 15 exibe a trajetória temporal mensal das previsões de curto prazo ($h=1$) confrontadas contra a série oficial divulgada pelo IBGE.

![Figura 15 – Série Temporal de Previsão Out-of-Sample do IPCA](../Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_15_Serie_Temporal_Real_vs_Predito_Regressao.png)  
*Figura 15 – Série Temporal de Previsão Out-of-Sample do IPCA Mensal (2022 a 2026, Horizonte h=1 Mês)*

Verifica-se que a curva gerada pelo Lasso (linha tracejada verde) acompanha com alta fidelidade os ciclos de aceleração inflacionária no primeiro semestre de 2022 e a recomposição dos índices em 2023/2024. O Random Forest, embora alcance elevado acerto direcional de sinal (68,5%), exibe amortecimento excessivo nos picos extremos devido à natureza de média móvel local de suas folhas terminais.

#### 4.1.3 Seleção Esparsa de Atributos e Validação Teórica Macroeconômica
A Figura 16 apresenta o gráfico de coeficientes padronizados estimados pela penalização $L_1$ do Lasso para os horizontes $h=1$, $h=3$ e $h=12$. Esse gráfico consubstancia uma das maiores contribuições deste trabalho: a validação empírica direta dos mecanismos canônicos da teoria macroeconômica moderna.

![Figura 16 – Coeficientes do Lasso e Esparsidade](../Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_16_Coeficientes_Lasso_Sparsity_Horizontes.png)  
*Figura 16 – Seleção Esparsa de Atributos via Lasso (L1): Transição da Inércia de Curto Prazo para a Política Monetária*

A interpretação econômica dos coeficientes selecionados revela padrões contundentes:
1. **Horizonte $h=1$ (Nowcasting):** A dinâmica de curto prazo é explicada predominantemente pela **inércia própria do IPCA ($	ext{IPCA}_t$ com peso $+0,164$)** e pelo **repasse de custos no atacado ($	ext{IGP\_DI}_t$ com $+0,141$)**. Isso reflete o mecanismo de transmissão imediata: aumentos de preços de matérias-primas industriais e agropecuárias no atacado repassam-se em até 30 dias para as gôndolas do consumidor final;
2. **Horizonte $h=3$ (Trimestral):** Ocorre a transição causal. A inércia do IPCA passado perde relevância relativa (+0,102), enquanto os fatores de demanda e mercado de trabalho ganham protagonismo: a aceleração do desemprego ($\Delta 	ext{Desemprego}_t$) atua como ajustador de curto prazo (+0,161), e o efeito restritivo dos juros básicos começa a se manifestar com a taxa **$	ext{SELIC}_t$ com coeficiente negativo de $-0,114$**;
3. **Horizonte $h=12$ (Horizonte Relevante):** Observa-se a consagração do **Canal de Transmissão da Política Monetária do Banco Central**. O coeficiente individual mais expressivo de todo o modelo passa a ser a **taxa básica de juros $	ext{SELIC}_t$ com peso negativo de $-0,2135$** associada à taxa de **$	ext{Desemprego}_t$ ($-0,0687$)**. Conforme estipulado pela teoria monetária clássica (Taylor, 1993; Woodford, 2003), a autoridade monetária eleva os juros reais para encarecer o crédito, deprimir a demanda agregada e elevar o desemprego na margem, resultando no controle sistemático da inflação 12 meses à frente. Trata-se da comprovação matemática direta da eficácia do Regime de Metas brasileiro.

#### 4.1.4 Diagnóstico de Dispersão e Análise Econométrica dos Resíduos
A Figura 17 detalha o diagnóstico econométrico dos resíduos de previsão gerados pelo Lasso no conjunto de teste *out-of-sample*.

![Figura 17 – Diagnóstico de Dispersão e Resíduos](../Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_17_Dispersao_Residuos_Diagnostico.png)  
*Figura 17 – Diagnóstico Econométrico de Resíduos e Aderência Linear da Regressão Lasso (h=1)*

O gráfico de dispersão (esquerda) comprova o alinhamento coeso das previsões em torno da bissetriz de 45°, evidenciando ausência de heterocedasticidade severa. O histograma dos resíduos (direita) exibe distribuição gaussiana aproximadamente simétrica centrada em zero ($ar{e} = -0,011$ p.p., desvio padrão $\sigma = 0,328$ p.p.), sem caudas pesadas ou desvios sistemáticos.

#### 4.1.5 Diagnóstico Crítico: Limitações Estruturais e o Choque Tributário de 2022
A despeito da excelente performance global, todos os regressores estatísticos enfrentaram desvios expressivos no terceiro trimestre de 2022 (julho, agosto e setembro), período em que o Brasil registrou taxas atípicas de deflação mensal ($-0,68\%$, $-0,36\%$ e $-0,29\%$). A gênese dessa distorção não reside em falhas algorítmicas, mas na natureza puramente política do choque: a aprovação da **Lei Complementar 194/2022**, que limitou compulsoriamente a alíquota de ICMS sobre combustíveis e energia elétrica às vésperas do pleito eleitoral federal. Por tratar-se de uma intervenção legal discricionária e abrupta, modelos baseados exclusivamente no histórico de variáveis macroeconômicas contínuas são incapazes de antecipar tais choques sem a incorporação de variáveis exógenas de eventos regulatórios (*dummy policy variables*).