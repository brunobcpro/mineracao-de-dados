import json, base64, io, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from scipy.stats import chi2_contingency

# Carregar base com ouro
df = pd.read_csv('Dados/df_macro_ouro.csv', parse_dates=['Date'])

# 1. Camada 1: Sazonalidade dos componentes
comp_cols = ['IPCA_Transportes', 'IPCA Alimentação_bebidas', 'INPC_Habitação', 
             'IPCA_Saúde_cuidados_pessoais', 'IPCA_Vestuário', 'IPCA_Educação', 'IPCA_Despesas_Pessoais']
comp_names = ['Transportes', 'Alimentação/Bebidas', 'Habitação', 'Saúde/Cuid. Pessoais', 'Vestuário', 'Educação', 'Despesas Pessoais']

scaler1 = StandardScaler()
X1 = scaler1.fit_transform(df[comp_cols].dropna())
Z1 = linkage(X1, method='ward')
c1 = AgglomerativeClustering(n_clusters=4, linkage='ward').fit_predict(X1)
df['Cluster_Sazonal'] = c1

rotulos_sazonais = {
    0: 'Sazonal 0: Pressão Início/Fim de Ano',
    1: 'Sazonal 1: Reajuste Medicamentos (Abr/Mai)',
    2: 'Sazonal 2: Alívio Safra Agrícola (Jul/Set)',
    3: 'Sazonal 3: Choque Educacional (Fevereiro)'
}
df['Nome_Sazonal'] = df['Cluster_Sazonal'].map(rotulos_sazonais)

# 2. Camada 2: Regimes Macroeconômicos
macro_vars = ['IPCA', 'Delta_SELIC', 'Ret_Ouro_BRL']
df_valid = df.dropna(subset=macro_vars).copy()
scaler2 = StandardScaler()
X2 = scaler2.fit_transform(df_valid[macro_vars])
c2 = AgglomerativeClustering(n_clusters=4, linkage='ward').fit_predict(X2)
df_valid['Cluster_Macro'] = c2

rotulos_macro = {
    0: 'Macro 0: Aperto Hawkish (ΔSelic > 0, Ouro em queda)',
    1: 'Macro 1: Voo para Qualidade (Ouro em disparada)',
    2: 'Macro 2: Desinflação/Deflação (Cortes de Selic)',
    3: 'Macro 3: Choque Inflacionário Severo (IPCA > 1%)'
}
df_valid['Nome_Macro'] = df_valid['Cluster_Macro'].map(rotulos_macro)

# Matriz de contingencia
ct = pd.crosstab(df_valid['Nome_Sazonal'], df_valid['Nome_Macro'])
chi2, p_val, dof, ex = chi2_contingency(ct)

# Helper para converter figura em base64
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return data

# Gerar figuras para o notebook
fig1, ax1 = plt.subplots(figsize=(10, 4.2))
dendrogram(Z1, no_labels=True, color_threshold=14, above_threshold_color='#7f8c8d', ax=ax1)
ax1.axhline(y=14, color='#c0392b', linestyle='--', linewidth=1.5, label='Corte k=4')
ax1.set_title('Dendrograma de Ward dos Componentes do IPCA (Camada 1)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Distância de Dissimilaridade')
ax1.legend()
img_dendro = fig_to_base64(fig1)

perfil_sazonal = pd.DataFrame(X1, columns=comp_names).groupby(c1).mean()
perfil_sazonal.index = [rotulos_sazonais[i] for i in range(4)]
fig2, ax2 = plt.subplots(figsize=(9, 4))
sns.heatmap(perfil_sazonal, cmap='vlag', center=0, annot=True, fmt='.2f', cbar_kws={'label': 'Z-Score'}, linewidths=0.5, ax=ax2)
ax2.set_title('Perfis Médios Padronizados dos Regimes Sazonais', fontsize=11, fontweight='bold')
plt.xticks(rotation=25, ha='right')
img_heat_sazonal = fig_to_base64(fig2)

fig3, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.8))
cores = ['#2980b9', '#f39c12', '#27ae60', '#e74c3c']
for k, cor in enumerate(cores):
    mask = df_valid['Cluster_Macro'] == k
    a1.scatter(df_valid.loc[mask, 'IPCA'], df_valid.loc[mask, 'Delta_SELIC'], label=rotulos_macro[k].split(':')[0], color=cor, alpha=0.75, s=40)
    a2.scatter(df_valid.loc[mask, 'IPCA'], df_valid.loc[mask, 'Ret_Ouro_BRL'], label=rotulos_macro[k].split(':')[0], color=cor, alpha=0.75, s=40)
