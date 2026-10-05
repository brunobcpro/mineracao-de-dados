<div align="center">

<p align="center">
  <img src="Logos/logo_upe.png" height="90" alt="Logo UPE" />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="Logos/logo_poli.png" height="70" alt="Logo POLI" />
</p>

# UNIVERSIDADE DE PERNAMBUCO
## ESCOLA POLITÉCNICA DE PERNAMBUCO - POLI
### CAMPUS RECIFE
### CURSO DE ENGENHARIA DA COMPUTAÇÃO
### DISCIPLINA: MINERAÇÃO DE DADOS
### PROFESSOR: PROF. DR. ALEXANDRE MACIEL

<br><br>

### AUTORES:
**BRUNO PROTÁSIO**  
**DANIEL MENESES**  
**MARCUS VINICIUS**  
**VINICYUS EMANUEL**  

<br><br><br>

# MINERAÇÃO DE SÉRIES TEMPORAIS PARA PREVISÃO DA INFLAÇÃO:
## ARQUITETURA HÍBRIDA MULTIVARIADA E OTIMIZAÇÃO BIOINSPIRADA DE ATRIBUTOS

<br><br><br><br>

### RECIFE
### 2026

</div>

---

## 1 INTRODUÇÃO

A trajetória dos preços em uma economia em desenvolvimento como a brasileira é marcada por uma tensão permanente entre a memória do passado e os choques imprevisíveis do presente. Ao longo de décadas, a sociedade conviveu com oscilações inflacionárias que desgastam a renda do trabalho, tornam o crédito escasso e impõem pesadas incertezas sobre o planejamento das famílias e das empresas. A consolidação da estabilidade monetária com a criação do Plano Real e a posterior adoção do regime de metas para a inflação estabeleceram um pacto institucional: manter o poder de compra da moeda através do monitoramento rigoroso do Índice Nacional de Preços ao Consumidor Amplo (IPCA), calculado mensalmente pelo Instituto Brasileiro de Geografia e Estatística (IBGE).

Contudo, conduzir e antecipar essa dinâmica é uma tarefa desafiadora. O Banco Central do Brasil utiliza a taxa básica de juros (Selic) como seu principal instrumento de controle, mas as decisões de política monetária demandam entre dois e quatro trimestres para produzir efeitos plenos sobre o consumo e os investimentos. Essa defasagem temporal impede que gestores públicos e privados naveguem olhando apenas para os preços observados ontem; torna-se imperativo antecipar o comportamento futuro do índice para embasar decisões tempestivas.

Historicamente, a literatura estatística abordou a previsão de preços sob a ótica univariada, partindo da premissa de que o próprio histórico de inflação sintetiza a inércia dos contratos e as expectativas dos agentes. Modelos clássicos de séries temporais assumem que as defasagens passadas e os ciclos sazonais são suficientes para projetar os próximos períodos. Entretanto, a economia brasileira é exposta a perturbações exógenas frequentes: choques cambiais que encarecem insumos importados, oscilações severas nas cotações internacionais de commodities energéticas, secas que penalizam a produção agrícola e desequilíbrios no mercado de trabalho.

Surge, assim, um dilema central de modelagem: modelos estritamente univariados correm o risco de ignorar sinais antecipados cruciais emitidos por variáveis externas, enquanto abordagens multivariadas que incorporam dezenas de indicadores econômicos enfrentam o risco de ruído amostral, multicolinearidade e superajuste (*overfitting*). O presente projeto investiga essa fronteira empírica sob a ótica da Engenharia da Computação e da Mineração de Dados. A presente entrega foca na formulação do problema, na integração interdisciplinar com economistas e no pipeline completo de coleta, análise exploratória descritiva e pré-processamento de um robusto painel macroeconômico, preparando a base para a futura calibração de modelos preditivos e algoritmos bioinspirados de seleção de atributos.

### 1.1 Contextualização
A dinâmica da inflação no Brasil conecta-se diretamente à arquitetura do Sistema Financeiro Nacional. O Conselho Monetário Nacional (CMN) define as metas anuais de inflação, cabendo ao Banco Central do Brasil (BACEN) calibrar as condições financeiras para o seu cumprimento. 

Para a ciência e engenharia de dados, esse cenário desdobra-se em três pilares de relevância aplicada:
- **Setor Público e Governança Macroeconômica:** O fornecimento de estimativas acuradas mitiga assimetrias informacionais, permitindo avaliar pressões de custos antes que se disseminem pela economia e auxiliando na ancoragem das expectativas de mercado;
- **Mercado Financeiro e Atividade Corporativa:** Empresas utilizam projeções de inflação para reajustar contratos de fornecimento de longo prazo, planejar orçamentos de capital e gerenciar estoques. No mercado financeiro, a correta precificação de títulos indexados à inflação (como NTN-B e debêntures) e a gestão de risco de tesouraria dependem da acurácia dessas projeções;
- **Pesquisa em Engenharia e Mineração de Dados:** Séries macroeconômicas de economias emergentes oferecem um ambiente de estresse para algoritmos computacionais, demandando engenharia de dados precisa para sincronizar bases heterogêneas, sanear dados ruidosos e evitar vazamento temporal.

