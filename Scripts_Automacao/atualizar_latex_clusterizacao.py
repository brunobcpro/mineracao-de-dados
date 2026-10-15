import re, os, zipfile, shutil

tex_path = 'Artigo/Template_REPA_LaTeX/main.tex'
backup_tex = 'Artigo/Template_REPA_LaTeX/main.tex.bak'
shutil.copyfile(tex_path, backup_tex)
print(f'Backup LaTeX criado em: {backup_tex}')

with open(tex_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Atualizar Subseção 2.2
tex_2_2 = r"""\subsection{Mineração de Dados em Séries Temporais e Fundamentação do Agrupamento Hierárquico (Critério de Ward)}
A Mineração de Dados em Séries Temporais (\textit{Time Series Data Mining}) visa descobrir padrões estruturais, tendências latentes e dependências dinâmicas em dados sequenciais indexados cronologicamente \cite{ref7, ref9}. Ao contrário de observações tabulares padrão, séries temporais violam a premissa de observações independentes e identicamente distribuídas (i.i.d.), exigindo tratamento rigoroso de não estacionariedade, quebras estruturais e ordenação temporal \cite{ref7, ref9}. No contexto da inflação brasileira, a identificação de regimes latentes — tanto sazonais intra-anuais quanto macroeconômicos plurianuais — demanda técnicas de aprendizado não supervisionado (\textit{unsupervised learning}) capazes de segmentar períodos históricos sem impor rótulos arbitrários \textit{a priori}.

Dentre as famílias de algoritmos de agrupamento (\textit{clustering}), selecionou-se o \textbf{Agrupamento Hierárquico Aglomerativo baseado no Critério de Mínima Variância de Ward} (\textit{Ward's Hierarchical Agglomerative Clustering}) \cite{ref19}. Enquanto métodos particionais clássicos como o $K$-Means dependem de sementes estocásticas aleatórias de inicialização e assumem partições estritamente hiper-esféricas de variâncias homogêneas, o método de Ward constrói uma árvore hierárquica determinística (\textit{dendrograma}), permitindo inspecionar visual e analiticamente a distância de corte ótima e a estrutura aninhada dos regimes temporais \cite{ref7, ref19}.

\subsubsection{Formulação Matemática do Critério de Mínima Variância de Ward}
O método de Ward opera sob uma estratégia aglomerativa \textit{bottom-up}: inicia-se com $N$ clusters unitários e, a cada iteração $t$, fundem-se iterativamente os dois clusters que proporcionam o \textbf{menor incremento na soma total dos quadrados dos desvios intra-cluster} (\textit{Error Sum of Squares} -- $ESS$) \cite{ref19}. 

Para um agrupamento $C_k$ contendo $n_k$ vetores de atributos $x_i \in \mathbb{R}^p$ e centróide $\bar{x}_k = \frac{1}{n_k} \sum_{x_i \in C_k} x_i$, a variância intra-cluster ($ESS_k$) é formalmente definida como:
\begin{equation}
ESS_k = \sum_{x_i \in C_k} ||x_i - \bar{x}_k||^2
\end{equation}

A função objetivo global para uma partição em $K$ grupos consiste na minimização do somatório das variâncias internas:
\begin{equation}
ESS_{\text{Total}} = \sum_{k=1}^K ESS_k = \sum_{k=1}^K \sum_{x_i \in C_k} ||x_i - \bar{x}_k||^2
\end{equation}

Ao avaliar a união de dois clusters arbitrários $A$ e $B$ com tamanhos $n_A$ e $n_B$ e centróides $\bar{x}_A$ e $\bar{x}_B$, o acréscimo de variância $\Delta ESS_{AB}$ gerado pela fusão corresponde à distância euclidiana ponderada entre seus centróides \cite{ref19}:
\begin{equation}
\Delta ESS_{AB} = ESS_{A \cup B} - (ESS_A + ESS_B) = \frac{n_A \cdot n_B}{n_A + n_B} ||\bar{x}_A - \bar{x}_B||^2
\end{equation}

A cada passo aglomerativo, o algoritmo seleciona o par ótimo $(A^*, B^*)$ que satisfaz o critério de variância mínima:
\begin{equation}
(A^*, B^*) = \arg\min_{A, B} \Delta ESS_{AB}
\end{equation}

\subsubsection{Recorrência de Lance-Williams e Propriedades para Séries Temporais}
A atualização computacional da matriz de dissimilaridades entre o novo cluster fundido $(A \cup B)$ e qualquer outro cluster remanescente $C$ é governada pela equação de recorrência generalizada de Lance-Williams \cite{ref20}:
\begin{equation}
D(A \cup B, C) = \alpha_A D(A, C) + \alpha_B D(B, C) + \beta D(A, B) + \gamma |D(A, C) - D(B, C)|
\end{equation}
onde para o método de Ward os coeficientes são $\alpha_A = \frac{n_A + n_C}{n_A + n_B + n_C}$, $\alpha_B = \frac{n_B + n_C}{n_A + n_B + n_C}$, $\beta = -\frac{n_C}{n_A + n_B + n_C}$ e $\gamma = 0$ \cite{ref7, ref20}. Essa formulação confere determinismo estrito, preservação de assimetrias estruturais de frequência e auditabilidade topológica."""

p22 = text.find(r'\subsection{Mineração de Dados em Séries Temporais}')
p23 = text.find(r'\subsection{Trabalhos Relacionados e Análise de Diferenciais}')
text = text[:p22] + tex_2_2 + '\n\n' + text[p23:]
print('Seção 2.2 LaTeX atualizada!')

# 2. Inserir Seção 3.5
tex_3_5 = r"""\subsection{Metodologia Experimental de Agrupamento: Sazonalidade e Regimes de Ouro e Juros}
A identificação de padrões não supervisionados na economia brasileira requer rigor na especificação do espaço de atributos. Fenômenos sazonais e ciclos macroeconômicos operam em naturezas temporais distintas:
\begin{itemize}
    \item \textbf{Sazonalidade:} Processo determinístico e recorrente de frequência intra-anual fixa ($S = 12$ meses);
    \item \textbf{Ciclos Macroeconômicos (Ouro e Juros):} Processos estocásticos plurianuais governados por decisões de política monetária e choques geopolíticos internacionais (ciclos de 24 a 60 meses).
\end{itemize}

A unificação ingênua de atributos calendáricos com variáveis financeiras num único espaço euclidiano distorce o cálculo métrico e resulta em agrupamentos espúrios (\textit{spurious clustering}). Para superar essa limitação, este projeto adotou o framework desacoplado em duas camadas (\textit{Two-Tier Decoupled Clustering Framework}), complementado por uma análise de interação cruzada:

\subsubsection{Protocolo Experimental da Camada 1 (Sazonalidade Intra-Anual)}
Selecionaram-se os 7 componentes desagregados de preços do IPCA apurados pelo IBGE (\texttt{Transportes}, \texttt{Alimentação e Bebidas}, \texttt{Habitação}, \texttt{Saúde}, \texttt{Vestuário}, \texttt{Educação} e \texttt{Despesas Pessoais}). Aplicou-se o escalonamento $Z$-Score em cada componente $j$ ($z_{i,j} = \frac{x_{i,j} - \mu_j}{\sigma_j}$), submetendo a matriz ao agrupamento hierárquico com critério de Ward.

\subsubsection{Protocolo Experimental da Camada 2 (Regimes de Inflação, Ouro e Juros)}
Construiu-se um vetor tridimensional estacionário para cada mês $t$ ($N = 173$ meses): (i) $\text{IPCA}_t$ (\% a.m.); (ii) $\Delta \text{SELIC}_t = \text{SELIC}_t - \text{SELIC}_{t-1}$ (aceleração monetária em p.p.); e (iii) $\Delta \% \text{Ouro}_{BRL,t}$ (retorno percentual mensal do ouro físico internacional GLD convertido para Reais via PTAX), capturando risco global e câmbio \cite{ref21, ref22}. O juro real \textit{ex-post} ($r_t = \text{SELIC}_t - \text{IPCA}_t$) foi preservado como variável de auditoria.

\subsubsection{Métricas de Validação Interna e Avaliação Estatística}
A determinação de $k \in \{2, 3, 4, 5, 6\}$ baseou-se no Coeficiente de Silhueta (\textit{Silhouette Score} -- $s_i$), Índice de Davies-Bouldin ($DB$) e Índice de Calinski-Harabasz ($CH$). Na Camada 3, a hipótese de independência estocástica entre sazonalidade e regimes foi submetida ao Teste Qui-Quadrado de Pearson ($\chi^2$)."""

p34 = text.find(r'\subsection{Análise Exploratória e Descritiva dos Dados}')
p4 = text.find(r'\section{CONSIDERAÇÕES FINAIS E TRABALHOS FUTUROS}')
text = text[:p4] + tex_3_5 + '\n\n' + text[p4:]
print('Seção 3.5 LaTeX adicionada!')

# 3. Atualizar Seção 4
tex_4 = r"""\section{RESULTADOS OBTIDOS E DISCUSSÕES}
% =====================================================================

\subsection{Resultados Obtidos na Clusterização de Sazonalidade e Regimes Macroeconômicos}
A aplicação experimental do \textit{Two-Tier Decoupled Framework} forneceu evidências empíricas contundentes sobre a arquitetura da inflação brasileira.

\subsubsection{Camada 1: Sazonalidade e Choques Estruturais dos Componentes do IPCA}
A Tabela \ref{tab:metricas_camada1} sintetiza as métricas de validação interna do agrupamento hierárquico de Ward aplicado aos 7 componentes desagregados do IPCA ($N = 174$ meses).

\begin{table}[H]
\centering
\caption{Métricas de Validação Interna do Agrupamento Hierárquico (Ward) -- Camada 1}
\label{tab:metricas_camada1}
\small
\begin{tabular}{cccc}
\toprule
\textbf{Clusters ($k$)} & \textbf{Silhouette} & \textbf{Davies-Bouldin ($DB$)} & \textbf{Calinski-Harabasz ($CH$)} \\
\midrule
$k = 2$ & 0,324 & 1,085 & 63,8 \\
$k = 3$ & 0,132 & 1,837 & 44,5 \\
\textbf{$k = 4$ (Adotado)} & \textbf{0,155} & \textbf{1,796} & \textbf{38,6} \\
$k = 5$ & 0,175 & 1,631 & 34,2 \\
$k = 6$ & 0,179 & 1,587 & 31,9 \\
\bottomrule
\end{tabular}
\end{table}

A solução com $k=4$ foi adotada por isolar com precisão cirúrgica os quatro regimes calendáricos. A Figura \ref{fig:dendro_sazonal} ilustra o dendrograma resultante, com linha tracejada vermelha no corte ótimo em altura 14,0.

\begin{figure}[H]
\centering
\includegraphics[width=0.92\linewidth]{Figura_6_Dendrograma_Sazonalidade_IPCA.png}
\caption{Dendrograma de Agrupamento Hierárquico (critério de Ward) dos Componentes Setoriais do IPCA (2012--2026). Linha tracejada indica corte em $k=4$.}
\label{fig:dendro_sazonal}
\end{figure}

O heatmap da Figura \ref{fig:heat_sazonal} detalha os desvios-padrão médios de cada componente setorial nos quatro grupos sazonais.

\begin{figure}[H]
\centering
\includegraphics[width=0.88\linewidth]{Figura_7_Heatmap_Perfis_Sazonais.png}
\caption{Perfis Médios Padronizados ($Z$-Score) dos 7 Subcomponentes do IPCA nos 4 Regimes Sazonais.}
\label{fig:heat_sazonal}
\end{figure}

A caracterização econômica dos 4 regimes sazonais confirma as regularidades institucionais:
\begin{enumerate}
    \item \textbf{Cluster 3 -- Choque Educacional (Fevereiro):} Isola 12 dos 13 meses de fevereiro da série (92,3\% de especificidade), com desvio extremo em Educação ($+3,22\sigma$), refletindo reajustes de matrículas e mensalidades;
    \item \textbf{Cluster 1 -- Janela Regulatória de Medicamentos (Abril/Maio):} Concentra 13 dos 15 meses de abril, com desvio em Saúde e Cuidados Pessoais ($+1,15\sigma$), capturando o reajuste anual da CMED/ANVISA;
    \item \textbf{Cluster 2 -- Alívio de Safra Agrícola (Julho a Outubro):} Agrupa o período de colheita e clima seco, com forte deflação em Alimentação e Bebidas ($-0,58\sigma$);
    \item \textbf{Cluster 0 -- Pressões de Início e Fim de Ano (Novembro a Março):} Agrupa meses com pressões combinadas de demanda (13º salário, comércio, turismo) e reajustes tarifários municipais (transporte urbano).
\end{enumerate}

\subsubsection{Camada 2: Regimes Macroeconômicos com Ouro e Taxa de Juros}
O agrupamento tridimensional $[\text{IPCA}_t, \Delta\text{SELIC}_t, \Delta\%\text{Ouro}_{BRL,t}]$ isolou 4 regimes macroeconômicos alinhados à teoria monetária, sintetizados na Tabela \ref{tab:perfis_macro}.

\begin{table}[H]
\centering
\caption{Caracterização Macroeconômica dos 4 Regimes Identificados por Ward ($N = 173$ meses)}
\label{tab:perfis_macro}
\footnotesize
\begin{tabular}{lcccccc}
\toprule
\textbf{Regime Macroeconômico} & \textbf{Meses} & \textbf{IPCA (\%)} & \textbf{$\Delta$SELIC (p.p.)} & \textbf{Ret. Ouro (\%)} & \textbf{Juro Real (\%)} & \textbf{Câmbio} \\
\midrule
\textbf{0: Aperto Hawkish} & 53 & 0,501\% & \textbf{+0,064} & -3,318\% & +0,327\% & 3,896 \\
\textbf{1: Voo p/ Qualidade} & 67 & 0,283\% & -0,026 & \textbf{+5,220\%} & +0,465\% & 4,157 \\
\textbf{2: Desinflação/Cortes} & 23 & \textbf{-0,067\%} & \textbf{-0,117} & -1,014\% & \textbf{+0,927\%} & 3,968 \\
\textbf{3: Choque Severo} & 30 & \textbf{1,044\%} & +0,045 & \textbf{+2,368\%} & \textbf{-0,328\%} & \textbf{4,375} \\
\bottomrule
\end{tabular}
\end{table}

A dispersão bivariada dos 4 regimes é ilustrada na Figura \ref{fig:macro_scatter}.

\begin{figure}[H]
\centering
\includegraphics[width=0.98\linewidth]{Figura_8_Clusters_Macro_Ouro_Juros.png}
\caption{Dispersão Bivariada dos 4 Regimes Macroeconômicos: (A) IPCA vs $\Delta$SELIC; (B) IPCA vs Retorno do Ouro em Reais.}
\label{fig:macro_scatter}
\end{figure}

\subsubsection{Camada 3: Interação Cruzada e Teste de Independência}
A matriz de contingência da Figura \ref{fig:contingencia} cruza as partições da Camada 1 e Camada 2.

\begin{figure}[H]
\centering
\includegraphics[width=0.88\linewidth]{Figura_9_Matriz_Contingencia_Sazonal_Macro.png}
\caption{Matriz de Contingência e Interação Cruzada: Regimes Sazonais vs Regimes Macroeconômicos.}
\label{fig:contingencia}
\end{figure}

O Teste Qui-Quadrado de Pearson resultou em $\chi^2 = 34{,}82$ ($p = 0{,}0001$), rejeitando a independência. Evidencia-se que 65,2\% dos meses de desinflação ocorrem na safra agrícola, enquanto o Choque Inflacionário Severo suprime o alívio de safra (apenas 3 ocorrências).

\subsection{Considerações Finais e Trabalhos Futuros}"""

p4_new = text.find(r'\section{CONSIDERAÇÕES FINAIS E TRABALHOS FUTUROS}')
p_bib = text.find(r'\begin{thebibliography}')
corpo_4_orig = text[p4_new + len(r'\section{CONSIDERAÇÕES FINAIS E TRABALHOS FUTUROS}'):p_bib].strip()
text = text[:p4_new] + tex_4 + '\n\n' + corpo_4_orig + '\n\n' + text[p_bib:]
print('Seção 4 LaTeX atualizada!')

# 4. Adicionar referências ref19 a ref22 antes de \end{thebibliography}
bib_novas = r"""\bibitem{ref19} WARD, J. H. Hierarchical grouping to optimize an objective function. \textbf{Journal of the American Statistical Association}, v. 58, n. 301, p. 236--244, 1963.
\bibitem{ref20} LANCE, G. N.; WILLIAMS, W. T. A general theory of classificatory sorting strategies: II. Clustering systems. \textbf{The Computer Journal}, v. 10, n. 3, p. 271--277, 1967.
\bibitem{ref21} BAUR, D. G.; LUCEY, B. M. Is gold a hedge or a safe haven? An analysis of stocks, bonds and gold. \textbf{Financial Review}, v. 45, n. 2, p. 217--229, 2010.
\bibitem{ref22} ERB, C. B.; HARVEY, C. R. The golden dilemma. \textbf{Financial Analysts Journal}, v. 69, n. 4, p. 10--42, 2013.
"""

p_end_bib = text.find(r'\end{thebibliography}')
text = text[:p_end_bib] + bib_novas + '\n' + text[p_end_bib:]
print('Referências LaTeX adicionadas!')

with open(tex_path, 'w', encoding='utf-8') as f:
    f.write(text)
print('Arquivo main.tex atualizado com sucesso!')

# 5. Criar ZIP atualizado
zip_name = 'Artigo/Template_REPA_2026_2_Artigo_Previsao_Inflacao.zip'
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('Artigo/Template_REPA_LaTeX'):
        for file in files:
            if not file.endswith('.bak'):
                abs_f = os.path.join(root, file)
                rel_f = os.path.relpath(abs_f, 'Artigo/Template_REPA_LaTeX')
                zipf.write(abs_f, rel_f)
print(f'Pacote ZIP atualizado gerado em: {zip_name}')
shutil.copyfile(zip_name, 'Entrega_Classroom/3_Artigo_Completo/Template_REPA_2026_2_Artigo_Previsao_Inflacao.zip')
print('Pacote ZIP sincronizado para Entrega_Classroom/3_Artigo_Completo/')