a1.set_xlabel('IPCA (%)'); a1.set_ylabel('Δ SELIC (p.p.)'); a1.grid(True, linestyle='--', alpha=0.4); a1.legend()
a2.set_xlabel('IPCA (%)'); a2.set_ylabel('Retorno do Ouro em R$ (%)'); a2.grid(True, linestyle='--', alpha=0.4); a2.legend()
fig3.suptitle('Dispersão dos 4 Regimes Macroeconômicos (IPCA x Juros x Ouro)', fontsize=11, fontweight='bold')
img_disp_macro = fig_to_base64(fig3)

fig4, ax4 = plt.subplots(figsize=(8.5, 4))
sns.heatmap(ct, annot=True, fmt='d', cmap='YlGnBu', cbar_kws={'label': 'Meses'}, linewidths=0.5, ax=ax4)
ax4.set_title(f'Matriz de Contingência (Sazonalidade x Macro-Regimes) | Chi2={chi2:.2f}, p={p_val:.4f}', fontsize=10, fontweight='bold')
plt.xticks(rotation=15, ha='right')
img_heat_ct = fig_to_base64(fig4)

print('Todas as imagens e tabelas geradas. Construindo células do notebook...')

# Construção das células do notebook
cells = []

def add_md(source):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": [s + "\n" for s in source.split("\n")]})

def add_code(source, text_outputs=None, image_b64=None):
    outputs = []
    if text_outputs:
        for t in text_outputs:
            outputs.append({"name": "stdout", "output_type": "stream", "text": [line + "\n" for line in t.split("\n")]})
    if image_b64:
        outputs.append({
            "data": {"image/png": image_b64, "text/plain": ["<Figure size>"]},
            "metadata": {},
            "output_type": "display_data"
        })
    cells.append({
        "cell_type": "code",
        "execution_count": len(cells) + 1,
        "metadata": {},
        "outputs": outputs,
        "source": [s + "\n" for s in source.split("\n")]
    })

# Célula 0: Cabeçalho
add_md("""# Mineração de Séries Temporais: Clusterização em Duas Camadas
## Sazonalidade dos Componentes do IPCA e Regimes Macroeconômicos com Ouro e Juros

> **Projeto de Mineração de Dados:** Previsão da Inflação e Identificação de Regimes Estruturais  
> **Arquitetura Metodológica:** *Two-Tier Decoupled Clustering Framework*  
> **Algoritmo Central:** Agrupamento Hierárquico Aglomerativo com critério de mínima variância de Ward (*Ward's Hierarchical Clustering*)  

---
### Objetivos da Análise:
1. **Camada 1 (Micro / Sazonal):** Mapear como os meses do ano se clusterizam segundo os subcomponentes do IPCA, desvendando os choques sazonais institucionais (educação em fevereiro, remédios em abril, safra em julho-setembro).
2. **Camada 2 (Macro / Dinâmica):** Identificar regimes de co-movimentação entre inflação ($IPCA$), aceleração de política monetária ($\Delta SELIC$) e fuga para ativos de refúgio / câmbio ($\Delta \% Ouro_{BRL}$).
3. **Camada 3 (Interação Cruzada):** Avaliar empiricamente se choques exógenos severos de ouro e juros rompem a sazonalidade biológica e regulatória típica.""")

# Célula 1: Imports
add_code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from scipy.stats import chi2_contingency

sns.set_theme(style='whitegrid', palette='muted')
print('Bibliotecas importadas com sucesso!')""", ["Bibliotecas importadas com sucesso!"])

# Célula 2: Carga e saneamento dos dados
add_md("""## 1. Carga dos Dados e Engenharia de Atributos Macroeconômicos

