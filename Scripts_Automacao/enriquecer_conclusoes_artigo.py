import re, os, shutil, zipfile

artigo_path = 'Artigo/Artigo_Previsao_Inflacao.md'

with open(artigo_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Corrigir tabs indesejados antes de ext{...}
text = text.replace('\text', '\\text')
# Se ainda restaram tabs literais seguidos de ext{
text = re.sub(r'\text\{', r'\\text{', text)

# 2. Enriquecer Seção 4.1.1 (Conclusão da Camada 1)
conclusao_camada_1 = """#### Conclusão da Camada 1: Reconstrução Não Supervisionada do Calendário Institucional e Deslocamento em Bloco de Educação
A análise detalhada da Camada 1 permite estabelecer três conclusões estruturais fundamentais:
1. **Reconstrução Não Supervisionada do Calendário:** O algoritmo de Ward agrupou a economia sem qualquer informação prévia de datas cronológicas. Ao alimentar o modelo apenas com as variações dos 7 subcomponentes setoriais, o método foi capaz de reconstruir autonomamente o calendário agrícola e regulatório brasileiro, comprovando que a inflação ao consumidor é governada por forças institucionais e biológicas rígidas.
2. **O Choque Assimétrico de Educação e o Deslocamento em Bloco:** O grupo *Educação* possui média histórica global de +0,52% ao mês e desvio-padrão de 1,38%. No Cluster Sazonal 3 (Fevereiro), a taxa média salta para impressionantes **+5,12% ao mês** (mediana de +5,31%), operando em um $Z$-Score médio de **+3,34 desvios-padrão** acima da média histórica. A dispersão desse grupo apresenta sobreposição nula (*zero overlap*) com o restante do ano (cujo mínimo histórico em fevereiro é +3,53%, patamar nunca atingido nos outros 11 meses). No cálculo da distância de Ward, apenas a dimensão educacional adiciona $(3,34 - (-0,25))^2 \approx 12,89$ pontos de dissimilaridade, justificando geometricamente por que o Ramo Laranja se isola na altura máxima da árvore hierárquica (distância 17,6).
3. **Mapeamento das Quatro Estações Inflacionárias Nacionais:** O dendrograma comprova que o ano econômico divide-se em: (i) *Choque Educacional* (Fevereiro); (ii) *Reajuste Farmacêutico da CMED/ANVISA* (Abril e Maio, com Saúde em $+1,15\sigma$); (iii) *Alívio de Safra Agrícola* (Julho a Outubro, com Alimentação em $-0,58\sigma$); e (iv) *Pressões de Demanda e Tarifárias* (Novembro a Março, puxado por 13º salário, festas, vestuário e transportes urbanos)."""

# Substituir o final da 4.1.1
alvo_camada_1 = "e reajustes tarifários municipais de início de ano (IPVA e transporte urbano)."
pos_c1 = text.find(alvo_camada_1)
if pos_c1 != -1:
    pos_fim_c1 = pos_c1 + len(alvo_camada_1)
    text = text[:pos_fim_c1] + '\n\n' + conclusao_camada_1 + text[pos_fim_c1:]
    print('Conclusão da Camada 1 adicionada ao artigo!')
else:
    print('Aviso: Alvo da Camada 1 não localizado exatamente.')

# 3. Enriquecer Seção 4.1.2 (Conclusão da Camada 2)
conclusao_camada_2 = """#### Conclusão da Camada 2: Não Linearidade da Trinca Inflação-Juros-Ouro e Identificação de Regimes Macroeconômicos
A investigação tridimensional da co-movimentação entre IPCA, variação da taxa SELIC e retorno do ouro físico em moeda nacional consolida conclusões econômicas cruciais:
1. **Ouro e Política Monetária como Forças Antagônicas:** No Regime 0 (*Aperto Hawkish* – 53 meses), quando a autoridade monetária eleva ativamente a SELIC ($\Delta\text{SELIC} = +0,064$ p.p./mês) para conter a inflação, o custo de oportunidade do capital aumenta e o Real tende a se valorizar frente ao dólar. Como consequência direta, o retorno do ouro em moeda nacional sofre severa contração média de **$-3,32\%$ ao mês** (com meses registrando quedas de até $-13\%$). Juros em alta e combate à inflação enfraquecem a demanda especulativa por metais preciosos.
2. **O Ouro como Cobertura em Momentos de Tensão Cambial:** No Regime 1 (*Voo para a Qualidade / Safe Haven* – 67 meses), mesmo com inflação moderada (0,283%), a desvalorização cambial (dólar médio a R$ 4,16) e incertezas globais empurram o retorno do ouro em reais para um ganho médio de **$+5,22\%$ ao mês** (atingindo picos de até $+18\%$). O ouro em moeda nacional opera com primazia como ativo de proteção patrimonial cambial antes mesmo que o repasse de custos (*pass-through*) atinja as gôndolas do varejo.
3. **Rigidez Monetária e Pico Histórico do Juro Real:** No Regime 2 (*Desinflação Dovish* – 23 meses), a taxa média de deflação ($-0,067\%$) abre espaço para fortes cortes de juros ($\Delta\text{SELIC} = -0,117$ p.p./mês). Contudo, pela dinâmica inercial da política monetária, a SELIC nominal recua mais lentamente do que os preços desabam, fazendo com que o **Juro Real atinja seu recorde histórico amostral de +0,93% ao mês** (mais de 11% ao ano em termos reais).
4. **Detecção do Banco Central "Atrás da Curva":** No Regime 3 (*Choque Inflacionário Severo* – 30 meses), choques severos de oferta e desancoragem empurram o IPCA para a média de **+1,04% ao mês** (variando entre 0,8% e 2,0%). Como a autoridade monetária reage com defasagem temporal, o **juro real mergulha no terreno negativo ($-0,33\%$ a.m.)**, estimulando a fuga para ativos reais (ouro valorizando $+2,37\%$). Esse regime fornece um sinal preditivo de alerta máximo para os modelos de machine learning."""

alvo_camada_2 = "atestando a corrida por ativos reais em cenários de estagflação."
pos_c2 = text.find(alvo_camada_2)
if pos_c2 != -1:
    pos_fim_c2 = pos_c2 + len(alvo_camada_2)
    text = text[:pos_fim_c2] + '\n\n' + conclusao_camada_2 + text[pos_fim_c2:]
    print('Conclusão da Camada 2 adicionada ao artigo!')
else:
    print('Aviso: Alvo da Camada 2 não localizado exatamente.')

# 4. Enriquecer Seção 4.1.3 (Conclusão da Camada 3)
conclusao_camada_3 = """#### Conclusão da Camada 3: Rejeição da Independência e Modulação Macroeconômica dos Ciclos Biológicos
O cruzamento das duas partições não supervisionadas e a aplicação do teste de hipótese revelam conclusões metodológicas que transformam a modelagem preditiva:
1. **Rejeição Estrita da Independência Estocástica:** O Teste Qui-Quadrado de Pearson ($\chi^2 = 34,73, p = 0,000067$) refuta categoricamente a hipótese nula de que a sazonalidade e os regimes macroeconômicos operam de forma isolada. A probabilidade de essa interação decorrer de mero acaso estatístico é inferior a 0,01%.
2. **A Safra de Alimentos como Condição Necessária para Cortes de Juros:** Dos 23 meses em que o Brasil vivenciou o Regime 2 (*Desinflação e Afrouxamento Monetário*), **15 meses (65,2%) concentraram-se exclusivamente na janela da Safra Agrícola** (Julho a Outubro). Isso comprova econometricamente que o COPOM depende da descompressão biológica dos alimentos para viabilizar ciclos de redução sustentada da taxa SELIC sem gerar pressões secundárias de demanda.
3. **A Supressão da Safra por Choques Globais de Custos:** No Regime 3 (*Choque Inflacionário Severo*), apenas 3 meses (10%) coincidiram com a safra agrícola, enquanto 70% (21 meses) ocorreram no período de início/fim de ano. Esse achado demonstra que episódios agudos de estagflação internacional e disparada do ouro possuem magnitude suficiente para anular o alívio sazonal biológico dos alimentos.
4. **Implicação Arquitetural para os Modelos Preditivos:** Modelos de séries temporais ingênuos que se apoiam apenas no calendário histórico esperam deflação todo mês de agosto. No entanto, ao acoplar os rótulos de regime da Camada 2 como variáveis de entrada categóricas (*one-hot encoded*) nos regressores `ARIMAX` e `Random Forest`, o sistema preditivo identifica preventivamente que, se a economia estiver no Regime 3 (choque de ouro e juro real negativo), a deflação esperada de agosto não ocorrerá, prevenindo erros drásticos de projeção."""

alvo_camada_3 = "anulam os benefícios sazonais biológicos de redução de preços de alimentos."
pos_c3 = text.find(alvo_camada_3)
if pos_c3 != -1:
    pos_fim_c3 = pos_c3 + len(alvo_camada_3)
    text = text[:pos_fim_c3] + '\n\n' + conclusao_camada_3 + text[pos_fim_c3:]
    print('Conclusão da Camada 3 adicionada ao artigo!')
else:
    print('Aviso: Alvo da Camada 3 não localizado exatamente.')

# Salvar artigo markdown atualizado
with open(artigo_path, 'w', encoding='utf-8') as f:
    f.write(text)
print('Artigo salvo com sucesso!')

# Sincronizar com Entrega_Classroom
shutil.copyfile(artigo_path, 'Entrega_Classroom/3_Artigo_Completo/Artigo_Previsao_Inflacao.md')
print('Artigo sincronizado para Entrega_Classroom/3_Artigo_Completo/Artigo_Previsao_Inflacao.md')