### 1.2 Descrição do Problema
O desafio central consiste em arbitrar entre a inércia temporal e a sensibilidade a choques macroeconômicos externos:
1. **A Hipótese Univariada:** Postula que a inércia inflacionária — sustentada por indexação contratual e rigidez de preços — domina a trajetória da série, de modo que modelos autorregressivos simples superariam formulações complexas que demandam estimativas de terceiros;
2. **A Hipótese Multivariada:** Postula que indicadores antecedentes de preços no atacado, custos de transporte, cotação do dólar e nível de atividade agregada emitem sinais preditivos antecipados que o histórico isolado do índice de inflação é incapaz de capturar a tempo.

A questão metodológica reside em determinar se a complexidade multivariada compensa o risco de instabilidade estatística e quais classes de variáveis econômicas trazem ganho preditivo mensurável.

> **Pergunta Central de Pesquisa:** *"A utilização de variáveis macroeconômicas exógenas melhora a acurácia preditiva da inflação frente a modelos puramente univariados? Quais atributos possuem maior capacidade de antecipar a trajetória da inflação brasileira?"*

### 1.3 Objetivos

#### 1.3.1 Objetivo Geral da Etapa Atual
Desenvolver o processo de mineração de dados focado na formulação do problema, fundamentação teórica, análise exploratória descritiva e pré-processamento integral de séries temporais da inflação brasileira e variáveis exógenas antecedentes, estruturando uma base de dados higienizada, consistente e documentada sob orientação de especialistas para fundamentar a futura calibração de modelos preditivos multivariados.

#### 1.3.2 Objetivos Específicos do Escopo Atual
1. **Engenharia e Coleta de Dados Macroeconômicos:** Coletar e consolidar a série histórica mensal do IPCA e de 28 variáveis exógenas candidatas de março de 2012 a agosto de 2026 via API oficial do SGS/Banco Central;
2. **Mapeamento de Stakeholders e Orientação Acadêmica:** Mapear os envolvidos no projeto, articulando a orientação acadêmica do Prof. Dr. Alexandre Maciel (POLI/UPE) e a consultoria de domínio macroeconômico do Prof. Guilherme Martins (FCAP/UPE);
3. **Fundamentação Teórica e Diferenciais Metodológicos:** Estruturar a revisão da literatura e estabelecer a matriz comparativa de diferenciais frente aos modelos clássicos e recentes;
4. **Caracterização Estatística e Visual dos Dados:** Conduzir análise descritiva univariada e bivariada dos atributos contínuos e discretos, explorando assimetrias, outliers e comportamento sob diferentes regimes nominais de inflação;
5. **Pipeline de Pré-processamento e Saneamento:** Implementar rotinas sistemáticas de limpeza de nulos, alinhamento temporal em frequência uniforme (Month-Start), tratamento de inconsistências, redução amostral e codificação de atributos;
6. **Estruturação do Dicionário de Dados da Base Consolidada:** Documentar formalmente todos os 31 atributos consolidados, seus códigos de origem, tipagem, procedimentos de pré-processamento e relevância de negócio.

### 1.4 Justificativa
Projeções de inflação influenciam a taxa de juros real da economia, os custos de captação de dívida soberana e a formação de preços no atacado e no varejo. Séries econômicas brasileiras apresentam não linearidades, quebras de regime e forte exposição a choques internacionais. Sob a perspectiva da computação aplicada, a pesquisa contribui ao estabelecer um pipeline reprodutível de engenharia de dados que transforma séries públicas brutas em um painel estruturado, alinhado e auditável, eliminando vieses e viabilizando a futura aplicação de estimadores preditivos avançados.

### 1.5 Escopo Negativo e Delimitação da Etapa
Para assegurar clareza quanto à entrega atual do projeto, definem-se os seguintes limites de escopo:
- **Análise de Estacionariedade e Modelagem Preditiva nesta Fase:** A realização de testes de raiz unitária (ADF), transformações de diferenciação para modelos específicos, calibração de algoritmos preditivos (ARIMA, ARIMAX, Random Forest, Lasso, Arquitetura Híbrida) e otimização bioinspirada (GA e PSO) pertencem à etapa subsequente do projeto, não fazendo parte do escopo da presente entrega, que encerra-se formalmente no pré-processamento dos dados;
- **Alta Frequência e Intradiário:** O estudo concentra-se na frequência mensal oficial e não aborda cotações diárias ou intradiárias de preços;
- **Nível Microeconômico:** Não são investigadas cestas de consumo de indivíduos específicos, recortes regionais isolados ou desagregações domiciliares da POF;
- **Prescrição de Política Econômica:** O trabalho tem finalidade analítica e de engenharia de dados, sem emitir recomendações normativas sobre o patamar adequado de juros ou diretrizes fiscais.

---

## 2 FUNDAMENTAÇÃO TEÓRICA

### 2.1 Área do Negócio: O Funcionamento da Inflação e a Dinâmica Econômica
Para compreender o desafio de antecipar a inflação, é necessário desmistificar o fenômeno em linguagem acessível a leitores de diferentes áreas e fundamentada na literatura macroeconômica.

#### O que é a Inflação na Prática?
De forma intuitiva, a inflação não é apenas o encarecimento de um produto específico, como o tomate ou a energia elétrica; ela representa o aumento contínuo e generalizado no nível de preços de bens e serviços de uma economia ao longo do tempo [4, 13]. O efeito prático mais imediato é a perda do poder de compra da moeda: se uma nota de R$ 100 permitia comprar um conjunto completo de mantimentos no início do ano e, meses depois, adquire apenas uma fração desses mesmos produtos, a moeda perdeu valor relativo [13].

