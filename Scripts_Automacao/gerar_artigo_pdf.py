import os
import base64
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR_ARTIGO = os.path.join(BASE_DIR, 'Artigo')
DIR_GRAFICOS = os.path.join(BASE_DIR, 'Entrega_Classroom', '4_Graficos_Alta_Resolucao')
DIR_LOGOS = os.path.join(DIR_ARTIGO, 'Logos')

LOGO_UPE = os.path.join(DIR_LOGOS, 'logo_upe.png')
LOGO_POLI = os.path.join(DIR_LOGOS, 'logo_poli.png')

def to_b64(path):
    if os.path.exists(path):
        with open(path, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
            ext = os.path.splitext(path)[1].replace('.', '')
            return f"data:image/{ext};base64,{data}"
    return ""

b64_upe = to_b64(LOGO_UPE)
b64_poli = to_b64(LOGO_POLI)
b64_fig1 = to_b64(os.path.join(DIR_GRAFICOS, 'Figura_1_Histograma_IPCA.png'))
b64_fig2 = to_b64(os.path.join(DIR_GRAFICOS, 'Figura_2_Boxplot_IPCA.png'))
b64_fig3 = to_b64(os.path.join(DIR_GRAFICOS, 'Figura_3_Dispersao_IPCA_Cambio.png'))
b64_fig4 = to_b64(os.path.join(DIR_GRAFICOS, 'Figura_4_Distribuicao_Regimes.png'))

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Mineração de Séries Temporais para Previsão da Inflação</title>
<style>
  @page {{
    size: A4;
    margin: 25mm 20mm 20mm 25mm;
    @bottom-right {{
      content: counter(page);
      font-family: Arial, sans-serif;
      font-size: 9pt;
      color: #666;
    }}
  }}

  body {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11pt;
    line-height: 1.35;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
    text-align: justify;
  }}

  /* Capa */
  .capa {{
    page-break-after: always;
    height: 92vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    padding: 10px 0;
  }}

  .capa-logos {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 35px;
    margin-bottom: 20px;
  }}

  .capa-logos img.upe {{
    height: 90px;
  }}

  .capa-logos img.poli {{
    height: 65px;
  }}

  .capa-instituicao {{
    font-size: 11pt;
    font-weight: bold;
    line-height: 1.3;
    margin-bottom: 30px;
  }}

  .capa-instituicao .campus {{
    font-style: italic;
    font-weight: normal;
  }}

  .capa-autores {{
    font-size: 11.5pt;
    font-weight: bold;
    line-height: 1.5;
    margin: 40px 0;
  }}

  .capa-titulo {{
    font-size: 13pt;
    font-weight: bold;
    color: #1a1a1a;
    line-height: 1.3;
    margin: 40px 10px;
  }}

  .capa-rodape {{
    font-size: 11pt;
    font-weight: bold;
    line-height: 1.3;
  }}

  /* Corpo do Artigo */
  h1 {{
    font-size: 13pt;
    color: #1F4E79;
    margin-top: 24px;
    margin-bottom: 8px;
    font-weight: bold;
    page-break-after: avoid;
  }}

  h2 {{
    font-size: 11.5pt;
    color: #1F4E79;
    margin-top: 18px;
    margin-bottom: 6px;
    font-weight: bold;
    page-break-after: avoid;
  }}

  h3 {{
    font-size: 11pt;
    color: #333333;
    margin-top: 14px;
    margin-bottom: 4px;
    font-weight: bold;
    page-break-after: avoid;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 8px;
    text-indent: 1.25cm;
  }}

  p.no-indent {{
    text-indent: 0;
  }}

  ul {{
    margin-top: 4px;
    margin-bottom: 10px;
    padding-left: 25px;
  }}

  li {{
    margin-bottom: 4px;
  }}

  /* Callout */
  .callout {{
    border-left: 4px solid #1F4E79;
    background-color: #F4F6F9;
    padding: 10px 14px;
    margin: 12px 0;
    font-size: 10.5pt;
    page-break-inside: avoid;
  }}

  .callout-title {{
    font-weight: bold;
    color: #1F4E79;
    margin-bottom: 4px;
  }}

  .callout-text {{
    font-style: italic;
    color: #222;
  }}

  /* Imagens */
  .figura-container {{
    text-align: center;
    margin: 16px 0;
    page-break-inside: avoid;
  }}

  .figura-container img {{
    max-width: 90%;
    height: auto;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
  }}

  .legenda {{
    font-size: 9pt;
    font-style: italic;
    color: #444;
    margin-top: 4px;
    text-align: center;
  }}

  /* Tabelas */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 8pt;
    page-break-inside: avoid;
  }}

  th {{
    background-color: #1F4E79;
    color: #FFFFFF;
    font-weight: bold;
    padding: 6px 5px;
    border: 1px solid #D1D5DB;
    text-align: center;
  }}

  td {{
    padding: 5px 5px;
    border: 1px solid #D1D5DB;
    vertical-align: middle;
  }}

  tr:nth-child(even) td {{
    background-color: #F9FAFB;
  }}

  .tbl-title {{
    font-size: 9.5pt;
    font-weight: bold;
    text-align: center;
    margin-top: 14px;
    margin-bottom: 4px;
    page-break-after: avoid;
  }}

  .tbl-source {{
    font-size: 8pt;
    text-align: center;
    color: #555;
    margin-top: 2px;
    margin-bottom: 12px;
  }}

  .ref-list {{
    font-size: 9.5pt;
    line-height: 1.25;
  }}

  .ref-item {{
    margin-bottom: 6px;
    text-indent: 0;
  }}