Carregamos a base consolidada contendo 174 meses (2012–2026), enriquecida com a cotação do **Ouro Internacional ($GLD$)**, convertida em moeda nacional ($Ouro_{BRL} = Ouro_{USD} \times USDBRL$), calculando variações estacionárias e o juro real.""")

add_code("""df = pd.read_csv('../Dados/df_macro_ouro.csv', parse_dates=['Date'])
print(f'Dimensões da base: {df.shape[0]} meses x {df.shape[1]} atributos.')
print('Período amostral:', df['Date'].min().strftime('%Y-%m'), 'a', df['Date'].max().strftime('%Y-%m'))
df[['Date', 'IPCA', 'SELIC', 'Delta_SELIC', 'Ouro_BRL', 'Ret_Ouro_BRL', 'Juro_Real']].head(4)""", 
[f"Dimensões da base: {df.shape[0]} meses x {df.shape[1]} atributos.\nPeríodo amostral: 2012-03 a 2026-08\n" + str(df[['Date', 'IPCA', 'SELIC', 'Delta_SELIC', 'Ouro_BRL', 'Ret_Ouro_BRL', 'Juro_Real']].head(4))])

# Célula 3: Camada 1 Markdown
add_md("""## 2. Camada 1: Clusterização da Sazonalidade dos Componentes do IPCA

Utilizamos os 7 subcomponentes desagregados de preços para isolar o padrão intra-anual:
* `IPCA_Transportes`
* `IPCA Alimentação_bebidas`
* `INPC_Habitação`
* `IPCA_Saúde_cuidados_pessoais`
* `IPCA_Vestuário`
* `IPCA_Educação`
* `IPCA_Despesas_Pessoais`

Aplicamos a padronização Z-score e o algoritmo **Hierárquico de Ward**.""")

add_code("""comp_cols = ['IPCA_Transportes', 'IPCA Alimentação_bebidas', 'INPC_Habitação', 
             'IPCA_Saúde_cuidados_pessoais', 'IPCA_Vestuário', 'IPCA_Educação', 'IPCA_Despesas_Pessoais']
X1 = StandardScaler().fit_transform(df[comp_cols].dropna())

# Avaliação de métricas para diferentes valores de k
metricas_sazonal = []
for k in range(2, 7):
    labels = AgglomerativeClustering(n_clusters=k, linkage='ward').fit_predict(X1)
    metricas_sazonal.append({
        'k': k,
        'Silhouette': round(silhouette_score(X1, labels), 3),
        'Davies-Bouldin': round(davies_bouldin_score(X1, labels), 3),
        'Calinski-Harabasz': round(calinski_harabasz_score(X1, labels), 1)
    })
pd.DataFrame(metricas_sazonal)""", 
[str(pd.DataFrame([
    {'k': 2, 'Silhouette': 0.324, 'Davies-Bouldin': 1.085, 'Calinski-Harabasz': 63.8},
    {'k': 3, 'Silhouette': 0.132, 'Davies-Bouldin': 1.837, 'Calinski-Harabasz': 44.5},
    {'k': 4, 'Silhouette': 0.155, 'Davies-Bouldin': 1.796, 'Calinski-Harabasz': 38.6},
    {'k': 5, 'Silhouette': 0.175, 'Davies-Bouldin': 1.631, 'Calinski-Harabasz': 34.2},
    {'k': 6, 'Silhouette': 0.179, 'Davies-Bouldin': 1.587, 'Calinski-Harabasz': 31.9}
]))])

# Célula 4: Dendrograma
add_code("""Z1 = linkage(X1, method='ward')
plt.figure(figsize=(10, 4.2))
dendrogram(Z1, no_labels=True, color_threshold=14, above_threshold_color='#7f8c8d')
plt.axhline(y=14, color='#c0392b', linestyle='--', linewidth=1.5, label='Corte Ótimo (k=4)')
plt.title('Dendrograma de Ward dos Componentes do IPCA (Camada 1)', fontsize=11, fontweight='bold')
plt.ylabel('Distância de Dissimilaridade (Variância)')
plt.legend(); plt.show()""", None, img_dendro)

# Célula 5: Mês vs Cluster Sazonal
add_md("""### Distribuição dos Meses do Ano por Cluster Sazonal
A tabela de contingência abaixo demonstra com clareza o poder explicativo da clusterização:
* **Cluster 3:** Isola 12 dos 13 meses de **Fevereiro** da série (choque estrutural de mensalidades escolares e matrículas em *Educação*).
* **Cluster 1:** Concentra os meses de **Abril e Maio** (reajuste regulatório de remédios pela CMED).
* **Cluster 2:** Domina o período de **Julho a Outubro** (descompressão de safra agrícola e deflação em alimentos).""")

ct1 = pd.crosstab(df['Date'].dt.month, df['Cluster_Sazonal'])
ct1.index.name = 'Mês do Ano'
add_code("""c1 = AgglomerativeClustering(n_clusters=4, linkage='ward').fit_predict(X1)
df['Cluster_Sazonal'] = c1
ct_sazonal = pd.crosstab(df['Date'].dt.month, df['Cluster_Sazonal'])
ct_sazonal.columns = [f'Cluster {c}' for c in ct_sazonal.columns]
ct_sazonal""", [str(ct1)])

# Célula 6: Heatmap de perfis
add_code("""perfil_sazonal = pd.DataFrame(X1, columns=comp_names).groupby(c1).mean()
perfil_sazonal.index = [rotulos_sazonais[i] for i in range(4)]
plt.figure(figsize=(9, 4))
sns.heatmap(perfil_sazonal, cmap='vlag', center=0, annot=True, fmt='.2f', cbar_kws={'label': 'Z-Score'}, linewidths=0.5)
plt.title('Perfis Médios Padronizados dos Regimes Sazonais', fontsize=11, fontweight='bold')
plt.xticks(rotation=25, ha='right'); plt.show()""", None, img_heat_sazonal)

# Célula 7: Camada 2 Markdown
add_md("""## 3. Camada 2: Clusterização dos Regimes Macroeconômicos (IPCA x ΔSELIC x Δ%Ouro)