#### Como o IPCA Mede Essa Realidade?
No Brasil, a inflação oficial é mensurada pelo Índice Nacional de Preços ao Consumidor Amplo (IPCA), calculado pelo IBGE desde 1979 e adotado formalmente como bússola do sistema de metas [10]. Para mensurá-lo, o IBGE não calcula uma média simples de preços: constrói-se uma "cesta média de consumo" ponderada, que reflete como as famílias com renda entre 1 e 40 salários mínimos distribuem seus gastos [10]. Despesas com alimentação, habitação e transporte possuem peso predominante no orçamento das famílias brasileiras; portanto, variações nesses grupos provocam impactos assimétricos sobre o índice geral.

#### Os Três Grandes Motores da Inflação Brasileira
A literatura econômica contemporânea e a experiência empírica brasileira identificam três forças fundamentais que movimentam os preços:
1. **A Inércia e a Memória da Moeda:** O Brasil atravessou décadas de inflação crônica antes do Plano Real, o que consolidou mecanismos formais e informais de "indexação" [5, 16]. Na prática, diversos preços da economia — como aluguéis residenciais, tarifas públicas, pedágios, mensalidades escolares e convenções coletivas de trabalho — são reajustados periodicamente pela inflação passada. Isso gera um comportamento de persistência ou "memória temporal": a inflação de hoje carrega em si a taxa observada no passado, perpetuando o ciclo mesmo na ausência de novos choques [5, 16];
2. **Choques de Oferta e Custos (Câmbio e Commodities):** Quando ocorrem perturbações externas, como a alta internacional do petróleo ou a desvalorização cambial do Real frente ao Dólar americano, os insumos de importação tornam-se imediatamente mais onerosos [3, 6]. O aumento nos preços dos combustíveis eleva o custo do frete rodoviário, que encarece a distribuição de alimentos e bens de consumo, produzindo o mecanismo clássico de repasse cambial (*pass-through*) para o consumidor final [6];
3. **Pressões de Demanda e o Hiato do Produto:** Quando a atividade econômica se expande aceleradamente, impulsionando a contratação de trabalhadores e o aumento da renda agregada acima da capacidade física das fábricas e prestadores de serviço de ofertar bens, surge escassez relativa [4, 17]. Os produtores ajustam os preços para cima para equilibrar o mercado, relação descrita classicamente pelo mecanismo da Curva de Phillips [4, 17].

#### O Banco Central e o 'Termostato' da Política Monetária
Para evitar desarranjos na estabilidade de preços, o Conselho Monetário Nacional (CMN) define uma meta percentual anual. O Banco Central atua como regulador do sistema por meio do Comitê de Política Monetária (COPOM), utilizando a taxa básica de juros (Selic) como instrumento regulador [3, 17].

A taxa Selic funciona de maneira análoga a um termostato econômico:
- **Elevação da Taxa Selic:** Quando a inflação ameaça ultrapassar o teto da meta, o Banco Central eleva a taxa Selic. O crédito fica mais caro, o custo de oportunidade de poupar aumenta, as empresas adiam investimentos e as famílias reduzem o consumo financiado. Essa desaceleração da demanda arrefece a alta dos preços [3, 13];
- **Redução da Taxa Selic:** Por outro lado, se a economia se retrai e a inflação converge para níveis muito baixos, o BACEN pode reduzir a taxa Selic para reativar a atividade produtiva.

O ponto crítico desse processo é a existência de defasagens temporais de transmissão (*transmission lags*): uma decisão tomada pelo COPOM hoje leva entre 6 e 12 meses para se propagar pelos canais de crédito, câmbio e expectativas até afetar os preços finais [3, 17]. Por esse motivo, as autoridades monetárias e os analistas de mercado dependem de modelos preditivos tempestivos, capazes de antecipar a trajetória da inflação no horizonte relevante.

### 2.2 Mineração de Dados
*(Nota: O detalhamento conceitual e matemático dos algoritmos computacionais de aprendizado de máquina, redes neurais e operadores genéticos será incorporado nesta subseção na etapa subsequente do projeto, permanecendo este tópico reservado para a fundamentação algorítmica específica).*

### 2.3 Trabalhos Relacionados e Análise de Diferenciais
A literatura sobre modelagem da inflação organiza-se em três paradigmas metodológicos principais:
1. **Modelagem Paramétrica Box-Jenkins:** A abordagem clássica de séries temporais de Box e Jenkins [1] consolidou o uso de processos autorregressivos integrados de médias móveis (ARIMA). Tais formulações capturam adequadamente a inércia estocástica e a sazonalidade, mas partem de hipóteses rígidas de linearidade e não respondem com tempestividade a choques de oferta exógenos [1, 9];
2. **Arquiteturas Híbridas Lineares e Não Lineares:** Zhang [18] introduziu a formulação híbrida canônica que decompõe uma série temporal na soma de uma componente linear com uma componente residual não linear ($y_t = L_t + N_t$). Ao aplicar redes neurais aos resíduos do ARIMA, Zhang demonstrou que a modelagem conjunta supera estimadores isolados. Contudo, suas aplicações originais concentraram-se em séries univariadas sem covariáveis macroeconômicas exógenas [18];
3. **Machine Learning Multivariado de Alta Dimensionalidade:** Estudos contemporâneos de econometria aplicada, como Garcia et al. [6] e Medeiros et al. [14], avaliaram o emprego de métodos de regularização (como Lasso e Elastic Net) e algoritmos ensemble (Random Forest) alimentados por grandes painéis de dados econômicos. Embora demonstrem que dados externos contêm sinal preditivo, tais estudos frequentemente enfrentam o custo da multicolinearidade e da perda de aderência quando não há uma modelagem prévia da inércia autoregressiva estrutural [6, 14].