</style>
</head>
<body>

  <!-- CAPA OFICIAL -->
  <div class="capa">
    <div>
      <div class="capa-logos">
        <img class="upe" src="{b64_upe}" alt="Logo UPE" />
        <img class="poli" src="{b64_poli}" alt="Logo POLI" />
      </div>
      <div class="capa-instituicao">
        UNIVERSIDADE DE PERNAMBUCO<br>
        ESCOLA POLITÉCNICA DE PERNAMBUCO - POLI<br>
        <span class="campus">CAMPUS RECIFE</span><br>
        CURSO DE ENGENHARIA DA COMPUTAÇÃO<br>
        DISCIPLINA: MINERAÇÃO DE DADOS<br>
        PROFESSOR: PROF. DR. ALEXANDRE MACIEL
      </div>
    </div>

    <div class="capa-autores">
      BRUNO PROTÁSIO<br>
      DANIEL MENESES<br>
      MARCUS VINICIUS<br>
      VINICYUS EMANUEL
    </div>

    <div class="capa-titulo">
      MINERAÇÃO DE SÉRIES TEMPORAIS PARA PREVISÃO DA INFLAÇÃO:<br>
      ARQUITETURA HÍBRIDA MULTIVARIADA E OTIMIZAÇÃO BIOINSPIRADA DE ATRIBUTOS
    </div>

    <div class="capa-rodape">
      RECIFE<br>
      2026
    </div>
  </div>

  <!-- CORPO DO ARTIGO -->
  <h1>1 INTRODUÇÃO</h1>

  <p>A trajetória dos preços em uma economia em desenvolvimento como a brasileira é marcada por uma tensão permanente entre a memória do passado e os choques imprevisíveis do presente. Ao longo de décadas, a sociedade conviveu com oscilações inflacionárias que desgastam a renda do trabalho, tornam o crédito escasso e impõem pesadas incertezas sobre o planejamento das famílias e das empresas. A consolidação da estabilidade monetária com a criação do Plano Real e a posterior adoção do regime de metas para a inflação estabeleceram um pacto institucional: manter o poder de compra da moeda através do monitoramento rigoroso do Índice Nacional de Preços ao Consumidor Amplo (IPCA), calculado mensalmente pelo Instituto Brasileiro de Geografia e Estatística (IBGE).</p>

  <p>Contudo, conduzir e antecipar essa dinâmica é uma tarefa desafiadora. O Banco Central do Brasil utiliza a taxa básica de juros (Selic) como seu principal instrumento de controle, mas as decisões de política monetária demandam entre dois e quatro trimestres para produzir efeitos plenos sobre o consumo e os investimentos. Essa defasagem temporal impede que gestores públicos e privados naveguem olhando apenas para os preços observados ontem; torna-se imperativo antecipar o comportamento futuro do índice para embasar decisões tempestivas.</p>

  <p>Historicamente, a literatura estatística abordou a previsão de preços sob a ótica univariada, partindo da premissa de que o próprio histórico de inflação sintetiza a inércia dos contratos e as expectativas dos agentes. Modelos clássicos de séries temporais assumem que as defasagens passadas e os ciclos sazonais são suficientes para projetar os próximos períodos. Entretanto, a economia brasileira é exposta a perturbações exógenas frequentes: choques cambiais que encarecem insumos importados, oscilações severas nas cotações internacionais de commodities energéticas, secas que penalizam a produção agrícola e desequilíbrios no mercado de trabalho.</p>

  <p>Surge, assim, um dilema central de modelagem: modelos estritamente univariados correm o risco de ignorar sinais antecipados cruciais emitidos por variáveis externas, enquanto abordagens multivariadas que incorporam dezenas de indicadores econômicos enfrentam o risco de ruído amostral, multicolinearidade e superajuste (<i>overfitting</i>). O presente projeto investiga essa fronteira empírica sob a ótica da Engenharia da Computação e da Mineração de Dados. A presente entrega foca na formulação do problema, na integração interdisciplinar com economistas e no pipeline completo de coleta, análise exploratória descritiva e pré-processamento de um robusto painel macroeconômico, preparando a base para a futura calibração de modelos preditivos e algoritmos bioinspirados de seleção de atributos.</p>

  <h2>1.1 Contextualização</h2>
  <p>A dinâmica da inflação no Brasil conecta-se diretamente à arquitetura do Sistema Financeiro Nacional. O Conselho Monetário Nacional (CMN) define as metas anuais de inflação, cabendo ao Banco Central do Brasil (BACEN) calibrar as condições financeiras para o seu cumprimento.</p>
  <p>Para a ciência e engenharia de dados, esse cenário desdobra-se em três pilares de relevância aplicada:</p>
  <ul>
    <li><b>Setor Público e Governança Macroeconômica:</b> O fornecimento de estimativas acuradas mitiga assimetrias informacionais, permitindo avaliar pressões de custos antes que se disseminem pela economia e auxiliando na ancoragem das expectativas de mercado;</li>
    <li><b>Mercado Financeiro e Atividade Corporativa:</b> Empresas utilizam projeções de inflação para reajustar contratos de fornecimento de longo prazo, planejar orçamentos de capital e gerenciar estoques. No mercado financeiro, a correta precificação de títulos indexados à inflação (como NTN-B e debêntures) e a gestão de risco de tesouraria dependem da acurácia dessas projeções;</li>
    <li><b>Pesquisa em Engenharia e Mineração de Dados:</b> Séries macroeconômicas de economias emergentes oferecem um ambiente de estresse para algoritmos computacionais, demandando engenharia de dados precisa para sincronizar bases heterogêneas, sanear dados ruidosos e evitar vazamento temporal.</li>
  </ul>

  <h2>1.2 Descrição do Problema</h2>
  <p>O desafio central consiste em arbitrar entre a inércia temporal e a sensibilidade a choques macroeconômicos externos:</p>
  <ul>
    <li><b>1. A Hipótese Univariada:</b> Postula que a inércia inflacionária — sustentada por indexação contratual e rigidez de preços — domina a trajetória da série, de modo que modelos autorregressivos simples superariam formulações complexas que demandam estimativas de terceiros;</li>
    <li><b>2. A Hipótese Multivariada:</b> Postula que indicadores antecedentes de preços no atacado, custos de transporte, cotação do dólar e nível de atividade agregada emitem sinais preditivos antecipados que o histórico isolado do índice de inflação é incapaz de capturar a tempo.</li>
  </ul>
  <p>A questão metodológica reside em determinar se a complexidade multivariada compensa o risco de instabilidade estatística e quais classes de variáveis econômicas trazem ganho preditivo mensurável.</p>

  <div class="callout">
    <div class="callout-title">Pergunta Central de Pesquisa:</div>
    <div class="callout-text">"A utilização de variáveis macroeconômicas exógenas melhora a acurácia preditiva da inflação frente a modelos puramente univariados? Quais atributos possuem maior capacidade de antecipar a trajetória da inflação brasileira?"</div>
  </div>

  <h2>1.3 Objetivos</h2>
  <h3>1.3.1 Objetivo Geral da Etapa Atual</h3>
  <p>Desenvolver o processo de mineração de dados focado na formulação do problema, fundamentação teórica, análise exploratória descritiva e pré-processamento integral de séries temporais da inflação brasileira e variáveis exógenas antecedentes, estruturando uma base de dados higienizada, consistente e documentada sob orientação de especialistas para fundamentar a futura calibração de modelos preditivos multivariados.</p>

  <h3>1.3.2 Objetivos Específicos do Escopo Atual</h3>
  <ul>
    <li><b>1. Engenharia e Coleta de Dados Macroeconômicos:</b> Coletar e consolidar a série histórica mensal do IPCA e de 28 variáveis exógenas candidatas de março de 2012 a agosto de 2026 via API oficial do SGS/Banco Central;</li>
    <li><b>2. Mapeamento de Stakeholders e Orientação Acadêmica:</b> Mapear os envolvidos no projeto, articulando a orientação acadêmica do Prof. Dr. Alexandre Maciel (POLI/UPE) e a consultoria de domínio macroeconômico do Prof. Guilherme Martins (FCAP/UPE);</li>
    <li><b>3. Fundamentação Teórica e Diferenciais Metodológicos:</b> Estruturar a revisão da literatura e estabelecer a matriz comparativa de diferenciais frente aos modelos clássicos e recentes;</li>
    <li><b>4. Caracterização Estatística e Visual dos Dados:</b> Conduzir análise descritiva univariada e bivariada dos atributos contínuos e discretos, explorando assimetrias, outliers e comportamento sob diferentes regimes nominais de inflação;</li>
    <li><b>5. Pipeline de Pré-processamento e Saneamento:</b> Implementar rotinas sistemáticas de limpeza de nulos, alinhamento temporal em frequência uniforme (Month-Start), tratamento de inconsistências, redução amostral e codificação de atributos;</li>
    <li><b>6. Estruturação do Dicionário de Dados da Base Consolidada:</b> Documentar formalmente todos os 31 atributos consolidados, seus códigos de origem, tipagem, procedimentos de pré-processamento e relevância de negócio.</li>
  </ul>

  <h2>1.4 Justificativa</h2>
  <p>Projeções de inflação influenciam a taxa de juros real da economia, os custos de captação de dívida soberana e a formação de preços no atacado e no varejo. Séries econômicas brasileiras apresentam não linearidades, quebras de regime e forte exposição a choques internacionais. Sob a perspectiva da computação aplicada, a pesquisa contribui ao estabelecer um pipeline reprodutível de engenharia de dados que transforma séries públicas brutas em um painel estruturado, alinhado e auditável, eliminando vieses e viabilizando a futura aplicação de estimadores preditivos avançados.</p>

  <h2>1.5 Escopo Negativo e Delimitação da Etapa</h2>
  <p>Para assegurar clareza quanto à entrega atual do projeto, definem-se os seguintes limites de escopo:</p>
  <ul>
    <li><b>Análise de Estacionariedade e Modelagem Preditiva nesta Fase:</b> A realização de testes de raiz unitária (ADF), transformações de diferenciação para modelos específicos, calibração de algoritmos preditivos (ARIMA, ARIMAX, Random Forest, Lasso, Arquitetura Híbrida) e otimização bioinspirada (GA e PSO) pertencem à etapa subsequente do projeto, não fazendo parte do escopo da presente entrega, que encerra-se formalmente no pré-processamento dos dados;</li>
    <li><b>Alta Frequência e Intradiário:</b> O estudo concentra-se na frequência mensal oficial e não aborda cotações diárias ou intradiárias de preços;</li>
    <li><b>Nível Microeconômico:</b> Não são investigadas cestas de consumo de indivíduos específicos, recortes regionais isolados ou desagregações domiciliares da POF;</li>
    <li><b>Prescrição de Política Econômica:</b> O trabalho tem finalidade analítica e de engenharia de dados, sem emitir recomendações normativas sobre o patamar adequado de juros ou diretrizes fiscais.</li>
  </ul>

  <hr style="border: 0; border-top: 1px solid #D1D5DB; margin: 24px 0;">

  <h1>2 FUNDAMENTAÇÃO TEÓRICA</h1>

  <h2>2.1 Área do Negócio: O Funcionamento da Inflação e a Dinâmica Econômica</h2>
  <p>Para compreender o desafio de antecipar a inflação, é necessário desmistificar o fenômeno em linguagem acessível a leitores de diferentes áreas e fundamentada na literatura macroeconômica.</p>

  <h3>O que é a Inflação na Prática?</h3>
  <p>De forma intuitiva, a inflação não é apenas o encarecimento de um produto específico, como o tomate ou a energia elétrica; ela representa o aumento contínuo e generalizado no nível de preços de bens e serviços de uma economia ao longo do tempo [4, 13]. O efeito prático mais imediato é a perda do poder de compra da moeda: se uma nota de R$ 100 permitia comprar um conjunto completo de mantimentos no início do ano e, meses depois, adquire apenas uma fração desses mesmos produtos, a moeda perdeu valor relativo [13].</p>

  <h3>Como o IPCA Mede Essa Realidade?</h3>
  <p>No Brasil, a inflação oficial é mensurada pelo Índice Nacional de Preços ao Consumidor Amplo (IPCA), calculado pelo IBGE desde 1979 e adotado formalmente como bússola do sistema de metas [10]. Para mensurá-lo, o IBGE não calcula uma média simples de preços: constrói-se uma "cesta média de consumo" ponderada, que reflete como as famílias com renda entre 1 e 40 salários mínimos distribuem seus gastos [10]. Despesas com alimentação, habitação e transporte possuem peso predominante no orçamento das famílias brasileiras; portanto, variações nesses grupos provocam impactos assimétricos sobre o índice geral.</p>

  <h3>Os Três Grandes Motores da Inflação Brasileira</h3>
  <p>A literatura econômica contemporânea e a experiência empírica brasileira identificam três forças fundamentais que movimentam os preços:</p>
  <ul>
    <li><b>1. A Inércia e a Memória da Moeda:</b> O Brasil atravessou décadas de inflação crônica antes do Plano Real, o que consolidou mecanismos formais e informais de "indexação" [5, 16]. Na prática, diversos preços da economia — como aluguéis residenciais, tarifas públicas, pedágios, mensalidades escolares e convenções coletivas de trabalho — são reajustados periodicamente pela inflação passada. Isso gera um comportamento de persistência ou "memória temporal": a inflação de hoje carrega em si a taxa observada no passado, perpetuando o ciclo mesmo na ausência de novos choques [5, 16];</li>
    <li><b>2. Choques de Oferta e Custos (Câmbio e Commodities):</b> Quando ocorrem perturbações externas, como a alta internacional do petróleo ou a desvalorização cambial do Real frente ao Dólar americano, os insumos de importação tornam-se imediatamente mais onerosos [3, 6]. O aumento nos preços dos combustíveis eleva o custo do frete rodoviário, que encarece a distribuição de alimentos e bens de consumo, produzindo o mecanismo clássico de repasse cambial (<i>pass-through</i>) para o consumidor final [6];</li>
    <li><b>3. Pressões de Demanda e o Hiato do Produto:</b> Quando a atividade econômica se expande aceleradamente, impulsionando a contratação de trabalhadores e o aumento da renda agregada acima da capacidade física das fábricas e prestadores de serviço de ofertar bens, surge escassez relativa [4, 17]. Os produtores ajustam os preços para cima para equilibrar o mercado, relação descrita classicamente pelo mecanismo da Curva de Phillips [4, 17].</li>
  </ul>

  <h3>O Banco Central e o 'Termostato' da Política Monetária</h3>
  <p>Para evitar desarranjos na estabilidade de preços, o Conselho Monetário Nacional (CMN) define uma meta percentual anual. O Banco Central atua como regulador do sistema por meio do Comitê de Política Monetária (COPOM), utilizando a taxa básica de juros (Selic) como instrumento regulador [3, 17].</p>
  <p>A taxa Selic funciona de maneira análoga a um termostato econômico:</p>
  <ul>
    <li><b>Elevação da Taxa Selic:</b> Quando a inflação ameaça ultrapassar o teto da meta, o Banco Central eleva a taxa Selic. O crédito fica mais caro, o custo de oportunidade de poupar aumenta, as empresas adiam investimentos e as famílias reduzem o consumo financiado. Essa desaceleração da demanda arrefece a alta dos preços [3, 13];</li>
    <li><b>Redução da Taxa Selic:</b> Por outro lado, se a economia se retrai e a inflação converge para níveis muito baixos, o BACEN pode reduzir a taxa Selic para reativar a atividade produtiva.</li>
  </ul>
  <p>O ponto crítico desse processo é a existência de defasagens temporais de transmissão (<i>transmission lags</i>): uma decisão tomada pelo COPOM hoje leva entre 6 e 12 meses para se propagar pelos canais de crédito, câmbio e expectativas até afetar os preços finais [3, 17]. Por esse motivo, as autoridades monetárias e os analistas de mercado dependem de modelos preditivos tempestivos, capazes de antecipar a trajetória da inflação no horizonte relevante.</p>

  <h2>2.2 Mineração de Dados</h2>
  <p style="font-style: italic; color: #555;">(Nota: O detalhamento conceitual e matemático dos algoritmos computacionais de aprendizado de máquina, redes neurais e operadores genéticos será incorporado nesta subseção na etapa subsequente do projeto, permanecendo este tópico reservado para a fundamentação algorítmica específica).</p>

  <h2>2.3 Trabalhos Relacionados e Análise de Diferenciais</h2>
  <p>A literatura sobre modelagem da inflação organiza-se em três paradigmas metodológicos principais:</p>
  <ul>
    <li><b>1. Modelagem Paramétrica Box-Jenkins:</b> A abordagem clássica de séries temporais de Box e Jenkins [1] consolidou o uso de processos autorregressivos integrados de médias móveis (ARIMA). Tais formulações capturam adequadamente a inércia estocástica e a sazonalidade, mas partem de hipóteses rígidas de linearidade e não respondem com tempestividade a choques de oferta exógenos [1, 9];</li>
    <li><b>2. Arquiteturas Híbridas Lineares e Não Lineares:</b> Zhang [18] introduziu a formulação híbrida canônica que decompõe uma série temporal na soma de uma componente linear com uma componente residual não linear ($y_t = L_t + N_t$). Ao aplicar redes neurais aos resíduos do ARIMA, Zhang demonstrou que a modelagem conjunta supera estimadores isolados. Contudo, suas aplicações originais concentraram-se em séries univariadas sem covariáveis macroeconômicas exógenas [18];</li>
    <li><b>3. Machine Learning Multivariado de Alta Dimensionalidade:</b> Estudos contemporâneos de econometria aplicada, como Garcia et al. [6] e Medeiros et al. [14], avaliaram o emprego de métodos de regularização (como Lasso e Elastic Net) e algoritmos ensemble (Random Forest) alimentados por grandes painéis de dados econômicos. Embora demonstrem que dados externos contêm sinal preditivo, tais estudos frequentemente enfrentam o custo da multicolinearidade e da perda de aderência quando não há uma modelagem prévia da inércia autoregressiva estrutural [6, 14].</li>
  </ul>

  <p>Para evidenciar com precisão como o presente projeto se insere nessa fronteira e quais lacunas metodológicas preenche, a Tabela 1 sintetiza uma análise comparativa baseada em critérios funcionais e computacionais, confrontando os trabalhos da literatura com a abordagem proposta para o projeto.</p>

  <div class="tbl-title">Tabela 1 – Matriz Comparativa de Trabalhos Relacionados e Diferenciais Metodológicos do Projeto</div>
  <table>
    <thead>
      <tr>
        <th style="width: 20%;">Dimensão Metodológica</th>
        <th style="width: 20%;">Modelos Clássicos [1]</th>
        <th style="width: 20%;">Híbridos Tradicionais [18]</th>
        <th style="width: 20%;">Machine Learning [14]</th>
        <th style="width: 20%;">Abordagem Proposta</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Estrutura de Modelagem</b></td>
        <td>Linear univariada estrita (ARIMA / SARIMA).</td>
        <td>Híbrida aditiva univariada (ARIMA + RNA nos resíduos).</td>
        <td>Regressores não lineares puros ou regularizados (Lasso, RF).</td>
        <td><b>Híbrida aditiva multivariada (ARIMAX + RF nos resíduos).</b></td>
      </tr>
      <tr>
        <td><b>Espaço de Exógenas</b></td>
        <td>Ausente (apenas o histórico passado da própria série).</td>
        <td>Ausente (opera unicamente com defasagens da série dependente).</td>
        <td>Amplo painel multivariado sem filtragem otimizada de atributos.</td>
        <td><b>28 covariáveis em 4 pilares macroeconômicos fundamentais.</b></td>
      </tr>
      <tr>
        <td><b>Seleção de Atributos</b></td>
        <td>Inexistente (critérios AIC/BIC em ordens p, d, q).</td>
        <td>Inexistente (foco apenas no ajuste de resíduos temporais).</td>
        <td>Penalização paramétrica passiva (L1/Lasso) ou importância em árvores.</td>
        <td><b>Meta-heurísticas bioinspiradas ativas (GA e PSO) para seleção global.</b></td>
      </tr>
      <tr>
        <td><b>Tratamento de Choques</b></td>
        <td>Incapaz de modelar quebras estruturais ou choques externos.</td>
        <td>Modela não linearidades endógenas, mas cego a choques externos.</td>
        <td>Captura interações não lineares, mas negligencia a inércia estocástica pura.</td>
        <td><b>ARIMAX ancora a inércia e Random Forest absorve os choques residuais.</b></td>
      </tr>
      <tr>
        <td><b>Prevenção de Vazamento</b></td>
        <td>Divisão amostral simples ou estimação em toda a amostra.</td>
        <td>Divisão estática simples de treino e teste.</td>
        <td>Frequentemente adota validação cruzada k-fold sem ordem temporal.</td>
        <td><b>Validação dinâmica Walk-Forward de 1 passo (h=1) sequencial.</b></td>
      </tr>
      <tr>
        <td><b>Aplicação Econômica</b></td>
        <td>Séries sintéticas ou industriais genéricas.</td>
        <td>Séries padronizadas internacionais de baixa volatilidade.</td>
        <td>Avaliação em mercados desenvolvidos sem indexação inflacionária.</td>
        <td><b>Painel brasileiro (2012–2026, 174 meses), com validação da FCAP/UPE.</b></td>
      </tr>
    </tbody>
  </table>
  <div class="tbl-source">Fonte: Elaboração própria com base na revisão sistemática da literatura (2026).</div>

  <hr style="border: 0; border-top: 1px solid #D1D5DB; margin: 24px 0;">

  <h1>3 MATERIAIS E MÉTODOS</h1>

  <h2>3.1 Stakeholders Envolvidos</h2>
  <p>A condução e a validação do projeto contam com a participação e o direcionamento de diferentes partes interessadas (<i>stakeholders</i>), articulando a liderança acadêmica na disciplina, a consultoria de domínio macroeconômico e a aplicabilidade prática:</p>

  <ul>
    <li><b>1. Professor da Disciplina e Orientador Metodológico:</b><br>
    <b>Prof. Dr. Alexandre Maciel (Escola Politécnica de Pernambuco – POLI/UPE):</b> Docente responsável pela disciplina de Mineração de Dados no curso de Engenharia da Computação. Atua como o principal stakeholder acadêmico e orientador metodológico do projeto, tendo como responsabilidades:
      <ul>
        <li>Orientar e avaliar a conformidade técnica do projeto com os preceitos científicos de Descoberta de Conhecimento em Bases de Dados (KDD) e Mineração de Dados;</li>
        <li>Avaliar o rigor do pipeline de engenharia de dados, garantindo reprodutibilidade e prevenção de vazamento temporal (<i>lookahead bias</i>);</li>
        <li>Validar as decisões de saneamento, tratamento de dados ausentes e estruturação formal do Dicionário de Dados;</li>
        <li>Avaliar a aderência do artigo aos padrões institucionais e critérios de avaliação da POLI-UPE.</li>
      </ul>
    </li>
    <li><b>2. Stakeholder Especialista de Domínio (Consultoria Macroeconômica):</b><br>
    <b>Prof. Guilherme Martins (Faculdade de Ciências da Administração de Pernambuco – FCAP/UPE):</b> Economista e docente da UPE, atuando como o consultor especialista de domínio do projeto. Sua responsabilidade e interesse residem em:
      <ul>
        <li>Validar a pertinência teórica das 28 variáveis exógenas candidatas à luz da teoria macroeconômica e das peculiaridades do mercado brasileiro;</li>
        <li>Orientar sobre a dinâmica dos mecanismos de transmissão de preços (<i>pass-through</i> cambial, inércia de contratos e tarifas públicas reguladas);</li>
        <li>Assegurar que os procedimentos de pré-processamento preservem a integridade e o significado econômico das séries históricas;</li>
        <li>Avaliar a consistência das conclusões exploratórias frente à política monetária conduzida pelo BACEN e pelo COPOM.</li>
      </ul>
    </li>
    <li><b>3. Stakeholders de Aplicação e Beneficiários Finais (Decisores Econômicos):</b>
      <ul>
        <li><b>Analistas de Mercado Financeiro e Gestores de Ativos:</b> Interessados em dados macroeconômicos saneados e consistentes para precificação de títulos públicos indexados (como NTN-B e debêntures incentivadas) e gestão de riscos de carteira;</li>
        <li><b>Departamentos de Planejamento e Controladorias Corporativas:</b> Necessidade de parâmetros preditivos confiáveis de custos para elaboração de orçamentos anuais, reajustes contratuais com fornecedores e planejamento de estoques;</li>
        <li><b>Sociedade e Gestores de Políticas Públicas:</b> Beneficiários indiretos de estudos transparentes e reprodutíveis que analisam as pressões de custos sobre itens de consumo essencial (alimentação, energia e transporte).</li>
      </ul>
    </li>
  </ul>

  <h2>3.2 Descrição da Base de Dados</h2>
  <p>A base empírica foi coletada automaticamente da API do Sistema Gerenciador de Séries Temporais do Banco Central (SGS/BACEN). O painel compreende 174 observações mensais contínuas (frequência <i>Month Start</i> - MS), de março de 2012 a agosto de 2026.</p>
  <p>A variável dependente alvo ($y_t$) é o IPCA mensal (SGS código 4447). As 28 variáveis exógenas candidatas foram agrupadas em quatro categorias macroeconômicas:</p>
  <ul>
    <li><b>Índices de Preços e Desagregações Setoriais (11 variáveis):</b> Subíndices do IPCA (Alimentação, Transportes, Habitação, Saúde, Vestuário, Educação e Despesas Pessoais) e índices gerais (INPC, IGP-M, IGP-DI e IPC-BR);</li>
    <li><b>Setor Financeiro, Moeda e Câmbio (3 variáveis):</b> Taxa Selic Over, taxa de câmbio nominal PTAX (USDBRL) e reservas internacionais;</li>
    <li><b>Atividade Econômica e Mercado de Trabalho (7 variáveis):</b> PIB Mensal a preços correntes, taxa de desocupação (PNAD Contínua), salário mínimo nacional, estoques de empregos formais ativos do CAGED (Total, Agropecuária e Construção Civil) e produção física de ovos;</li>
    <li><b>Energia e Combustíveis (6 variáveis):</b> Refino de petróleo, consumo aparente de gasolina automotiva, consumo de óleo combustível e demanda faturada de energia elétrica (Comercial, Residencial e Total).</li>
  </ul>

  <h3>3.2.1 Delimitação Temporal e Justificativa Metodológica (2012 a 2026)</h3>
  <p>O marco temporal inicial em março de 2012 foi adotado devido a três fatores metodológicos fundamentados com o stakeholder economista:</p>
  <ul>
    <li><b>1. Transição da Medição do Desemprego:</b> Implantação da PNAD Contínua pelo IBGE em substituição à antiga PME, eliminando quebra estrutural severa nos dados de mercado de trabalho;</li>
    <li><b>2. Nova Ponderação da Cesta do IPCA:</b> Atualização dos pesos da cesta de consumo com base na POF 2008-2009;</li>
    <li><b>3. Painel Balanceado no SGS/BACEN:</b> Disponibilidade ininterrupta do painel balanceado de séries setoriais.</li>
  </ul>

  <h2>3.3 Análise Descritiva dos Dados</h2>
  <p>A análise descritiva investigou a dispersão, a assimetria e os valores extremos antes da modelagem preditiva. Para atender aos critérios formais de mineração de dados, foram caracterizados um atributo numérico contínuo e um atributo nominal institucionalmente fundamentado:</p>
  <ul>
    <li><b>1. Atributo Numérico Contínuo (IPCA):</b> Variação percentual mensal da inflação oficial (SGS 4447);</li>
    <li><b>2. Atributo Nominal Categórico (Regime de Inflação):</b> Discretização da série contínua em três classes balizadas pelas metas do CMN: Deflação (<i>IPCA &lt; 0,00%</i>), Meta / Estável (<i>0,00% &le; IPCA &le; 0,50%</i>) e Alta / Acima da Meta (<i>IPCA &gt; 0,50%</i>).</li>
  </ul>

  <h3>3.3.1 Distribuição de Frequências e Métricas Descritivas</h3>
  <p>A análise da amostra atualizada (174 meses contínuos) aponta a predominância de meses dentro da meta oficial, conforme demonstrado na Tabela 2.</p>

  <div class="tbl-title">Tabela 2 – Distribuição de Frequência do Atributo Nominal (Regime de Inflação)</div>
  <table>
    <thead>
      <tr>
        <th>Classe Nominal</th>
        <th>Faixa Paramétrica</th>
        <th>Freq. Absoluta (<i>f<sub>i</sub></i>)</th>
        <th>Freq. Relativa (%)</th>
        <th>Freq. Acumulada (<i>F<sub>i</sub></i>)</th>
        <th>Freq. Rel. Acum. (%)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><b>Deflação</b></td>
        <td style="text-align: center;">IPCA &lt; 0,00%</td>
        <td style="text-align: center;">27</td>
        <td style="text-align: center;">15,52%</td>
        <td style="text-align: center;">27</td>
        <td style="text-align: center;">15,52%</td>
      </tr>
      <tr>
        <td><b>Meta / Estável</b></td>
        <td style="text-align: center;">0,00% &le; IPCA &le; 0,50%</td>
        <td style="text-align: center;">77</td>
        <td style="text-align: center;">44,25%</td>
        <td style="text-align: center;">104</td>
        <td style="text-align: center;">59,77%</td>
      </tr>
      <tr>
        <td><b>Alta / Acima da Meta</b></td>
        <td style="text-align: center;">IPCA &gt; 0,50%</td>
        <td style="text-align: center;">70</td>
        <td style="text-align: center;">40,23%</td>
        <td style="text-align: center;">174</td>
        <td style="text-align: center;">100,00%</td>
      </tr>
      <tr style="font-weight: bold; background-color: #F2F4F7;">
        <td>Total Geral Amostral</td>
        <td style="text-align: center;">Horizonte 2012–2026</td>
        <td style="text-align: center;">174</td>
        <td style="text-align: center;">100,00%</td>
        <td style="text-align: center;">174</td>
        <td style="text-align: center;">100,00%</td>
      </tr>
    </tbody>
  </table>
  <div class="tbl-source">Fonte: Elaboração própria com base no SGS/BACEN (2026).</div>

  <p>Principais estimadores estatísticos do IPCA contínuo na amostra:</p>
  <ul>
    <li><b>Média e Mediana:</b> Média de 0,4324% ao mês e mediana de 0,4150% ao mês;</li>
    <li><b>Dispersão:</b> Desvio padrão amostral de 0,4719% e variância de 0,2226;</li>
    <li><b>Assimetria e Curtose:</b> Assimetria positiva (+0,5287), acusando cauda direita alongada por choques inflacionários, e curtose de +0,3736;</li>
    <li><b>Valores Extremos:</b> Mínimo histórico de -0,7400% (junho/2023) e máximo de +1,9500% (dezembro/2019);</li>
    <li><b>Quartis e Intervalo Interquartílico:</b> <i>Q</i><sub>1</sub> = 0,0800%, <i>Q</i><sub>3</sub> = 0,6775% e <i>IQR</i> = 0,5975 p.p.</li>
  </ul>

  <h3>3.3.2 Análise Visual: Histograma, Boxplot e Gráficos de Dispersão</h3>
  <p>A caracterização visual dos dados foi conduzida através de gráficos gerados a partir do histórico consolidado:</p>

  <div class="figura-container">
    <img src="{b64_fig1}" alt="Figura 1 - Histograma IPCA" />
    <div class="legenda">Figura 1 – Histograma e Densidade Empírica (KDE) do IPCA (2012 a 2026)</div>
  </div>
  <p>A Figura 1 confirma que a distribuição da inflação concentra-se entre 0,10% e 0,60% ao mês. A proximidade entre média e mediana reforça a regularidade central, enquanto a assimetria positiva (+0,53) demonstra que choques inflacionários são mais acentuados do que quedas de preço.</p>

  <div class="figura-container">
    <img src="{b64_fig2}" alt="Figura 2 - Boxplot IPCA" />
    <div class="legenda">Figura 2 – Diagrama de Caixa (Boxplot) do IPCA: Amostra Global e por Regimes de Inflação</div>
  </div>
  <p>O Boxplot univariado na Figura 2 identifica 5 outliers pelo critério de Tukey (IQR): dezembro/2019 (+1,95%), outubro/2020 (+1,72%), novembro/2020 (+1,61%), dezembro/2020 (+1,58%) e dezembro/2021 (+1,58%), decorrentes de choques em carnes e restrições de cadeias de suprimentos globais. A dispersão na classe "Alta" é muito mais ampla do que na classe "Meta", justificando a modelagem não linear dos resíduos.</p>

  <div class="figura-container">
    <img src="{b64_fig3}" alt="Figura 3 - Dispersão IPCA vs Câmbio" />
    <div class="legenda">Figura 3 – Gráfico de Dispersão entre IPCA e Taxa de Câmbio (USDBRL) por Regime Nominal</div>
  </div>
  <p>O gráfico de dispersão da Figura 3 evidencia a relação positiva entre desvalorização cambial e inflação (mecanismo de pass-through cambial). À medida que a cotação do dólar sobe, a frequência de meses no regime de "Alta" aumenta perceptivelmente.</p>

  <div class="figura-container">
    <img src="{b64_fig4}" alt="Figura 4 - Proporção de Regimes" />
    <div class="legenda">Figura 4 – Proporção Percentual dos Regimes Nominais de Inflação (N = 174 meses)</div>
  </div>
  <p>A Figura 4 sintetiza a distribuição amostral: 44,25% dos meses situaram-se na meta, 40,23% em patamares elevados e 15,52% em deflação (provocada por desonerações tributárias temporárias e contrações severas de demanda).</p>

  <h3>3.3.3 Governança, Integridade e Requisitos de Qualidade</h3>
  <p>O tratamento dos dados segue rigorosamente a Lei Geral de Proteção de Dados Pessoais (LGPD – Lei nº 13.709/2018). As séries temporais empregadas são dados macroeconômicos públicos e agregados (SGS/BACEN, IBGE, FGV e Ministério do Trabalho), sem identificadores individuais. Sob a perspectiva de engenharia de dados, garantimos: (i) prevenção estrita de vazamento prospectivo (<i>lookahead bias</i>); (ii) completude amostral de 100% sem lacunas no período de 2012 a 2026; e (iii) reprodutibilidade científica por meio de scripts Python automatizados.</p>

  <h2>3.4 Pré-processamento dos Dados</h2>
  <p>O pré-processamento de dados constitui a etapa culminante da presente entrega. Nesta fase, as séries temporais brutas foram submetidas a rotinas sistemáticas de engenharia de dados para transformá-las em um painel estruturado, consistente e livre de inconsistências, sem qualquer vazamento de dados futuros.</p>

  <h3>3.4.1 Procedimentos de Limpeza e Saneamento de Dados (Data Cleaning)</h3>
  <p>O pipeline de limpeza executado compreendeu quatro procedimentos principais:</p>
  <ul>
    <li><b>1. Sincronização Cronológica:</b> Séries divulgadas em periodicidade diária no mercado financeiro (taxa de câmbio nominal PTAX e taxa Selic Over) foram convertidas para médias mensais de dias úteis e sincronizadas sob frequência contínua Month Start (MS) de março de 2012 a agosto de 2026;</li>
    <li><b>2. Tratamento de Zeros Estruturais:</b> Em séries contínuas de fluxos e estoques físicos (refino de petróleo, consumo de combustíveis, demanda de energia e estoques de emprego do CAGED), zeros espúrios gerados por atrasos de apuração de órgãos governamentais foram identificados e substituídos por valores nulos (<code>NaN</code>);</li>
    <li><b>3. Sanitização Numérica:</b> Verificação sistemática contra potenciais valores infinitos ($\pm\infty$) ou divisões por zero, assegurando que todas as entradas pertencem ao espaço numérico real Float64;</li>
    <li><b>4. Imputação Temporal de Dados Ausentes:</b> Valores faltantes pontuais em séries mensais foram tratados via interpolação linear temporal contínua indexada pelo calendário (<code>interpolate(method='time')</code>). A preservação da ordem cronológica garante a integridade histórica dos dados sem distorções.</li>
  </ul>

  <h3>3.4.2 Técnicas de Redução de Dados e Engenharia de Atributos</h3>
  <ul>
    <li><b>1. Redução Amostral Estrutural (Truncamento pós-2012):</b> Conforme validado junto ao consultor de domínio, descartaram-se os dados anteriores a março de 2012 para eliminar quebras estruturais metodológicas severas (transição da PME para PNAD Contínua e revisão dos pesos da cesta do IPCA pela POF 2008-2009);</li>
    <li><b>2. Discretização do Atributo Nominal:</b> Construção da variável categórica "Regime de Inflação" com base nas faixas institucionais do CMN, permitindo a segmentação exploratória de períodos de normalidade, estresse e deflação;</li>
    <li><b>3. Codificação de Sazonalidade Harmônica:</b> Criação dos atributos sazonais $mes\_sin = \sin(2\pi m / 12)$ e $mes\_cos = \cos(2\pi m / 12)$, viabilizando a captura contínua e suave de ciclos anuais sem o custo de inflar a dimensionalidade com 11 variáveis dummy binárias.</li>
  </ul>

  <h3>3.4.3 Dicionário de Dados da Base Consolidada Pré-Processada</h3>
  <p>Como resultado final de todo o fluxo de coleta, higienização e saneamento, a Tabela 3 consolida o Dicionário de Dados da base pré-processada, especificando para cada um dos 31 atributos o seu código de origem, tipo de dado, tratamento recebido no pré-processamento, pilar macroeconômico e papel de negócio validado pelo Prof. Guilherme Martins.</p>

  <div class="tbl-title">Tabela 3 – Dicionário de Dados da Base Consolidada Pré-Processada (174 Meses, 2012–2026)</div>
  <table>
    <thead>
      <tr>
        <th style="width: 18%;">Atributo</th>
        <th style="width: 14%;">Código / Fonte</th>
        <th style="width: 13%;">Tipo / Unidade</th>
        <th style="width: 20%;">Tratamento no Pré-processamento</th>
        <th style="width: 15%;">Pilar Econômico</th>
        <th style="width: 20%;">Papel / Descrição Econômica</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><b>IPCA</b></td><td>SGS 4447 (IBGE)</td><td>Float64 (% a.m.)</td><td>Interpolação de nulos; alinhamento Month-Start (MS)</td><td>Preços Setoriais</td><td>Variável dependente alvo (Target $y_t$) - Inflação oficial sob regime de metas.</td></tr>
      <tr><td><b>IPCA_Transportes</b></td><td>SGS 1639 (IBGE)</td><td>Float64 (% a.m.)</td><td>Sincronização MS; tratamento de nulos via interpolação</td><td>Preços Setoriais</td><td>Covariável exógena - Choques de preços de combustíveis e tarifas de mobilidade.</td></tr>
      <tr><td><b>IPCA_Alimentação_bebidas</b></td><td>SGS 1635 (IBGE)</td><td>Float64 (% a.m.)</td><td>Sincronização MS; tratamento de nulos via interpolação</td><td>Preços Setoriais</td><td>Covariável exógena - Choques climáticos e safras no consumo domiciliar.</td></tr>
      <tr><td><b>INPC_Habitação</b></td><td>SGS 1636 (IBGE)</td><td>Float64 (% a.m.)</td><td>Sincronização MS; tratamento de nulos via interpolação</td><td>Preços Setoriais</td><td>Covariável exógena - Pressões de aluguel e tarifas de energia residencial.</td></tr>
      <tr><td><b>IPCA_Saúde_cuidados_pessoais</b></td><td>SGS 1641 (IBGE)</td><td>Float64 (% a.m.)</td><td>Sincronização MS; tratamento de nulos via interpolação</td><td>Preços Setoriais</td><td>Covariável exógena - Repasse de custos médicos e planos de saúde regulados.</td></tr>
      <tr><td><b>IPCA_Vestuário</b></td><td>SGS 1638 (IBGE)</td><td>Float64 (% a.m.)</td><td>Sincronização MS; tratamento de nulos via interpolação</td><td>Preços Setoriais</td><td>Covariável exógena - Sazonalidade de coleções e liquidações do varejo.</td></tr>
      <tr><td><b>IPCA_Educação</b></td><td>SGS 1643 (IBGE)</td><td>Float64 (% a.m.)</td><td>Sincronização MS; tratamento de nulos via interpolação</td><td>Preços Setoriais</td><td>Covariável exógena - Reajustes concentrados em início de ano letivo.</td></tr>
      <tr><td><b>IPCA_Despesas_Pessoais</b></td><td>SGS 1642 (IBGE)</td><td>Float64 (% a.m.)</td><td>Sincronização MS; tratamento de nulos via interpolação</td><td>Preços Setoriais</td><td>Covariável exógena - Sensibilidade de demanda de serviços recreativos e pessoais.</td></tr>
      <tr><td><b>USDBRL (Câmbio PTAX)</b></td><td>SGS 3696 (BACEN)</td><td>Float64 (R$/US$)</td><td>Conversão diária para média mensal de dias úteis; MS</td><td>Câmbio / Finanças</td><td>Covariável exógena - Mecanismo de pass-through cambial e importações.</td></tr>
      <tr><td><b>SELIC</b></td><td>SGS 4390 (BACEN)</td><td>Float64 (% a.m.)</td><td>Conversão de taxa diária para média mensal; MS</td><td>Câmbio / Finanças</td><td>Covariável exógena - Taxa básica de juros da política monetária do COPOM.</td></tr>
      <tr><td><b>Reservas_Internacionais</b></td><td>SGS 3546 (BACEN)</td><td>Float64 (US$ Milhões)</td><td>Alinhamento mensal MS; saneamento de lacunas</td><td>Câmbio / Finanças</td><td>Covariável exógena - Liquidez externa e blindagem a choques globais.</td></tr>
      <tr><td><b>INPC</b></td><td>SGS 188 (IBGE)</td><td>Float64 (% a.m.)</td><td>Sincronização MS; interpolação linear de nulos</td><td>Preços Setoriais</td><td>Covariável exógena - Inflação incidente em famílias de 1 a 5 salários mínimos.</td></tr>
      <tr><td><b>IGP_M</b></td><td>SGS 189 (FGV)</td><td>Float64 (% a.m.)</td><td>Sincronização MS; alinhamento de competência</td><td>Preços Setoriais</td><td>Covariável exógena - Indicador antecedente de custos no atacado (FGV).</td></tr>
      <tr><td><b>IGP_DI</b></td><td>SGS 190 (FGV)</td><td>Float64 (% a.m.)</td><td>Sincronização MS; verificação de integridade</td><td>Preços Setoriais</td><td>Covariável exógena - Preços ao produtor e insumos de disponibilidade interna.</td></tr>
      <tr><td><b>IPC_BR</b></td><td>SGS 191 (FGV)</td><td>Float64 (% a.m.)</td><td>Sincronização MS; saneamento de inconsistências</td><td>Preços Setoriais</td><td>Covariável exógena - Índice de preços ao consumidor abrangente da FGV.</td></tr>
      <tr><td><b>PIB_Mensal</b></td><td>SGS 4380 (BACEN)</td><td>Float64 (R$ Milhões)</td><td>Tratamento de atrasos de divulgação; sincronização MS</td><td>Atividade Econômica</td><td>Covariável exógena - Proxy de nível de atividade econômica mensal e hiato.</td></tr>
      <tr><td><b>Desemprego (PNAD)</b></td><td>SGS 24369 (IBGE)</td><td>Float64 (% da PEA)</td><td>Truncamento pós-2012; interpolação de quebras</td><td>Mercado de Trabalho</td><td>Covariável exógena - Dinâmica da desocupação formal (Curva de Phillips).</td></tr>
      <tr><td><b>Salario_Minimo</b></td><td>SGS 1619 (Governo)</td><td>Float64 (R$ correntes)</td><td>Sincronização MS; preservação de reajustes federais anuais</td><td>Mercado de Trabalho</td><td>Covariável exógena - Custos de contratação básica no setor terciário.</td></tr>
      <tr><td><b>Estoque_Empregos_Total</b></td><td>SGS 28763 (CAGED)</td><td>Float64 (Mil vínculos)</td><td>Zeros contábeis substituídos por NaN; interpolação</td><td>Mercado de Trabalho</td><td>Covariável exógena - Saldo mensal de geração de emprego formal no Brasil.</td></tr>
      <tr><td><b>Estoque_Agropecuária</b></td><td>SGS 28764 (CAGED)</td><td>Float64 (Mil vínculos)</td><td>Substituição de zeros por NaN; sincronização contínua</td><td>Mercado de Trabalho</td><td>Covariável exógena - Dinâmica do emprego rural e safras do agronegócio.</td></tr>
      <tr><td><b>Estoque_Construção</b></td><td>SGS 28770 (CAGED)</td><td>Float64 (Mil vínculos)</td><td>Alinhamento cronológico; saneamento de inconsistências</td><td>Mercado de Trabalho</td><td>Covariável exógena - Nível de atividade e investimentos na construção civil.</td></tr>
      <tr><td><b>Qte_Ovos</b></td><td>SGS 1310 (IBGE)</td><td>Float64 (Mil dúzias)</td><td>Interpolação de atrasos; alinhamento de frequência MS</td><td>Atividade Econômica</td><td>Covariável exógena - Proxy física da oferta agropecuária de ciclo rápido.</td></tr>
      <tr><td><b>Produção_Derivados_Petróleo</b></td><td>SGS 1391 (ANP)</td><td>Float64 (Mil m³)</td><td>Alinhamento MS; interpolação linear de lacunas</td><td>Energia / Combustíveis</td><td>Covariável exógena - Volume de refino de petróleo e oferta energética.</td></tr>
      <tr><td><b>Consumo_Gasolina</b></td><td>SGS 1393 (ANP)</td><td>Float64 (m³)</td><td>Sincronização MS; zeros de atraso tratados como NaN</td><td>Energia / Combustíveis</td><td>Covariável exógena - Consumo automotivo e pressão de curto prazo em transporte.</td></tr>
      <tr><td><b>Consumo_Óleo_Combustível</b></td><td>SGS 1395 (ANP)</td><td>Float64 (t)</td><td>Alinhamento temporal e interpolação de competência</td><td>Energia / Combustíveis</td><td>Covariável exógena - Indicador logístico do transporte rodoviário pesado.</td></tr>
      <tr><td><b>Consumo_Energia_Comercial</b></td><td>SGS 1402 (EPE)</td><td>Float64 (MWh)</td><td>Sincronização MS; zeros tratados como NaN</td><td>Energia / Combustíveis</td><td>Covariável exógena - Carga elétrica no comércio (termômetro em tempo real).</td></tr>
      <tr><td><b>Consumo_Energia_Residencial</b></td><td>SGS 1403 (EPE)</td><td>Float64 (MWh)</td><td>Alinhamento MS; interpolação temporal contínua</td><td>Energia / Combustíveis</td><td>Covariável exógena - Padrão de consumo elétrico das famílias brasileiras.</td></tr>
      <tr><td><b>Consumo_Energia_Total</b></td><td>SGS 1406 (EPE)</td><td>Float64 (MWh)</td><td>Sincronização mensal MS; verificação de integridade</td><td>Energia / Combustíveis</td><td>Covariável exógena - Demanda física global de energia elétrica produtiva.</td></tr>
      <tr><td><b>Regime de Inflação</b></td><td>IBGE / CMN</td><td>Categórico Nominal</td><td>Discretização paramétrica: Deflação, Meta e Alta</td><td>Governança / CMN</td><td>Atributo nominal derivado - Caracterização qualitativa da trajetória.</td></tr>
      <tr><td><b>mes_sin</b></td><td>Engenharia Temporal</td><td>Float64 (Adimensional)</td><td>Harmônica periódica senoidal: $\sin(2\pi m / 12)$</td><td>Sazonalidade</td><td>Covariável sazonal contínua - Captura de ciclos periódicos anuais.</td></tr>
      <tr><td><b>mes_cos</b></td><td>Engenharia Temporal</td><td>Float64 (Adimensional)</td><td>Harmônica periódica cossenoidal: $\cos(2\pi m / 12)$</td><td>Sazonalidade</td><td>Covariável sazonal contínua - Captura de ciclos periódicos anuais.</td></tr>
    </tbody>
  </table>
  <div class="tbl-source">Fonte: Elaboração própria com base no pipeline computacional desenvolvido e validado com os stakeholders (2026).</div>

  <hr style="border: 0; border-top: 1px solid #D1D5DB; margin: 24px 0;">

  <h1>Referências Bibliográficas</h1>

  <div class="ref-list">
    <div class="ref-item">[1] BOX, G. E.; JENKINS, G. M.; REINSEL, G. C.; LJUNG, G. M. <i>Time Series Analysis: Forecasting and Control</i>. 5. ed. Hoboken: John Wiley & Sons, 2015.</div>
    <div class="ref-item">[2] BANCO CENTRAL DO BRASIL (BACEN). <i>Sistema Gerenciador de Séries Temporais (SGS)</i>. Disponível em: &lt;https://www3.bcb.gov.br/sgspub/&gt;. Acesso em: 16 set. 2026.</div>
    <div class="ref-item">[3] BANCO CENTRAL DO BRASIL (BACEN). <i>Relatório de Inflação</i>. v. 26, n. 2. Brasília: Banco Central do Brasil, 2024.</div>
    <div class="ref-item">[4] BLANCHARD, O. <i>Macroeconomia</i>. 7. ed. São Paulo: Pearson, 2017.</div>
    <div class="ref-item">[5] BRESSER-PEREIRA, L. C.; NAKANO, Y. <i>A Teoria da Inflação Inercial</i>. São Paulo: Brasiliense, 1984.</div>
    <div class="ref-item">[6] GARCIA, M. G.; MEDEIROS, M. C.; VASCONCELOS, G. F. Real-time inflation forecasting with high-dimensional data: the case of Brazil. <i>International Journal of Forecasting</i>, v. 33, n. 3, p. 679–693, 2017.</div>
    <div class="ref-item">[7] HASTIE, T.; TIBSHIRANI, R.; FRIEDMAN, J. <i>The Elements of Statistical Learning: Data Mining, Inference, and Prediction</i>. 2. ed. New York: Springer, 2009.</div>
    <div class="ref-item">[8] HOLLAND, J. H. <i>Adaptation in Natural and Artificial Systems: An Introductory Analysis with Applications to Biology, Control, and Artificial Intelligence</i>. Cambridge: MIT Press, 1992.</div>
    <div class="ref-item">[9] HYNDMAN, R. J.; ATHANASOPOULOS, G. <i>Forecasting: Principles and Practice</i>. 3. ed. Melbourne: OTexts, 2021.</div>
    <div class="ref-item">[10] INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA (IBGE). <i>Sistema Nacional de Índices de Preços ao Consumidor (SNIPC): Metodologia do IPCA e INPC</i>. Rio de Janeiro: IBGE, 2020.</div>
    <div class="ref-item">[11] KENNEDY, J.; EBERHART, R. Particle swarm optimization. In: <i>Proceedings of ICNN'95 - International Conference on Neural Networks</i>, v. 4, p. 1942–1948, 1995.</div>
    <div class="ref-item">[12] KHANDANI, A. E.; KIM, A. J.; LO, A. W. Consumer credit-risk models via machine-learning algorithms. <i>Journal of Banking & Finance</i>, v. 34, n. 11, p. 2767–2787, 2010.</div>
    <div class="ref-item">[13] MANKIW, N. G. <i>Macroeconomia</i>. 10. ed. Rio de Janeiro: LTC, 2021.</div>
    <div class="ref-item">[14] MEDEIROS, M. C.; VASCONCELOS, G. F.; VEIGA, Á.; ZILBERMAN, E. Forecasting inflation in a data-rich environment: the benefits of machine learning methods. <i>Journal of Business & Economic Statistics</i>, v. 39, n. 1, p. 98–119, 2021.</div>
    <div class="ref-item">[15] PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. <i>Journal of Machine Learning Research</i>, v. 12, p. 2825–2830, 2011.</div>
    <div class="ref-item">[16] SIMONSEN, M. H. <i>30 Anos de Indexação</i>. Rio de Janeiro: Editora FGV, 1995.</div>
    <div class="ref-item">[17] TAYLOR, J. B. Discretion versus policy rules in practice. <i>Carnegie-Rochester Conference Series on Public Policy</i>, v. 39, p. 195–214, 1993.</div>
    <div class="ref-item">[18] ZHANG, G. P. Time series forecasting using a hybrid ARIMA and neural network model. <i>Neurocomputing</i>, v. 50, p. 159–175, 2003.</div>
  </div>

</body>
</html>
"""

# Salvar HTML temporário para compilação PDF
html_path = os.path.join(DIR_ARTIGO, 'Artigo_Previsao_Inflacao_print.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

pdf_artigo = os.path.join(DIR_ARTIGO, 'Artigo_Previsao_Inflacao.pdf')
pdf_entrega = os.path.join(BASE_DIR, 'Entrega_Classroom', '3_Artigo_Completo', 'Artigo_Previsao_Inflacao.pdf')

chrome_cmd = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '--headless',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    f'--print-to-pdf={pdf_artigo}',
    html_path
]

print("Compilando Artigo em PDF de alta resolução via Chrome Engine...")
res = subprocess.run(chrome_cmd, capture_output=True, text=True)
if res.returncode == 0 and os.path.exists(pdf_artigo):
    print(f"PDF Principal gerado com sucesso: {pdf_artigo} ({os.path.getsize(pdf_artigo)} bytes)")
    import shutil
    shutil.copyfile(pdf_artigo, pdf_entrega)
    print(f"PDF copiado para Entrega Classroom: {pdf_entrega}")
else:
    print("Erro na geração do PDF:", res.stderr)

# Limpar HTML temporário
if os.path.exists(html_path):
    os.remove(html_path)