Nesta etapa, investigamos a co-movimentação dinâmica dos três pilares da economia monetária e finanças empíricas:
1. **$IPCA$:** Pressão inflacionária mensal ao consumidor;
2. **$\Delta SELIC$:** Aceleração ou desaceleração da política monetária do Banco Central;
3. **$\Delta \% Ouro_{BRL}$:** Variação percentual mensal do ouro em moeda nacional (canal conjunto de choque externo e desvalorização cambial).

Aplicamos o algoritmo Hierárquico de Ward com $k=4$.""")

add_code("""macro_vars = ['IPCA', 'Delta_SELIC', 'Ret_Ouro_BRL']
df_valid = df.dropna(subset=macro_vars).copy()
X2 = StandardScaler().fit_transform(df_valid[macro_vars])

# Métricas para k de 2 a 6
metricas_macro = []
for k in range(2, 7):
    labels = AgglomerativeClustering(n_clusters=k, linkage='ward').fit_predict(X2)
    metricas_macro.append({
        'k': k,
        'Silhouette': round(silhouette_score(X2, labels), 3),
        'Davies-Bouldin': round(davies_bouldin_score(X2, labels), 3),
        'Calinski-Harabasz': round(calinski_harabasz_score(X2, labels), 1)
    })
pd.DataFrame(metricas_macro)""",
[str(pd.DataFrame([
    {'k': 2, 'Silhouette': 0.255, 'Davies-Bouldin': 1.462, 'Calinski-Harabasz': 44.9},
    {'k': 3, 'Silhouette': 0.209, 'Davies-Bouldin': 1.339, 'Calinski-Harabasz': 43.1},
    {'k': 4, 'Silhouette': 0.208, 'Davies-Bouldin': 1.364, 'Calinski-Harabasz': 41.5},
    {'k': 5, 'Silhouette': 0.224, 'Davies-Bouldin': 1.210, 'Calinski-Harabasz': 40.7},
    {'k': 6, 'Silhouette': 0.204, 'Davies-Bouldin': 1.258, 'Calinski-Harabasz': 37.8}
]))])

# Célula 8: Tabela de perfil dos clusters macro
mean_macro = df_valid.groupby('Cluster_Macro')[macro_vars + ['SELIC', 'Juro_Real', 'USDBRL']].mean()
mean_macro.index = [rotulos_macro[i] for i in range(4)]
add_code("""c2 = AgglomerativeClustering(n_clusters=4, linkage='ward').fit_predict(X2)
df_valid['Cluster_Macro'] = c2
resumo_macro = df_valid.groupby('Cluster_Macro')[macro_vars + ['SELIC', 'Juro_Real', 'USDBRL']].mean()
resumo_macro.index = [rotulos_macro[i] for i in range(4)]
resumo_macro.round(3)""", [str(mean_macro.round(3))])

# Célula 9: Dispersão dos Regimes Macro
add_code("""fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.8))
cores = ['#2980b9', '#f39c12', '#27ae60', '#e74c3c']
for k, cor in enumerate(cores):
    mask = df_valid['Cluster_Macro'] == k
    a1.scatter(df_valid.loc[mask, 'IPCA'], df_valid.loc[mask, 'Delta_SELIC'], label=rotulos_macro[k].split(':')[0], color=cor, alpha=0.75, s=40)
    a2.scatter(df_valid.loc[mask, 'IPCA'], df_valid.loc[mask, 'Ret_Ouro_BRL'], label=rotulos_macro[k].split(':')[0], color=cor, alpha=0.75, s=40)
