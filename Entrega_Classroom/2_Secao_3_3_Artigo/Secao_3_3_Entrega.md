# 3.3 Análise Exploratória dos Dados e Caracterização dos Atributos

A análise exploratória de dados (*Exploratory Data Analysis* – EDA) constitui etapa mandatória no fluxo de mineração de dados em séries temporais macroeconômicas. Sua finalidade é desvendar o comportamento distributivo, identificar padrões estocásticos de dispersão e assimetria, isolar valores extremos (*outliers*) decorrentes de choques exógenos e caracterizar formalmente a correlação entre os atributos antes da calibração dos modelos preditivos lineares e não lineares. Em cumprimento aos requisitos metodológicos da disciplina e do projeto de pesquisa, foram selecionados e caracterizados em profundidade um atributo contínuo numérico primordial e um atributo categórico nominal institucionalmente respaldado.

---

### 3.3.1 Seleção e Justificativa dos Atributos Numérico e Nominal

1. **Atributo Numérico Contínuo (`IPCA`):** Consiste na taxa de variação percentual mensal do Índice Nacional de Preços ao Consumidor Amplo (SGS/BACEN código 4447), apurada pelo IBGE. Trata-se da variável dependente primária (*target*, $y$) do projeto. Apresenta natureza quantitativa contínua, oscilando entre valores positivos em momentos de pressão inflacionária e valores negativos em conjunturas de choques atípicos de oferta e desonerações fiscais (deflação).
2. **Atributo Nominal Categórico (`Regime_Inflacao`):** Construído a partir da discretização orientada ao domínio econômico, fundamentada no **Regime de Metas para a Inflação** instituído pelo Decreto Federal nº 3.088/1999 e regulamentado pelo Conselho Monetário Nacional (CMN). Para viabilizar a análise estatística de classes em mineração de dados, a série temporal contínua foi categorizada em três regimes qualitativos mutuamente exclusivos:
   - **`Deflação`** ($IPCA < 0{,}00\%$): caracterizando episódios de choque estocástico negativo de preços;
   - **`Meta / Estável`** ($0{,}00\% \le IPCA \le 0{,}50\%$): intervalo representativo da convergência da inflação com o centro da meta oficial estipulada pelo BACEN (que anualizada oscilou historicamente entre 3,00% e 4,50%, equivalente a taxas mensais de 0,25% a 0,50% a.m.);
   - **`Alta / Acima da Meta`** ($IPCA > 0{,}50\%$): evidenciando pressões desmedidas sobre a capacidade produtiva e desancoragem das expectativas de mercado.

---

### 3.3.2 Tabela de Distribuição de Frequência e Métricas Descritivas

A distribuição conjunta da série histórica atualizada (março de 2012 a agosto de 2026, totalizando $N = 174$ observações mensais contínuas) revela a predominância do regime compatível com a meta estipulada pelas autoridades monetárias, conforme sumarizado na Tabela 1.

#### Tabela 1 – Distribuição de Frequência do Atributo Nominal (Regime de Inflação)