Para evidenciar com precisão como o presente projeto se insere nessa fronteira e quais lacunas metodológicas preenche, a Tabela 1 sintetiza uma análise comparativa baseada em critérios funcionais e computacionais, confrontando os trabalhos da literatura com a abordagem proposta para o projeto.

#### Tabela 1 – Matriz Comparativa de Trabalhos Relacionados e Diferenciais Metodológicos do Projeto
| Dimensão Metodológica / Requisito | Modelos Clássicos (Box & Jenkins, 2015) [1] | Híbridos Tradicionais (Zhang, 2003) [18] | Machine Learning Multivariado (Medeiros et al., 2021) [14] | Abordagem Proposta (ARIMAX Híbrido + Meta-heurísticas) |
| :--- | :--- | :--- | :--- | :--- |
| **Estrutura de Modelagem** | Linear univariada estrita (ARIMA / SARIMA). | Híbrida aditiva univariada (ARIMA linear + RNA nos resíduos). | Regressores puramente não lineares ou regularizados (Lasso, RF). | Híbrida aditiva multivariada (ARIMAX com exógenas + RF nos resíduos). |
| **Espaço de Variáveis Exógenas** | Ausente (apenas o histórico passado da própria série $y_t$). | Ausente (opera unicamente com defasagens da série dependente). | Amplo painel multivariado sem filtragem otimizada de atributos. | 28 covariáveis estruturadas em 4 pilares macroeconômicos fundamentais. |
| **Seleção Inteligente de Atributos** | Inexistente (seleção via critérios AIC/BIC em ordens $p, d, q$). | Inexistente (foco apenas no ajuste de resíduos temporais). | Penalização paramétrica passiva ($L_1$/Lasso) ou importância em árvores. | Meta-heurísticas bioinspiradas ativas (Algoritmo Genético e PSO) para seleção global. |
| **Tratamento de Choques Não Lineares** | Incapaz de modelar quebras estruturais ou choques de custos exógenos. | Modela não linearidades endógenas, mas cego a choques externos (câmbio/petróleo). | Captura interações não lineares, mas negligencia a inércia autoregressiva pura. | ARIMAX ancora a inércia estocástica e a Random Forest absorve os choques exógenos residuais. |
| **Prevenção de Vazamento (*Data Leakage*)** | Divisão amostral simples ou estimação em toda a amostra. | Divisão estática simples de treino e teste. | Frequentemente adota validação cruzada $k$-fold sem preservação estrita da ordem temporal. | Validação sequencial dinâmica *Walk-Forward* de 1 passo ($h=1$) com reestimação cronológica. |
| **Contextualização Econômica Aplicada** | Foco estatístico genérico em séries sintéticas ou industriais. | Aplicações empíricas clássicas em séries padronizadas internacionais. | Avaliação em mercados desenvolvidos com baixa volatilidade e sem indexação. | Painel brasileiro contemporâneo (2012–2026, 174 meses), com validação de economista da FCAP/UPE. |

*Fonte: Elaboração própria com base na revisão sistemática da literatura (2026).*

---

## 3 MATERIAIS E MÉTODOS

### 3.1 Stakeholders Envolvidos
A condução e a validação do projeto contam com a participação e o direcionamento de diferentes partes interessadas (*stakeholders*), articulando a liderança acadêmica na disciplina, a consultoria de domínio macroeconômico e a aplicabilidade prática:

1. **Professor da Disciplina e Orientador Metodológico:**
   - **Prof. Dr. Alexandre Maciel (Escola Politécnica de Pernambuco – POLI/UPE):** Docente responsável pela disciplina de Mineração de Dados no curso de Engenharia da Computação. Atua como o principal stakeholder acadêmico e orientador metodológico do projeto, tendo como responsabilidades:
     - Orientar e avaliar a conformidade técnica do projeto com os preceitos científicos de Descoberta de Conhecimento em Bases de Dados (KDD) e Mineração de Dados;
     - Avaliar o rigor do pipeline de engenharia de dados, garantindo reprodutibilidade e prevenção de vazamento temporal (*lookahead bias*);
     - Validar as decisões de saneamento, tratamento de dados ausentes e estruturação formal do Dicionário de Dados;
     - Avaliar a aderência do artigo aos padrões institucionais e critérios de avaliação da POLI-UPE.

2. **Stakeholder Especialista de Domínio (Consultoria Macroeconômica):**
   - **Prof. Guilherme Martins (Faculdade de Ciências da Administração de Pernambuco – FCAP/UPE):** Economista e docente da UPE, atuando como o consultor especialista de domínio do projeto. Sua responsabilidade e interesse residem em:
     - Validar a pertinência teórica das 28 variáveis exógenas candidatas à luz da teoria macroeconômica e das peculiaridades do mercado brasileiro;
     - Orientar sobre a dinâmica dos mecanismos de transmissão de preços (*pass-through* cambial, inércia de contratos e tarifas públicas reguladas);
     - Assegurar que os procedimentos de pré-processamento preservem a integridade e o significado econômico das séries históricas;
     - Avaliar a consistência das conclusões exploratórias frente à política monetária conduzida pelo BACEN e pelo COPOM.