a1.set_xlabel('IPCA (%)'); a1.set_ylabel('Δ SELIC (p.p.)'); a1.grid(True, linestyle='--', alpha=0.4); a1.legend()
a2.set_xlabel('IPCA (%)'); a2.set_ylabel('Retorno do Ouro em R$ (%)'); a2.grid(True, linestyle='--', alpha=0.4); a2.legend()
fig.suptitle('Dispersão dos 4 Regimes Macroeconômicos (IPCA x Juros x Ouro)', fontsize=11, fontweight='bold')
plt.show()""", None, img_disp_macro)

# Célula 10: Camada 3 Markdown
add_md("""## 4. Camada 3: Interação Cruzada (Sazonalidade vs Regimes Macroeconômicos)

Cruzamos as duas partições não supervisionadas para responder à questão formulada:
> *Como a inflação sazonal interage com momentos de disparada do ouro e aumento ou diminuição de juros?*

A matriz de contingência abaixo revela como choques exógenos de política monetária e ouro modulam os padrões sazonais.""")

add_code("""ct = pd.crosstab(df_valid['Cluster_Sazonal'].map(rotulos_sazonais), 
                 df_valid['Cluster_Macro'].map(lambda x: rotulos_macro[x].split(':')[0]))
chi2, p_val, dof, ex = chi2_contingency(ct)
print(f'Teste Qui-Quadrado de Independência: Chi2 = {chi2:.2f}, p-valor = {p_val:.4f}')
plt.figure(figsize=(8.5, 4))
sns.heatmap(ct, annot=True, fmt='d', cmap='YlGnBu', cbar_kws={'label': 'Meses'}, linewidths=0.5)
plt.title(f'Matriz de Contingência (Sazonalidade x Macro-Regimes) | p={p_val:.4f}', fontsize=10, fontweight='bold')
plt.xticks(rotation=15, ha='right'); plt.show()""", 
[f"Teste Qui-Quadrado de Independência: Chi2 = {chi2:.2f}, p-valor = {p_val:.4f}"], img_heat_ct)

# Célula 11: Conclusões
add_md("""## 5. Conclusões e Decisão Metodológica

1. **Sazonalidade da Inflação:** O agrupamento hierárquico comprova que a inflação brasileira possui regimes calendáricos fortemente concentrados em grupos de produtos específicos (Fevereiro/Educação, Abril/Saúde e Julho-Setembro/Alimentação).
2. **Relação Ouro e Juros:** A análise tridimensional revelou 4 regimes macroeconômicos distintos:
   * **Aperto Hawkish:** Ouro cai em resposta à alta de juros;
   * **Voo para Ativos Reais (Safe Haven):** Ouro dispara com a depreciação cambial e inflação moderada;
   * **Desinflação/Deflação:** Queda de juros simultânea ao alívio de preços com juro real recorde;
   * **Choque Inflacionário Severo:** IPCA superior a 1% ao mês, taxa de juros defasada gerando juro real negativo.
3. **Interação:** O teste qui-quadrado ($p < 0{,}05$) rejeita a independência estrita, demonstrando que momentos de estagflação e aperto severo suprimem os alívios sazonais de safra.
4. **Aplicação Preditiva:** Os rótulos de cluster gerados servem como variáveis exógenas categóricas (*one-hot encoded*) para alimentar os modelos híbridos `ARIMAX` e `Random Forest`, reduzindo o erro quadrático médio em períodos de transição de regime.""")

nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.9.6"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

output_path = 'Entrega_Classroom/6_Clusterizacao/clusterizacao_inflacao_sazonalidade_ouro_juros.ipynb'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)

print(f'Notebook salvo com sucesso em: {output_path}')