| Classe Nominal (Regime) | Faixa Paramétrica | Frequência Absoluta ($f_i$) | Frequência Relativa ($f_r\%$) | Frequência Acumulada ($F_i$) | Freq. Rel. Acumulada ($F_r\%$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Deflação** | $IPCA < 0{,}00\%$ | 27 | 15,52% | 27 | 15,52% |
| **Meta / Estável** | $0{,}00\% \le IPCA \le 0{,}50\%$ | 77 | 44,25% | 104 | 59,77% |
| **Alta / Acima da Meta** | $IPCA > 0{,}50\%$ | 70 | 40,23% | 174 | 100,00% |
| **Total Geral Amostral** | **Horizonte 2012–2026** | **174** | **100,00%** | **174** | **100,00%** |

*Fonte: Elaboração própria com base em microdados do SGS/BACEN (2026).*

Complementarmente, os estimadores estatísticos univariados da variável contínua `IPCA` apontam:
- **Tamanho Amostral ($N$):** 174 meses;
- **Média Aritmética ($\mu$):** 0,4324% a.m.;
- **Mediana ($Md$):** 0,4150% a.m.;
- **Desvio Padrão ($\sigma$):** 0,4719% a.m. (Variância amostral: 0,2226);
- **Coeficiente de Assimetria (*Skewness*):** +0,5287 (assimetria moderada à direita);
- **Coeficiente de Curtose (*Kurtosis*):** +0,3736 (fracamente leptocúrtica);
- **Valores Extremos:** Mínimo histórico de -0,7400% (junho/2023) e Máximo histórico de 1,9500% (dezembro/2019);
- **Quartis:** $Q_1 = 0{,}0800\%$, $Q_3 = 0{,}6775\%$, Intervalo Interquartílico $IQR = 0{,}5975\%$;
- **Limites de Tukey ($1{,}5 \times IQR$):** $[-0{,}8163\%; +1{,}5737\%]$, totalizando 5 *outliers* na cauda superior.

---

### 3.3.3 Análise Visual: Histograma, Boxplot e Gráfico de Dispersão

Para examinar visualmente as propriedades morfológicas do IPCA, gerou-se o conjunto gráfico padrão em alta resolução composto por histograma com curva de densidade contínua (KDE), diagramas de caixa (*boxplots*) univariados e segmentados, e dispersão bivariada relacionando o IPCA ao vetor de *pass-through* cambial (`USDBRL`).

#### 1. Histograma e Densidade Empírica (KDE)
Conforme demonstrado na Figura 1, a distribuição empírica do IPCA apresenta média de 0,4324% e mediana de 0,4150%. A proximidade entre os estimadores de tendência central aliada ao coeficiente de assimetria positivo (+0,5287) comprova a presença de assimetria moderada à direita: a grande maioria dos meses concentra-se em oscilações controladas, mas ocorrem choques inflacionários pontuais de magnitude acentuada. O coeficiente de curtose de 0,3736 indica uma distribuição com cauda ligeiramente mais pesada que a distribuição normal de referência.

#### 2. Diagrama de Caixa (Boxplot)
A inspeção do boxplot univariado na Figura 2(A) pelo critério interquartílico de Tukey ($IQR = 0{,}5975$ p.p.) detecta formalmente 5 observações categorizadas como *outliers* estatísticos: dezembro/2019 (1,95%, choque na pecuária bovina), outubro/2020 (1,72%), novembro/2020 (1,61%), dezembro/2020 (1,58%) e dezembro/2021 (1,58%), reflexos da desorganização das cadeias globais pós-confinamento pandêmico. Na Figura 2(B), o boxplot estratificado demonstra que a variabilidade interna do regime de 'Alta' é consideravelmente maior do que no regime de 'Meta', reforçando a necessidade dos modelos preditivos híbridos (ARIMAX + Random Forest) implementados na pesquisa para absorver tais não linearidades.

#### 3. Gráfico de Dispersão (IPCA versus Câmbio USDBRL)
O gráfico de dispersão da Figura 3 investiga o mecanismo de transmissão cambial (*pass-through*). Observa-se inclinação positiva na reta de tendência média, indicando que depreciações cambiais da moeda nacional (elevação do câmbio R$/US$) exercem pressão altista sobre a inflação ao consumidor via encarecimento de insumos e matérias-primas importadas. A discriminação por cores confirma a separação nítida dos clusters entre os regimes nominais de inflação ao longo do espaço bidimensional.

#### 4. Distribuição de Frequências das Classes
A Figura 4 ilustra graficamente a proporção de cada classe na amostra: o regime de estabilidade e convergência ('Meta / Estável') abrange 44,25% da série (77 meses), seguido pelo regime de aceleração ('Alta / Acima da Meta') com 40,23% (70 meses). Já os episódios deflacionários representam 15,52% do histórico (27 meses), concentrados em contrações agudas de demanda e nas desonerações fiscais temporárias sobre eletricidade e combustíveis aprovadas em meados de 2022.

---

### 3.3.4 Governança, Integridade Amostral e Requisitos de Qualidade

A consolidação deste ecossistema analítico adota conformidade irrestrita com a Lei Geral de Proteção de Dados Pessoais (LGPD – Lei nº 13.709/2018) e com as diretrizes federais de dados abertos governamentais, visto que todas as séries temporais utilizadas constituem indicadores públicos agregados do SGS/BACEN, IBGE, FGV e Ministério do Trabalho e Emprego, isentos de sigilo fiscal ou identificadores individuais. Sob o rigor da engenharia de qualidade de dados, assegura-se:
1. **Prevenção de viés prospectivo (*lookahead bias*):** calibração de imputadores e normalizadores estritamente no conjunto temporal passado;
2. **Congelamento histórico de séries:** fotografia consolidada que previne quebras por revisões retroativas das fontes estatísticas;
3. **Completude amostral integral:** 100% de preenchimento nas 174 observações mensais contínuas (2012 a 2026);
4. **Reprodutibilidade científica e algorítmica:** pipeline 100% codificado em Python com chamadas diretas às APIs públicas oficiais.