3. **Stakeholders de Aplicação e Beneficiários Finais (Decisores Econômicos):**
   - **Analistas de Mercado Financeiro e Gestores de Ativos:** Interessados em dados macroeconômicos saneados e consistentes para precificação de títulos públicos indexados (como NTN-B e debêntures incentivadas) e gestão de riscos de carteira;
   - **Departamentos de Planejamento e Controladorias Corporativas:** Necessidade de parâmetros preditivos confiáveis de custos para elaboração de orçamentos anuais, reajustes contratuais com fornecedores e planejamento de estoques;
   - **Sociedade e Gestores de Políticas Públicas:** Beneficiários indiretos de estudos transparentes e reprodutíveis que analisam as pressões de custos sobre itens de consumo essencial (alimentação, energia e transporte).

### 3.2 Descrição da Base de Dados
A base empírica foi coletada automaticamente da API do Sistema Gerenciador de Séries Temporais do Banco Central (SGS/BACEN). O painel compreende 174 observações mensais contínuas (frequência *Month Start* - MS), de março de 2012 a agosto de 2026.

A variável dependente alvo ($y_t$) é o IPCA mensal (SGS código 4447). As 28 variáveis exógenas candidatas foram agrupadas em quatro categorias macroeconômicas:
- **Índices de Preços e Desagregações Setoriais (11 variáveis):** Subíndices do IPCA (Alimentação, Transportes, Habitação, Saúde, Vestuário, Educação e Despesas Pessoais) e índices gerais (INPC, IGP-M, IGP-DI e IPC-BR);
- **Setor Financeiro, Moeda e Câmbio (3 variáveis):** Taxa Selic Over, taxa de câmbio nominal PTAX (USDBRL) e reservas internacionais;
- **Atividade Econômica e Mercado de Trabalho (7 variáveis):** PIB Mensal a preços correntes, taxa de desocupação (PNAD Contínua), salário mínimo nacional, estoques de empregos formais ativos do CAGED (Total, Agropecuária e Construção Civil) e produção física de ovos;
- **Energia e Combustíveis (6 variáveis):** Refino de petróleo, consumo aparente de gasolina automotiva, consumo de óleo combustível e demanda faturada de energia elétrica (Comercial, Residencial e Total).

#### 3.2.1 Delimitação Temporal e Justificativa Metodológica (2012 a 2026)
O marco temporal inicial em março de 2012 foi adotado devido a três fatores metodológicos fundamentados com o stakeholder economista:
1. **Transição da Medição do Desemprego:** Implantação da PNAD Contínua pelo IBGE em substituição à antiga PME, eliminando quebra estrutural severa nos dados de mercado de trabalho;
2. **Nova Ponderação da Cesta do IPCA:** Atualização dos pesos da cesta de consumo com base na POF 2008-2009;
3. **Painel Balanceado no SGS/BACEN:** Disponibilidade ininterrupta do painel balanceado de séries setoriais.

### 3.3 Análise Descritiva dos Dados
A análise descritiva investigou a dispersão, a assimetria e os valores extremos antes da modelagem preditiva. Para atender aos critérios formais de mineração de dados, foram caracterizados um atributo numérico contínuo e um atributo nominal institucionalmente fundamentado:
1. **Atributo Numérico Contínuo (`IPCA`):** Variação percentual mensal da inflação oficial (SGS 4447);
2. **Atributo Nominal Categórico (`Regime de Inflação`):** Discretização da série contínua em três classes balizadas pelas metas do CMN: Deflação ($IPCA < 0{,}00\%$), Meta / Estável ($0{,}00\% \le IPCA \le 0{,}50\%$) e Alta / Acima da Meta ($IPCA > 0{,}50\%$).

#### 3.3.1 Distribuição de Frequências e Métricas Descritivas
A análise da amostra atualizada (174 meses contínuos) aponta a predominância de meses dentro da meta oficial, conforme demonstrado na Tabela 2.

