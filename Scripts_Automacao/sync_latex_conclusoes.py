import re, os, zipfile, shutil

tex_path = 'Artigo/Template_REPA_LaTeX/main.tex'
with open(tex_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Inserir conclusões detalhadas nas subseções do LaTeX
conc_1_tex = r"""\paragraph{Conclusão da Camada 1: Reconstrução Não Supervisionada do Calendário Institucional}
O algoritmo de Ward reconstruiu autonomamente o calendário agrícola e regulatório brasileiro sem receber rótulos de data. O grupo Educação apresenta média histórica de +0,52\% ao mês e salta para impressionantes \textbf{+5,12\% ao mês} em Fevereiro ($Z$-Score médio de \textbf{+3,34 desvios-padrão}), com sobreposição nula frente aos demais meses (mínimo de +3,53\% em fevereiro, valor nunca atingido no restante do ano). A distância euclidiana ao quadrado de 12,89 pontos na dimensão educacional explica por que o Ramo Laranja se isola na altura máxima da árvore hierárquica (distância 17,6)."""

conc_2_tex = r"""\paragraph{Conclusão da Camada 2: Não Linearidade da Trinca Inflação-Juros-Ouro e Identificação de Regimes}
O agrupamento tridimensional revela que Ouro e Selic operam como forças opostas no Brasil: no Regime 0 (Aperto Hawkish), a elevação de juros ($\Delta\text{SELIC} = +0,064$ p.p.) induz contração média de \textbf{-3,32\% no ouro em Reais}. No Regime 1 (Voo para Qualidade), o ouro dispara \textbf{+5,22\% ao mês} em resposta a tensões cambiais antes do repasse aos preços. No Regime 2 (Desinflação Dovish), a deflação ($-0,067\%$) associada à queda de juros eleva o \textbf{Juro Real ao recorde histórico de +0,93\% ao mês}. Por fim, o Regime 3 (Choque Severo, IPCA de +1,04\%) flagra a política monetária defasada, empurrando o juro real para o campo negativo ($-0,33\%$) e estimulando a fuga para o ouro (+2,37\%)."""

conc_3_tex = r"""\paragraph{Conclusão da Camada 3: Rejeição da Independência e Modulação Macroeconômica da Safra}
O Teste Qui-Quadrado de Pearson ($\chi^2 = 34,73, p = 0,000067$) refuta a independência entre sazonalidade e choques macroeconômicos. Evidencia-se que \textbf{65,2\% dos episódios de afrouxamento monetário sustentado (Regime 2)} dependem da descompressão de preços da Safra Agrícola de inverno. Em contrapartida, sob Choques Inflacionários Severos (Regime 3), a safra é anulada (apenas 10\% de incidência), demonstrando que pressões externas severas de custos e ouro suprimem o alívio sazonal biológico dos alimentos."""

# Inserções no LaTeX
if 'Conclusão da Camada 1' not in text:
    p1 = text.find(r'\subsubsection{Camada 2: Regimes Macroeconômicos com Ouro e Taxa de Juros}')
    text = text[:p1] + conc_1_tex + '\n\n' + text[p1:]

if 'Conclusão da Camada 2' not in text:
    p2 = text.find(r'\subsubsection{Camada 3: Interação Cruzada e Teste de Independência}')
    text = text[:p2] + conc_2_tex + '\n\n' + text[p2:]

if 'Conclusão da Camada 3' not in text:
    p3 = text.find(r'\subsection{Considerações Finais e Trabalhos Futuros}')
    text = text[:p3] + conc_3_tex + '\n\n' + text[p3:]

with open(tex_path, 'w', encoding='utf-8') as f:
    f.write(text)
print('LaTeX main.tex enriquecido com as conclusões!')

# Reempacotar zip
zip_name = 'Artigo/Template_REPA_2026_2_Artigo_Previsao_Inflacao.zip'
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('Artigo/Template_REPA_LaTeX'):
        if not any(f.endswith('.bak') for f in files):
            for file in files:
                abs_f = os.path.join(root, file)
                rel_f = os.path.relpath(abs_f, 'Artigo/Template_REPA_LaTeX')
                zipf.write(abs_f, rel_f)
print(f'Pacote ZIP atualizado: {zip_name}')
shutil.copyfile(zip_name, 'Entrega_Classroom/3_Artigo_Completo/Template_REPA_2026_2_Artigo_Previsao_Inflacao.zip')
print('ZIP copiado para Entrega_Classroom/3_Artigo_Completo/')
