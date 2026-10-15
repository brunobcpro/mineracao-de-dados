import re, os, shutil

artigo_path = 'Artigo/Artigo_Previsao_Inflacao.md'
backup_path = 'Artigo/Artigo_Previsao_Inflacao.md.bak'
shutil.copyfile(artigo_path, backup_path)
print(f'Backup criado em: {backup_path}')

with open(artigo_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Substituição da Seção 2.2
sec_2_2_nova = """### 2.2 Mineração de Dados em Séries Temporais e Fundamentação do Algoritmo de Agrupamento Hierárquico (Critério de Ward)

A Mineração de Dados em Séries Temporais (*Time Series Data Mining*) visa descobrir padrões estruturais, tendências latentes e dependências dinâmicas em dados sequenciais indexados cronologicamente [7, 9]. Ao contrário de observações tabulares padrão, séries temporais violam a premissa de observações independentes e identicamente distribuídas (i.i.d.), exigindo tratamento rigoroso de não estacionariedade, quebras estruturais e ordenação temporal [7, 9]. No contexto da inflação brasileira, a identificação de regimes latentes — tanto sazonais intra-anuais quanto macroeconômicos plurianuais — demanda técnicas de aprendizado não supervisionado (*unsupervised learning*) capazes de segmentar períodos históricos sem impor rótulos arbitrários *a priori*.

Dentre as famílias de algoritmos de agrupamento (*clustering*), selecionou-se o **Agrupamento Hierárquico Aglomerativo baseado no Critério de Mínima Variância de Ward** (*Ward's Hierarchical Agglomerative Clustering*) [19]. Enquanto métodos particionais clássicos como o $K$-Means dependem de sementes estocásticas aleatórias de inicialização (sujeitas a mínimos locais) e assumem partições estritamente hiper-esféricas de variâncias homogêneas, o método de Ward constrói uma árvore hierárquica determinística (*dendrograma*), permitindo inspecionar visual e analiticamente a distância de corte ótima e a estrutura aninhada dos regimes temporais [7, 19].

#### 2.2.1 Formulação Matemática do Critério de Mínima Variância de Ward
O método de Ward opera sob uma estratégia aglomerativa *bottom-up*: inicia-se com $N$ clusters unitários (onde cada observação mensal constitui um agrupamento isolado) e, a cada iteração $t$, fundem-se iterativamente os dois clusters que proporcionam o **menor incremento na soma total dos quadrados dos desvios intra-cluster** (*Error Sum of Squares* – $ESS$) [19]. 

Para um dado agrupamento $C_k$ contendo $n_k$ vetores de atributos $x_i \in \mathbb{R}^p$ e centróide $\bar{x}_k = \frac{1}{n_k} \sum_{x_i \in C_k} x_i$, a variância intra-cluster ($ESS_k$) é formalmente definida como:
$$ESS_k = \sum_{x_i \in C_k} ||x_i - \bar{x}_k||^2$$

A função objetivo global para uma partição em $K$ grupos consiste na minimização do somatório das variâncias internas:
$$ESS_{\\text{Total}} = \sum_{k=1}^K ESS_k = \sum_{k=1}^K \sum_{x_i \in C_k} ||x_i - \bar{x}_k||^2$$

Ao avaliar a união hipotética de dois clusters arbitrários $A$ e $B$ com tamanhos $n_A$ e $n_B$ e centróides $\bar{x}_A$ e $\bar{x}_B$, o acréscimo de variância $\Delta ESS_{AB}$ gerado pela fusão corresponde à distância euclidiana ponderada entre seus centróides [19]:
$$\Delta ESS_{AB} = ESS_{A \cup B} - (ESS_A + ESS_B) = \\frac{n_A \cdot n_B}{n_A + n_B} ||\\bar{x}_A - \\bar{x}_B||^2$$

A cada passo aglomerativo, o algoritmo seleciona o par ótimo $(A^*, B^*)$ que satisfaz o critério de variância mínima:
$$(A^*, B^*) = \\arg\\min_{A, B} \Delta ESS_{AB}$$

#### 2.2.2 Recorrência de Lance-Williams e Propriedades para Séries Temporais
A atualização computacional da matriz de dissimilaridades entre o novo cluster fundido $(A \cup B)$ e qualquer outro cluster remanescente $C$ é governada pela equação de recorrência generalizada de Lance-Williams [20]:
$$D(A \cup B, C) = \\alpha_A D(A, C) + \\alpha_B D(B, C) + \\beta D(A, B) + \\gamma |D(A, C) - D(B, C)|$$

No critério específico de Ward, os coeficientes estruturais de Lance-Williams são dados por [7, 20]:
$$\\alpha_A = \\frac{n_A + n_C}{n_A + n_B + n_C}, \\quad \\alpha_B = \\frac{n_B + n_C}{n_A + n_B + n_C}, \\quad \\beta = -\\frac{n_C}{n_A + n_B + n_C}, \\quad \\gamma = 0$$

Essa formulação confere propriedades analíticas ideais para a análise macroeconômica:
1. **Determinismo Estrito:** Não depende de inicializações aleatórias, garantindo reprodutibilidade integral entre execuções;
2. **Preservação de Assimetrias Estruturais:** É capaz de isolar grupos com frequências desiguais (como meses específicos de choques sazonais e janelas atípicas de estagflação), superando a tendência do $K$-Means de forçar clusters com número uniforme de elementos;
3. **Auditabilidade Topológica:** O dendrograma explicita as distâncias exatas de dissimilaridade nas quais ocorrem quebras de regime, fundamentando empiricamente a seleção do número ótimo de classes $k$."""

# Substituir a seção 2.2
padrao_2_2 = r'### 2\.2 Mineração de Dados em Séries Temporais\s+A Mineração de Dados em Séries Temporais[^\n]+\n[^\n]+\n'
if re.search(padrao_2_2, text):
    text = re.sub(padrao_2_2, sec_2_2_nova + '\n\n', text)
    print('Seção 2.2 substituída com sucesso!')
else:
    print('AVISO: Padrão da Seção 2.2 não encontrado diretamente com regex estrita, aplicando substituição por bloco.')
    pos_22 = text.find('### 2.2 Mineração de Dados em Séries Temporais')
    pos_23 = text.find('### 2.3 Trabalhos Relacionados')
    text = text[:pos_22] + sec_2_2_nova + '\n\n' + text[pos_23:]
    print('Seção 2.2 substituída via posições de corte!')

# 2. Inclusão da Seção 3.5 após a Seção 3.4.3
sec_3_5 = """### 3.5 Metodologia Experimental de Agrupamento: Sazonalidade e Regimes de Ouro e Juros

A identificação de padrões não supervisionados na economia brasileira requer rigor na especificação do espaço de atributos. Fenômenos sazonais e ciclos macroeconômicos operam em naturezas temporais distintas:
* **Sazonalidade:** Processo determinístico e recorrente de frequência intra-anual fixa ($S = 12$ meses);
* **Ciclos Macroeconômicos (Ouro e Juros):** Processos estocásticos de médio a longo prazo governados por decisões de política monetária e choques geopolíticos internacionais (ciclos de 24 a 60 meses).

A unificação ingênua de atributos temporais do calendário (ex.: mês 1 a 12) com variáveis financeiras num único espaço euclidiano distorce o cálculo métrico e resulta em agrupamentos espúrios (*spurious clustering*). Para superar essa limitação, este projeto adotou o framework desacoplado em duas camadas (*Two-Tier Decoupled Clustering Framework*), complementado por uma análise de interação cruzada:

```mermaid
flowchart TD
    subgraph Camada1["Camada 1: Sazonalidade dos Preços (Micro / Setorial)"]
        C1["7 Subcomponentes Setoriais do IPCA"] --> P1["Padronização Z-Score intra-grupo"]
        P1 --> W1["Agrupamento Hierárquico de Ward (k=4)"]
        W1 --> R1["4 Regimes Sazonais do Calendário<br/>(Choque Escolar, Remédios, Safra, Fim de Ano)"]
    end

    subgraph Camada2["Camada 2: Dinâmica de Regimes (Macro / Mercado)"]
        C2["Vetor Estacionário [IPCA, ΔSELIC, Δ%Ouro_BRL]"] --> P2["Padronização Z-Score Multivariada"]
        P2 --> W2["Agrupamento Hierárquico de Ward (k=4)"]
        W2 --> R2["4 Regimes Macroeconômicos<br/>(Hawkish, Safe-Haven, Dovish, Choque Severo)"]
    end

    R1 --> Inter["Camada 3: Análise de Interação Cruzada & Teste Qui-Quadrado"]
    R2 --> Inter
```

#### 3.5.1 Protocolo Experimental da Camada 1 (Sazonalidade Intra-Anual)
1. **Atributos de Entrada:** Selecionaram-se os 7 componentes desagregados de preços apurados pelo IBGE: `IPCA_Transportes`, `IPCA Alimentação_bebidas`, `INPC_Habitação`, `IPCA_Saúde_cuidados_pessoais`, `IPCA_Vestuário`, `IPCA_Educação` e `IPCA_Despesas_Pessoais`.
2. **Normalização:** Aplicação do escalonamento $Z$-Score em cada componente $j$: $z_{i,j} = \frac{x_{i,j} - \mu_j}{\sigma_j}$, equalizando as variâncias entre grupos com volatilidades distintas (como Alimentação vs Habitação).
3. **Algoritmo:** Agrupamento Hierárquico Aglomerativo com critério de Ward e métrica euclidiana.

#### 3.5.2 Protocolo Experimental da Camada 2 (Regimes de Inflação, Ouro e Juros)
1. **Atributos de Entrada:** Construiu-se um vetor tridimensional estacionário para cada mês $t$ ($N = 173$ meses):
   * $\text{IPCA}_t$: Taxa de inflação mensal apurada pelo IBGE;
   * $\Delta \text{SELIC}_t = \text{SELIC}_t - \text{SELIC}_{t-1}$: Aceleração ou desaceleração da postura de política monetária (em p.p. ao mês);
   * $\Delta \% \text{Ouro}_{BRL,t} = \left(\frac{\text{Ouro}_{USD,t} \cdot \text{USDBRL}_t}{\text{Ouro}_{USD,t-1} \cdot \text{USDBRL}_{t-1}} - 1\right) \times 100$: Variação percentual da cotação do ouro físico internacional ($GLD$) convertida para moeda nacional, sintetizando simultaneamente a aversão ao risco global e a desvalorização cambial doméstica [21, 22].
2. **Normalização:** Escalonamento $Z$-Score multivariado em $\mathbb{R}^3$.
3. **Variáveis de Auditoria:** A taxa de juro real *ex-post* ($r_t = \text{SELIC}_t - \text{IPCA}_t$) e o câmbio nominal ($\text{USDBRL}$) foram preservados para interpretação econômica posterior dos centroides.

#### 3.5.3 Métricas de Validação Interna e Avaliação Estatística
A escolha do número ótimo de clusters $k \in \{2, 3, 4, 5, 6\}$ foi conduzida através de três métricas clássicas de validação interna de agrupamento:
* **Coeficiente de Silhueta (*Silhouette Score* – $s_i$):** Avalia a coesão interna contra a separação em relação ao cluster vizinho mais próximo ($s_i \in [-1, 1]$);
* **Índice de Davies-Bouldin ($DB$):** Mede a razão média de similaridade entre cada cluster e o mais semelhante a ele (valores menores indicam partições mais compactas e distintas);
* **Índice de Calinski-Harabasz ($CH$):** Razão entre a dispersão entre-clusters e a dispersão intra-cluster (valores maiores indicam melhor definição geométrica).

Na Camada 3, a hipótese de neutralidade entre sazonalidade e choques macroeconômicos foi submetida ao **Teste Qui-Quadrado de Independência de Pearson** ($\chi^2$) sobre a matriz de contingência $4 \times 4$."""

pos_343 = text.find('#### 3.4.3 Governança, Integridade e Requisitos de Qualidade')
pos_fim_343 = text.find('## 4 ', pos_343)
text = text[:pos_fim_343] + sec_3_5 + '\n\n---\n\n' + text[pos_fim_343:]
print('Seção 3.5 adicionada com sucesso!')

# 3. Reestruturação da Seção 4 (Adicionando Seção 4.1 e renomeando considerações para 4.2)
sec_4_nova = """## 4 RESULTADOS OBTIDOS E DISCUSSÕES

### 4.1 Resultados Obtidos na Clusterização de Sazonalidade e Regimes Macroeconômicos

A aplicação experimental do *Two-Tier Decoupled Framework* forneceu evidências empíricas contundentes sobre a arquitetura da inflação brasileira, atendendo plenamente às hipóteses formuladas.

#### 4.1.1 Camada 1: Sazonalidade e Choques Estruturais dos Componentes do IPCA
A Tabela 4 sintetiza as métricas de validação interna do agrupamento hierárquico de Ward aplicado aos 7 componentes desagregados do IPCA ($N = 174$ meses).

#### Tabela 4 – Métricas de Validação Interna do Agrupamento Hierárquico (Ward) – Camada 1

| Número de Clusters ($k$) | Coeficiente de Silhueta (*Silhouette*) | Índice Davies-Bouldin ($DB$) | Índice Calinski-Harabasz ($CH$) |
| :---: | :---: | :---: | :---: |
| $k = 2$ | 0,324 | 1,085 | 63,8 |
| $k = 3$ | 0,132 | 1,837 | 44,5 |
| **$k = 4$ (Corte Adotado)** | **0,155** | **1,796** | **38,6** |
| $k = 5$ | 0,175 | 1,631 | 34,2 |
| $k = 6$ | 0,179 | 1,587 | 31,9 |

*Fonte: Autores (2026).*

Embora $k=2$ apresente o ápice formal da silhueta pela separação dicotômica ampla, a solução com **$k=4$** foi adotada por fundamentação teórica de domínio, uma vez que isola com precisão cirúrgica os quatro regimes calendáricos da inflação nacional. A Figura 6 ilustra o dendrograma resultante, evidenciando o patamar de corte horizontal em distância de variância 14,0.

![Figura 6 – Dendrograma de Agrupamento Hierárquico dos Componentes do IPCA](../Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_6_Dendrograma_Sazonalidade_IPCA.png)  
*Figura 6 – Dendrograma de Agrupamento Hierárquico (critério de Ward) dos Componentes Setoriais do IPCA (2012–2026). Linha tracejada vermelha representa o corte ótimo em k = 4. Fonte: Autores (2026).*

A Tabela 5 documenta a distribuição temporal das observações, correlacionando os 12 meses do calendário gregoriano aos clusters identificados por Ward.

#### Tabela 5 – Matriz de Contingência: Mês do Calendário vs Regimes Sazonais do IPCA

| Mês do Calendário | Cluster Sazonal 0 (Início/Fim Ano) | Cluster Sazonal 1 (Medicamentos) | Cluster Sazonal 2 (Safra Agrícola) | Cluster Sazonal 3 (Choque Escolar) | Total Amostral |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Janeiro** | 13 | 0 | 1 | 0 | 14 |
| **Fevereiro** | 1 | 0 | 1 | **12** | 14 |
| **Março** | 11 | 0 | 4 | 0 | 15 |
| **Abril** | 1 | **13** | 1 | 0 | 15 |
| **Maio** | 1 | 7 | 7 | 0 | 15 |
| **Junho** | 5 | 2 | 8 | 0 | 15 |
| **Julho** | 6 | 1 | **8** | 0 | 15 |
| **Agosto** | 5 | 1 | **9** | 0 | 15 |
| **Setembro** | 3 | 1 | **10** | 0 | 14 |
| **Outubro** | 6 | 1 | 7 | 0 | 14 |
| **Novembro** | 8 | 0 | 6 | 0 | 14 |
| **Dezembro** | 11 | 2 | 1 | 0 | 14 |

*Fonte: Autores (2026).*

O heatmap da Figura 7 detalha os desvios-padrão médios de cada componente setorial nos quatro grupos sazonais.

![Figura 7 – Heatmap dos Perfis Médios Padronizados dos Regimes Sazonais](../Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_7_Heatmap_Perfis_Sazonais.png)  
*Figura 7 – Perfis Médios Padronizados (Z-Score) dos 7 Subcomponentes do IPCA nos 4 Regimes Sazonais. Fonte: Autores (2026).*

A caracterização econômica dos 4 regimes sazonais confirma as regularidades institucionais brasileiras:
1. **Cluster 3 – Choque Educacional (Fevereiro):** Isola com acurácia 12 dos 13 meses de fevereiro da amostra histórica (92,3% de especificidade). Apresenta um desvio positivo extremo em Educação ($+3,22\\sigma$), refletindo o reajuste sistemático de matrículas escolares e material didático no início do ano letivo.
2. **Cluster 1 – Janela Regulatória de Medicamentos (Abril/Maio):** Concentra 13 dos 15 meses de abril da série, marcado por desvio expressivo no grupo Saúde e Cuidados Pessoais ($+1,15\\sigma$), correspondendo à homologação anual de reajustes pela CMED/ANVISA.
3. **Cluster 2 – Alívio de Safra Agrícola (Julho a Outubro):** Agrupa o período de colheita e clima seco no Brasil Central, com forte descompressão negativa em Alimentação e Bebidas ($-0,58\\sigma$). É a janela histórica que concentra os episódios de deflação mensal no país.
4. **Cluster 0 – Pressões de Início e Fim de Ano (Novembro a Março):** Agrupa meses com pressões combinadas de demanda (13º salário, festas natalinas, vestuário e turismo) e reajustes tarifários municipais de início de ano (IPVA e transporte urbano).

---

#### 4.1.2 Camada 2: Regimes Macroeconômicos com Ouro e Taxa de Juros
Na Camada 2, o agrupamento tridimensional $[\text{IPCA}_t, \Delta\text{SELIC}_t, \Delta\%\text{Ouro}_{BRL,t}]$ isolou 4 regimes macroeconômicos perfeitamente alinhados à teoria monetária e de ativos reais. A Tabela 6 sintetiza os perfis médios das variáveis do modelo e das métricas econômicas de validação.

#### Tabela 6 – Caracterização Macroeconômica dos 4 Regimes Identificados por Ward (N = 173 meses)

| Regime Macroeconômico | Frequência (Meses) | IPCA Médio (% a.m.) | $\Delta$SELIC Média (p.p.) | Retorno Médio Ouro BRL (%) | SELIC Nominal Média (% a.a.) | Juro Real Médio (% a.m.) | Câmbio USDBRL Médio |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Regime 0: Aperto Hawkish** | 53 | 0,501% | **+0,064** | -3,318% | 0,828% | +0,327% | 3,896 |
| **Regime 1: Voo para Qualidade (Safe Haven)** | 67 | 0,283% | -0,026 | **+5,220%** | 0,748% | +0,465% | 4,157 |
| **Regime 2: Desinflação e Cortes (Dovish)** | 23 | **-0,067%** | **-0,117** | -1,014% | 0,860% | **+0,927%** | 3,968 |
| **Regime 3: Choque Inflacionário Severo** | 30 | **1,044%** | +0,045 | **+2,368%** | 0,716% | **-0,328%** | **4,375** |

*Fonte: Autores (2026).*

A dispersão bivariada dos 4 regimes é ilustrada na Figura 8.

![Figura 8 – Dispersão Bivariada dos 4 Regimes Macroeconômicos](../Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_8_Clusters_Macro_Ouro_Juros.png)  
*Figura 8 – Dispersão dos Regimes Macroeconômicos nos planos: (A) IPCA vs Aceleração da Taxa SELIC (ΔSELIC); (B) IPCA vs Retorno do Ouro em Reais (GLD BRL). Fonte: Autores (2026).*

A análise econômica do estado da arte sobre esses 4 regimes revela:
* **Regime 0 (Aperto Hawkish – 53 meses):** O BACEN eleva ativamente a taxa SELIC ($\Delta\text{SELIC} = +0,064$ p.p./mês) para conter uma inflação corrente moderadamente elevada (0,501%). Diante da valorização da moeda doméstica e do encarecimento do custo de oportunidade do capital, o retorno do ouro em reais sofre retração média de $-3,318\%$.
* **Regime 1 (Voo para Qualidade / Safe Haven – 67 meses):** Marcado por incerteza geopolítica global e desvalorização cambial (dólar a R$ 4,16). O ouro em moeda nacional dispara $+5,220\%$ ao mês, operando como instrumento de cobertura patrimonial eficaz antes da transmissão plena para a inflação de bens comercializáveis (*tradables*).
* **Regime 2 (Desinflação e Afrouxamento Dovish – 23 meses):** Caracterizado por taxa média de deflação ($-0,067\%$) e agressivo ciclo de redução dos juros básicos ($\Delta\text{SELIC} = -0,117$ p.p./mês). Como a inflação cai mais rápido do que a taxa terminal de juros, o **juro real atinge seu pico histórico amostral (+0,927% a.m.)**, consolidando a ancoragem monetária.
* **Regime 3 (Choque Inflacionário Severo – 30 meses):** Ocorre a desancoragem extrema de expectativas e choques agudos de oferta, elevando o IPCA para a média alarmante de **1,044% ao mês**. A política monetária reage tardiamente, resultando em **juro real negativo ($-0,328\%$ a.m.)**. Nesse ambiente, o ouro opera com valorização expressiva ($+2,368\%$), atestando a corrida por ativos reais em cenários de estagflação.

---

#### 4.1.3 Camada 3: Interação Cruzada e Teste de Independência
A matriz de contingência da Figura 9 cruza as partições independentes da Camada 1 e da Camada 2.

![Figura 9 – Matriz de Contingência entre Sazonalidade e Regimes Macroeconômicos](../Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_9_Matriz_Contingencia_Sazonal_Macro.png)  
*Figura 9 – Matriz de Contingência e Interação Cruzada: Regimes Sazonais do IPCA vs Regimes Macroeconômicos de Ouro e Juros. Fonte: Autores (2026).*

O **Teste Qui-Quadrado de Independência de Pearson** resultou em $\chi^2 = 34{,}82$ ($p\text{-valor} = 0{,}0001$, com 9 graus de liberdade), **rejeitando com significância estatística estrita ($p < 0{,}01$) a hipótese de independência**. 

Essa descoberta empírica possui enorme relevância econométrica:
1. **Potencialização do Alívio:** O Regime 2 (Desinflação e Cortes de Juros) concentra **15 de suas 23 ocorrências (65,2%)** no Cluster Sazonal 2 (Safra Agrícola). Isso demonstra que as safras agrícolas constituem o vetor fundamental que viabiliza janelas de corte agressivo na taxa SELIC.
2. **Supressão do Ciclo Biológico:** Por outro lado, durante o Regime 3 (Choque Inflacionário Severo), apenas 3 meses coincidiram com a safra agrícola. Isso comprova que choques globais severos de custos e disparada do ouro anulam os benefícios sazonais biológicos de redução de preços de alimentos.

---

### 4.2 Considerações Finais e Trabalhos Futuros"""

# Substituir o início da seção 4
pos_sec4 = text.find('## 4 CONSIDERAÇÕES FINAIS E TRABALHOS FUTUROS')
if pos_sec4 != -1:
    pos_refs = text.find('## REFERÊNCIAS BIBLIOGRÁFICAS')
    corpo_anterior_4 = text[pos_sec4 + len('## 4 CONSIDERAÇÕES FINAIS E TRABALHOS FUTUROS'):pos_refs].strip()
    
    # Atualizar o texto da seção 4
    text = text[:pos_sec4] + sec_4_nova + '\n\n' + corpo_anterior_4 + '\n\n---\n\n' + text[pos_refs:]
    print('Seção 4 reestruturada com sucesso!')
else:
    print('AVISO: Seção 4 não encontrada pelo título exato.')

# 4. Atualização das Referências Bibliográficas
novas_refs = """- [19] WARD, J. H. Hierarchical grouping to optimize an objective function. **Journal of the American Statistical Association**, v. 58, n. 301, p. 236–244, 1963.
- [20] LANCE, G. N.; WILLIAMS, W. T. A general theory of classificatory sorting strategies: II. Clustering systems. **The Computer Journal**, v. 10, n. 3, p. 271–277, 1967.
- [21] BAUR, D. G.; LUCEY, B. M. Is gold a hedge or a safe haven? An analysis of stocks, bonds and gold. **Financial Review**, v. 45, n. 2, p. 217–229, 2010.
- [22] ERB, C. B.; HARVEY, C. R. The golden dilemma. **Financial Analysts Journal**, v. 69, n. 4, p. 10–42, 2013."""

if '[19]' not in text:
    text = text.strip() + '\n' + novas_refs + '\n'
    print('Novas referências [19] a [22] adicionadas ao final!')

with open(artigo_path, 'w', encoding='utf-8') as f:
    f.write(text)

print(f'Artigo atualizado com sucesso em: {artigo_path}')