#### Tabela 2 – Distribuição de Frequência do Atributo Nominal (Regime de Inflação)
| Classe Nominal | Faixa Paramétrica | Freq. Absoluta ($f_i$) | Freq. Relativa (%) | Freq. Acumulada ($F_i$) | Freq. Rel. Acum. (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Deflação** | $IPCA < 0{,}00\%$ | 27 | 15,52% | 27 | 15,52% |
| **Meta / Estável** | $0{,}00\% \le IPCA \le 0{,}50\%$ | 77 | 44,25% | 104 | 59,77% |
| **Alta / Acima da Meta** | $IPCA > 0{,}50\%$ | 70 | 40,23% | 174 | 100,00% |
| **Total Geral Amostral** | **Horizonte 2012–2026** | **174** | **100,00%** | **174** | **100,00%** |

*Fonte: Elaboração própria com base no SGS/BACEN (2026).*

Principais estimadores estatísticos do IPCA contínuo na amostra:
- **Média e Mediana:** Média de 0,4324% ao mês e mediana de 0,4150% ao mês;
- **Dispersão:** Desvio padrão amostral de 0,4719% e variância de 0,2226;
- **Assimetria e Curtose:** Assimetria positiva (+0,5287), acusando cauda direita alongada por choques inflacionários, e curtose de +0,3736;
- **Valores Extremos:** Mínimo histórico de -0,7400% (junho/2023) e máximo de +1,9500% (dezembro/2019);
- **Quartis e Intervalo Interquartílico:** $Q_1 = 0{,}0800\%$, $Q_3 = 0{,}6775\%$ e $IQR = 0{,}5975$ p.p.

#### 3.3.2 Análise Visual: Histograma, Boxplot e Gráfico de Dispersão
A caracterização visual dos dados foi conduzida através de gráficos gerados a partir do histórico consolidado:
- **Figura 1 (Histograma e Densidade Empírica KDE):** Concentração predominante de taxas mensais entre 0,10% e 0,60%, confirmando regularidade central e assimetria à direita;
- **Figura 2 (Boxplots):** Pelo critério de Tukey ($1{,}5 \times IQR$), detectam-se 5 observações discrepantes extremas: dezembro/2019 (+1,95%), outubro/2020 (+1,72%), novembro/2020 (+1,61%), dezembro/2020 (+1,58%) e dezembro/2021 (+1,58%), decorrentes de choques em carnes e restrições de cadeias de suprimentos globais. A dispersão na classe "Alta" é muito mais ampla do que na classe "Meta", justificando a modelagem não linear dos resíduos;
- **Figura 3 (Dispersão Câmbio vs. IPCA):** Demonstra a correlação positiva entre a cotação do dólar (USDBRL) e a probabilidade de ocorrência do regime "Alta", ilustrando o mecanismo de repasse cambial (*pass-through*);
- **Figura 4 (Distribuição de Regimes):** 44,25% das ocorrências situam-se na Meta, 40,23% em Alta e 15,52% em Deflação.

#### 3.3.3 Governança, Integridade e Requisitos de Qualidade
O tratamento dos dados segue rigorosamente a Lei Geral de Proteção de Dados Pessoais (LGPD – Lei nº 13.709/2018). As séries temporais empregadas são dados macroeconômicos públicos e agregados (SGS/BACEN, IBGE, FGV e Ministério do Trabalho), sem identificadores individuais. Sob a perspectiva de engenharia de dados, garantimos: (i) prevenção estrita de vazamento prospectivo (*lookahead bias*); (ii) completude amostral de 100% sem lacunas no período de 2012 a 2026; e (iii) reprodutibilidade científica por meio de scripts Python automatizados.

### 3.4 Pré-processamento dos Dados
O pré-processamento de dados constitui a etapa culminante da presente entrega. Nesta fase, as séries temporais brutas foram submetidas a rotinas sistemáticas de engenharia de dados para transformá-las em um painel estruturado, consistente e livre de inconsistências, sem qualquer vazamento de dados futuros.

#### 3.4.1 Procedimentos de Limpeza e Saneamento de Dados (Data Cleaning)
O pipeline de limpeza executado compreendeu quatro procedimentos principais:
1. **Sincronização Cronológica:** Séries divulgadas em periodicidade diária no mercado financeiro (taxa de câmbio nominal PTAX e taxa Selic Over) foram convertidas para médias mensais de dias úteis e sincronizadas sob frequência contínua *Month Start* (MS) de março de 2012 a agosto de 2026;
2. **Tratamento de Zeros Estruturais:** Em séries contínuas de fluxos e estoques físicos (refino de petróleo, consumo de combustíveis, demanda de energia e estoques de emprego do CAGED), zeros espúrios gerados por atrasos de apuração de órgãos governamentais foram identificados e substituídos por valores nulos (`NaN`);
3. **Sanitização Numérica:** Verificação sistemática contra potenciais valores infinitos ($\pm\infty$) ou divisões por zero, assegurando que todas as entradas pertencem ao espaço numérico real Float64;
4. **Imputação Temporal de Dados Ausentes:** Valores faltantes pontuais em séries mensais foram tratados via interpolação linear temporal contínua indexada pelo calendário (`interpolate(method='time')`). A preservação da ordem cronológica garante a integridade histórica dos dados sem distorções.

#### 3.4.2 Técnicas de Redução de Dados e Engenharia de Atributos
1. **Redução Amostral Estrutural (Truncamento pós-2012):** Conforme validado junto ao consultor de domínio, descartaram-se os dados anteriores a março de 2012 para eliminar quebras estruturais metodológicas severas (transição da PME para PNAD Contínua e revisão dos pesos da cesta do IPCA pela POF 2008-2009);
2. **Discretização do Atributo Nominal:** Construção da variável categórica "Regime de Inflação" com base nas faixas institucionais do CMN, permitindo a segmentação exploratória de períodos de normalidade, estresse e deflação;
3. **Codificação de Sazonalidade Harmônica:** Criação dos atributos sazonais $mes\_sin = \sin(2\pi m / 12)$ e $mes\_cos = \cos(2\pi m / 12)$, viabilizando a captura contínua e suave de ciclos anuais sem o custo de inflar a dimensionalidade com 11 variáveis dummy binárias.

#### 3.4.3 Dicionário de Dados da Base Consolidada Pré-Processada
Como resultado final de todo o fluxo de coleta, higienização e saneamento, a Tabela 3 consolida o Dicionário de Dados da base pré-processada, especificando para cada um dos 31 atributos o seu código de origem, tipo de dado, tratamento recebido no pré-processamento, pilar macroeconômico e papel de negócio validado pelo Prof. Guilherme Martins.

#### Tabela 3 – Dicionário de Dados da Base Consolidada Pré-Processada (174 Meses, 2012–2026)
| Atributo | Código / Fonte | Tipo / Unidade | Tratamento no Pré-processamento | Pilar Econômico | Papel / Descrição Econômica |
| :--- | :---: | :---: | :--- | :---: | :--- |
| **IPCA** | SGS 4447 (IBGE) | Float64 (% a.m.) | Interpolação de nulos; alinhamento Month-Start (MS) | Preços Setoriais | Variável dependente alvo (Target $y_t$) - Inflação oficial sob regime de metas. |
| **IPCA_Transportes** | SGS 1639 (IBGE) | Float64 (% a.m.) | Sincronização MS; tratamento de nulos via interpolação | Preços Setoriais | Covariável exógena - Choques de preços de combustíveis e tarifas de mobilidade. |
| **IPCA_Alimentação_bebidas** | SGS 1635 (IBGE) | Float64 (% a.m.) | Sincronização MS; tratamento de nulos via interpolação | Preços Setoriais | Covariável exógena - Choques climáticos e safras no consumo domiciliar. |
| **INPC_Habitação** | SGS 1636 (IBGE) | Float64 (% a.m.) | Sincronização MS; tratamento de nulos via interpolação | Preços Setoriais | Covariável exógena - Pressões de aluguel e tarifas de energia residencial. |
| **IPCA_Saúde_cuidados_pessoais** | SGS 1641 (IBGE) | Float64 (% a.m.) | Sincronização MS; tratamento de nulos via interpolação | Preços Setoriais | Covariável exógena - Repasse de custos médicos e planos de saúde regulados. |
| **IPCA_Vestuário** | SGS 1638 (IBGE) | Float64 (% a.m.) | Sincronização MS; tratamento de nulos via interpolação | Preços Setoriais | Covariável exógena - Sazonalidade de coleções e liquidações do varejo. |
| **IPCA_Educação** | SGS 1643 (IBGE) | Float64 (% a.m.) | Sincronização MS; tratamento de nulos via interpolação | Preços Setoriais | Covariável exógena - Reajustes concentrados em início de ano letivo. |
| **IPCA_Despesas_Pessoais** | SGS 1642 (IBGE) | Float64 (% a.m.) | Sincronização MS; tratamento de nulos via interpolação | Preços Setoriais | Covariável exógena - Sensibilidade de demanda de serviços recreativos e pessoais. |
| **USDBRL (Câmbio PTAX)** | SGS 3696 (BACEN) | Float64 (R$/US$) | Conversão diária para média mensal de dias úteis; MS | Câmbio / Finanças | Covariável exógena - Mecanismo de pass-through cambial e importações. |
| **SELIC** | SGS 4390 (BACEN) | Float64 (% a.m.) | Conversão de taxa diária para média mensal; MS | Câmbio / Finanças | Covariável exógena - Taxa básica de juros da política monetária do COPOM. |
| **Reservas_Internacionais** | SGS 3546 (BACEN) | Float64 (US$ Milhões) | Alinhamento mensal MS; saneamento de lacunas | Câmbio / Finanças | Covariável exógena - Liquidez externa e blindagem a choques globais. |
| **INPC** | SGS 188 (IBGE) | Float64 (% a.m.) | Sincronização MS; interpolação linear de nulos | Preços Setoriais | Covariável exógena - Inflação incidente em famílias de 1 a 5 salários mínimos. |
| **IGP_M** | SGS 189 (FGV) | Float64 (% a.m.) | Sincronização MS; alinhamento de competência | Preços Setoriais | Covariável exógena - Indicador antecedente de custos no atacado (FGV). |
| **IGP_DI** | SGS 190 (FGV) | Float64 (% a.m.) | Sincronização MS; verificação de integridade | Preços Setoriais | Covariável exógena - Preços ao produtor e insumos de disponibilidade interna. |
| **IPC_BR** | SGS 191 (FGV) | Float64 (% a.m.) | Sincronização MS; saneamento de inconsistências | Preços Setoriais | Covariável exógena - Índice de preços ao consumidor abrangente da FGV. |
| **PIB_Mensal** | SGS 4380 (BACEN) | Float64 (R$ Milhões) | Tratamento de atrasos de divulgação; sincronização MS | Atividade Econômica | Covariável exógena - Proxy de nível de atividade econômica mensal e hiato. |
| **Desemprego (PNAD)** | SGS 24369 (IBGE) | Float64 (% da PEA) | Truncamento pós-2012; interpolação de quebras | Mercado de Trabalho | Covariável exógena - Dinâmica da desocupação formal (Curva de Phillips). |
| **Salario_Minimo** | SGS 1619 (Governo) | Float64 (R$ correntes) | Sincronização MS; preservação de reajustes federais anuais | Mercado de Trabalho | Covariável exógena - Custos de contratação básica no setor terciário. |
| **Estoque_Empregos_Total** | SGS 28763 (CAGED) | Float64 (Mil vínculos) | Zeros contábeis substituídos por NaN; interpolação | Mercado de Trabalho | Covariável exógena - Saldo mensal de geração de emprego formal no Brasil. |
| **Estoque_Agropecuária** | SGS 28764 (CAGED) | Float64 (Mil vínculos) | Substituição de zeros por NaN; sincronização contínua | Mercado de Trabalho | Covariável exógena - Dinâmica do emprego rural e safras do agronegócio. |
| **Estoque_Construção** | SGS 28770 (CAGED) | Float64 (Mil vínculos) | Alinhamento cronológico; saneamento de inconsistências | Mercado de Trabalho | Covariável exógena - Nível de atividade e investimentos na construção civil. |
| **Qte_Ovos** | SGS 1310 (IBGE) | Float64 (Mil dúzias) | Interpolação de atrasos; alinhamento de frequência MS | Atividade Econômica | Covariável exógena - Proxy física da oferta agropecuária de ciclo rápido. |
| **Produção_Derivados_Petróleo** | SGS 1391 (ANP) | Float64 (Mil m³) | Alinhamento MS; interpolação linear de lacunas | Energia / Combustíveis | Covariável exógena - Volume de refino de petróleo e oferta energética. |
| **Consumo_Gasolina** | SGS 1393 (ANP) | Float64 (m³) | Sincronização MS; zeros de atraso tratados como NaN | Energia / Combustíveis | Covariável exógena - Consumo automotivo e pressão de curto prazo em transporte. |
| **Consumo_Óleo_Combustível** | SGS 1395 (ANP) | Float64 (t) | Alinhamento temporal e interpolação de competência | Energia / Combustíveis | Covariável exógena - Indicador logístico do transporte rodoviário pesado. |
| **Consumo_Energia_Comercial** | SGS 1402 (EPE) | Float64 (MWh) | Sincronização MS; zeros tratados como NaN | Energia / Combustíveis | Covariável exógena - Carga elétrica no comércio (termômetro em tempo real). |
| **Consumo_Energia_Residencial** | SGS 1403 (EPE) | Float64 (MWh) | Alinhamento MS; interpolação temporal contínua | Energia / Combustíveis | Covariável exógena - Padrão de consumo elétrico das famílias brasileiras. |
| **Consumo_Energia_Total** | SGS 1406 (EPE) | Float64 (MWh) | Sincronização mensal MS; verificação de integridade | Energia / Combustíveis | Covariável exógena - Demanda física global de energia elétrica produtiva. |
| **Regime de Inflação** | IBGE / CMN | Categórico Nominal | Discretização paramétrica: Deflação, Meta e Alta | Governança / CMN | Atributo nominal derivado - Caracterização qualitativa da trajetória. |
| **mes_sin** | Engenharia Temporal | Float64 (Adimensional) | Harmônica periódica senoidal: $\sin(2\pi m / 12)$ | Sazonalidade | Covariável sazonal contínua - Captura de ciclos periódicos anuais. |
| **mes_cos** | Engenharia Temporal | Float64 (Adimensional) | Harmônica periódica cossenoidal: $\cos(2\pi m / 12)$ | Sazonalidade | Covariável sazonal contínua - Captura de ciclos periódicos anuais. |

*Fonte: Elaboração própria com base no pipeline computacional desenvolvido e validado com os stakeholders (2026).*

---

## Referências Bibliográficas

- [1] BOX, G. E.; JENKINS, G. M.; REINSEL, G. C.; LJUNG, G. M. *Time Series Analysis: Forecasting and Control*. 5. ed. Hoboken: John Wiley & Sons, 2015.
- [2] BANCO CENTRAL DO BRASIL (BACEN). *Sistema Gerenciador de Séries Temporais (SGS)*. Disponível em: <https://www3.bcb.gov.br/sgspub/>. Acesso em: 16 set. 2026.
- [3] BANCO CENTRAL DO BRASIL (BACEN). *Relatório de Inflação*. v. 26, n. 2. Brasília: Banco Central do Brasil, 2024.
- [4] BLANCHARD, O. *Macroeconomia*. 7. ed. São Paulo: Pearson, 2017.
- [5] BRESSER-PEREIRA, L. C.; NAKANO, Y. *A Teoria da Inflação Inercial*. São Paulo: Brasiliense, 1984.
- [6] GARCIA, M. G.; MEDEIROS, M. C.; VASCONCELOS, G. F. Real-time inflation forecasting with high-dimensional data: the case of Brazil. *International Journal of Forecasting*, v. 33, n. 3, p. 679–693, 2017.
- [7] HASTIE, T.; TIBSHIRANI, R.; FRIEDMAN, J. *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*. 2. ed. New York: Springer, 2009.
- [8] HOLLAND, J. H. *Adaptation in Natural and Artificial Systems: An Introductory Analysis with Applications to Biology, Control, and Artificial Intelligence*. Cambridge: MIT Press, 1992.
- [9] HYNDMAN, R. J.; ATHANASOPOULOS, G. *Forecasting: Principles and Practice*. 3. ed. Melbourne: OTexts, 2021.
- [10] INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). *Sistema Nacional de Índices de Preços ao Consumidor (SNIPC): Metodologia do IPCA e INPC*. Rio de Janeiro: IBGE, 2020.
- [11] KENNEDY, J.; EBERHART, R. Particle swarm optimization. In: *Proceedings of ICNN'95 - International Conference on Neural Networks*, v. 4, p. 1942–1948, 1995.
- [12] KHANDANI, A. E.; KIM, A. J.; LO, A. W. Consumer credit-risk models via machine-learning algorithms. *Journal of Banking & Finance*, v. 34, n. 11, p. 2767–2787, 2010.
- [13] MANKIW, N. G. *Macroeconomia*. 10. ed. Rio de Janeiro: LTC, 2021.
- [14] MEDEIROS, M. C.; VASCONCELOS, G. F.; VEIGA, Á.; ZILBERMAN, E. Forecasting inflation in a data-rich environment: the benefits of machine learning methods. *Journal of Business & Economic Statistics*, v. 39, n. 1, p. 98–119, 2021.
- [15] PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*, v. 12, p. 2825–2830, 2011.
- [16] SIMONSEN, M. H. *30 Anos de Indexação*. Rio de Janeiro: Editora FGV, 1995.
- [17] TAYLOR, J. B. Discretion versus policy rules in practice. *Carnegie-Rochester Conference Series on Public Policy*, v. 39, p. 195–214, 1993.
- [18] ZHANG, G. P. Time series forecasting using a hybrid ARIMA and neural network model. *Neurocomputing*, v. 50, p. 159–175, 2003.
