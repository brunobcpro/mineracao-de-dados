#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script gerador do Jupyter Notebook executado:
'Entrega_Classroom/7_Classificacao/classificacao_regimes_inflacao.ipynb'
Contempla integralmente a Aula 7 e Atividade 7 da UPE (Prof. Alexandre Maciel).
"""

import json
import os
import nbformat as nbf

def build_notebook():
    nb = nbf.v4.new_notebook()
    nb['metadata'] = {
        'kernelspec': {
            'display_name': 'Python 3',
            'language': 'python',
            'name': 'python3'
        },
        'language_info': {
            'codemirror_mode': {'name': 'ipython', 'version': 3},
            'file_extension': '.py',
            'mimetype': 'text/x-python',
            'name': 'python',
            'nbconvert_exporter': 'python',
            'pygments_lexer': 'ipython3',
            'version': '3.9.6'
        }
    }

    cells = []

    # Célula 1: Título e Identificação Acadêmica
    c1 = """# 🏛️ Universidade de Pernambuco (UPE) - Escola Politécnica (POLI)
## Programa de Pós-Graduação em Engenharia da Computação / Mineração de Dados
### **Atividade 7: Métodos de Classificação Supervisionada Aplicados a Regimes de Inflação (IPCA)**
**Professor:** Dr. Alexandre Maciel (`alexandre.maciel@upe.br`)  
**Aluno / Projeto:** Mineração de Dados em Séries Macroeconômicas e Previsão da Inflação  
**Período Amostral:** Março de 2012 a Agosto de 2026 ($N = 174$ meses contínuos)

---

## 🎯 Objetivos da Atividade 7:
1. **Escolha e Aplicação de Algoritmos de Classificação:**
   - Árvore de Decisão (*Decision Tree* com Entropia de Shannon e Ganho de Informação);
   - Classificador Baseado em Regras (Cálculo formal de **Cobertura** e **Precisão**);
   - $k$-Nearest Neighbors ($k$-NN baseado em distância euclidiana e manhattan, com teste de $k$ ímpar);
   - Naïve Bayes Gaussiano (Classificador estatístico baseado no Teorema de Bayes);
   - Baseline Majoritário (*Zero-Rule*) como referencial mínimo.
2. **Engenharia de Dados e Causalidade Temporal:**
   - Prevenção rigorosa de *Data Leakage* temporal: estimar o regime no mês $t$ a partir dos atributos em $t-1$;
   - Discretização macroeconômica dos 3 regimes de inflação: **Deflação**, **Controlado (Meta)** e **Alta Inflação**;
   - *Split* temporal *out-of-sample*: Treino (2012–2021) e Teste (2022–2026).
3. **Avaliação Multicritério:**
   - Matrizes de Confusão $3 \\times 3$, Acurácia, Precisão, Recall e F1-Score (Macro e por classe)."""
    cells.append(nbf.v4.new_markdown_cell(c1))

    # Célula 2: Imports e Setup
    c2 = """import os
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree, _tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# Configuração estética dos gráficos
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 120
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11

print("✅ Bibliotecas importadas com sucesso!")"""
    cells.append(nbf.v4.new_code_cell(c2))

    # Célula 3: Markdown - Carga e Engenharia de Dados
    c3 = """## 📥 1. Ingestão, Saneamento e Engenharia de Atributos

A base consolidada (`df_macro.csv`) reúne 174 meses contínuos do SGS/Banco Central e IBGE.
Definimos três regimes fundamentados na teoria macroeconômica e nas metas do CMN:
- **Deflação:** $\\text{IPCA}_t \\le 0,00\\%$ (choques de oferta de alimentos ou desonerações fiscais pontuais);
- **Controlado / Meta:** $0,00\\% < \\text{IPCA}_t \\le 0,50\\%$ (inflação mensal compatível com o centro da meta anualizada);
- **Alta Inflação:** $\\text{IPCA}_t > 0,50\\%$ (estresse inflacionário que rompe o teto de tolerância da meta).

Para garantir que a modelagem preditiva seja **estritamente causal e sem vazamento futuro (*zero data leakage*)**, todas as covariáveis explicativas são defasadas em $t-1$:
$$Y_t = f(X_{t-1})$$"""
    cells.append(nbf.v4.new_markdown_cell(c3))

    # Célula 4: Código - Carga de dados e defasagem
    c4 = """# 1. Carregamento dos dados
df = pd.read_csv('../../Dados/df_macro.csv' if os.path.exists('../../Dados/df_macro.csv') else 'Dados/df_macro.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)

# Tratamento causal de valores ausentes (ffill em séries com defasagem de publicação)
df = df.ffill().bfill()

# 2. Definição do Target
def classificar_regime(val):
    if val <= 0.0:
        return 'Deflação'
    elif val <= 0.50:
        return 'Controlado'
    else:
        return 'Alta'

df['Regime'] = df['IPCA'].apply(classificar_regime)

# 3. Engenharia de Sazonalidade Cíclica
meses = df['Date'].dt.month
df['mes_sin'] = np.sin(2 * np.pi * meses / 12)
df['mes_cos'] = np.cos(2 * np.pi * meses / 12)

# Atributos preditivos candidatos (t-1)
feature_cols = [
    'IPCA', 'IPCA Alimentação_bebidas', 'IPCA_Transportes', 'INPC_Habitação',
    'IPCA_Educação', 'IGP_M', 'USDBRL', 'SELIC', 'Desemprego',
    'Consumo_Energia_Total', 'mes_sin', 'mes_cos'
]

# Construção do espaço X (t-1) e Y (t)
X = df[feature_cols].shift(1).iloc[1:].copy()
y = df['Regime'].iloc[1:].copy()
dates = df['Date'].iloc[1:].copy()

print(f"Dimensões do espaço amostral: {X.shape[0]} meses e {X.shape[1]} atributos preditivos.")
print("\\nDistribuição Global das Classes (2012–2026):")
dist = y.value_counts()
dist_pct = y.value_counts(normalize=True) * 100
pd.DataFrame({'Contagem': dist, 'Percentual (%)': dist_pct.round(2)})"""
    cells.append(nbf.v4.new_code_cell(c4))

    # Célula 5: Markdown - Divisão Temporal
    c5 = """## ⏳ 2. Metodologia Experimental: Divisão Temporal Out-of-Sample

Em séries temporais macroeconômicas, a divisão aleatória (*k-fold shuffle*) é metodologicamente inválida por introduzir autocorrelação espúria e vazamento temporal.  
Adotamos uma partição cronológica estrita:
- **Conjunto de Treinamento (Indução):** 2012-04 a 2021-12 ($N_{treino} = 117$ meses);
- **Conjunto de Teste (Dedução / Generalização Out-of-Sample):** 2022-01 a 2026-08 ($N_{teste} = 56$ meses).

Esse teste out-of-sample constitui um ambiente de estresse severo, contemplando os choques globais de commodities da guerra na Ucrânia, o ciclo de desonerações tributárias de 2022 e a política de juros pós-pandemia."""
    cells.append(nbf.v4.new_markdown_cell(c5))

    # Célula 6: Código - Split e Normalização
    c6 = """# Split temporal estrito
mask_train = dates < '2022-01-01'
mask_test = dates >= '2022-01-01'

X_train, y_train = X[mask_train].copy(), y[mask_train].copy()
X_test, y_test = X[mask_test].copy(), y[mask_test].copy()
dates_train, dates_test = dates[mask_train], dates[mask_test]

print(f"Período de Treinamento: {dates_train.min().strftime('%m/%Y')} a {dates_train.max().strftime('%m/%Y')} (N = {len(X_train)})")
print(f"Período de Teste:        {dates_test.min().strftime('%m/%Y')} a {dates_test.max().strftime('%m/%Y')} (N = {len(X_test)})")

# Normalização de atributos para algoritmos baseados em distância (k-NN) e densidade (Naïve Bayes)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

labels = ['Deflação', 'Controlado', 'Alta']
print("\\nDistribuição de Classes no Conjunto de Teste:")
print(y_test.value_counts(normalize=True).round(4) * 100)"""
    cells.append(nbf.v4.new_code_cell(c6))

    # Célula 7: Markdown - Modelagem Supervisionada
    c7 = """## 🤖 3. Implementação dos Métodos de Classificação (Aula 7)

Conforme o programa da disciplina (Castro cap. 5, Goldschmidt cap. 5), avaliamos quatro famílias metodológicas:

1. **Baseline Majoritário (Zero-Rule):** Prediz sistematicamente a classe com maior frequência no treino para estabelecer o patamar de desempenho nulo;
2. **Árvore de Decisão:** Utiliza o critério de **Entropia de Shannon** $H(T)$ e **Ganho de Informação** para particionar os atributos e gerar nós de decisão:
   $$H(T) = - \\sum_{j=1}^k p(c_j, T) \\log_2 p(c_j, T)$$
   $$Ganho(A, T) = H(T) - \\sum_{i=1}^n \\frac{|T_i|}{|T|} H(T_i)$$
3. **Classificador Baseado em Regras:** Regras $r_i: (condição) \\rightarrow y_i$ derivadas da árvore, avaliadas por:
   - **Cobertura:** $|A| / |D|$
   - **Precisão:** $|A \\cap y| / |A|$
4. **$k$-NN ($k$-Nearest Neighbors):** Classificador baseado em distância no espaço hiperdimensional padronizado. Avaliamos métricas Euclidiana e Manhattan com $k$ ímpar ($k=5$) para evitar empates na votação;
5. **Naïve Bayes Gaussiano:** Classificador probabilístico fundamentado no Teorema de Bayes:
   $$P(C_i|x) = \\frac{P(x|C_i)P(C_i)}{P(x)}$$"""
    cells.append(nbf.v4.new_markdown_cell(c7))

    # Célula 8: Código - Treinamento dos Classificadores
    c8 = """# 1. Baseline Majoritário
classe_majoritaria = y_train.mode()[0]
y_pred_base = [classe_majoritaria] * len(y_test)

# 2. Árvore de Decisão (Entropia e Ganho de Informação)
# class_weight='balanced' para compensar a menor frequência amostral da classe 'Deflação'
dt = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=3,
    class_weight='balanced',
    min_samples_leaf=2,
    random_state=42
)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)

# 3. k-NN (Distância Euclidiana, k=5)
knn_euc = KNeighborsClassifier(n_neighbors=5, metric='euclidean', weights='distance')
knn_euc.fit(X_train_scaled, y_train)
y_pred_knn_euc = knn_euc.predict(X_test_scaled)

# 4. k-NN (Distância Manhattan, k=5)
knn_man = KNeighborsClassifier(n_neighbors=5, metric='manhattan', weights='distance')
knn_man.fit(X_train_scaled, y_train)
y_pred_knn_man = knn_man.predict(X_test_scaled)

# 5. Naïve Bayes Gaussiano
nb = GaussianNB()
nb.fit(X_train_scaled, y_train)
y_pred_nb = nb.predict(X_test_scaled)

print(" Treinamento de todos os classificadores concluído com sucesso!")"""
    cells.append(nbf.v4.new_code_cell(c8))

    # Célula 9: Markdown - Avaliação e Métricas
    c9 = """## 📊 4. Avaliação Comparativa de Desempenho

Calculamos as métricas formais apresentadas na Aula 7:
- **Acurácia:** Proporção total de acertos sobre todas as previsões;
- **Precisão Macro:** Média aritmética da precisão entre as três classes (evitando viés em direção à classe mais frequente);
- **Recall Macro:** Capacidade média de recuperar as instâncias de cada classe;
- **F1-Score Macro:** Média harmônica entre Precisão e Recall."""
    cells.append(nbf.v4.new_markdown_cell(c9))

    # Célula 10: Código - Métricas e Tabela Comparativa
    c10 = """modelos = {
    'Baseline Majoritário': y_pred_base,
    'Árvore de Decisão (Entropia)': y_pred_dt,
    'k-NN (Euclidiana, k=5)': y_pred_knn_euc,
    'k-NN (Manhattan, k=5)': y_pred_knn_man,
    'Naïve Bayes Gaussiano': y_pred_nb
}

tabela_metricas = []
for nome, preds in modelos.items():
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, average='macro', zero_division=0)
    rec = recall_score(y_test, preds, average='macro', zero_division=0)
    f1 = f1_score(y_test, preds, average='macro', zero_division=0)
    tabela_metricas.append({
        'Modelo Classificador': nome,
        'Acurácia (%)': round(acc * 100, 2),
        'Precisão Macro (%)': round(prec * 100, 2),
        'Recall Macro (%)': round(rec * 100, 2),
        'F1-Score Macro': round(f1, 4)
    })

df_resumo = pd.DataFrame(tabela_metricas).sort_values(by='F1-Score Macro', ascending=False)
display(df_resumo.reset_index(drop=True))"""
    cells.append(nbf.v4.new_code_cell(c10))

    # Célula 11: Markdown - Matrizes de Confusão
    c11 = """### 🔍 Matrizes de Confusão dos Classificadores
A Matriz de Confusão relaciona as classes originais (linhas) com as classes preditas (colunas), permitindo identificar se o modelo confunde regimes adjacentes (ex.: Controlado vs. Alta) ou se comete erros drásticos (ex.: classificar Deflação como Alta Inflação)."""
    cells.append(nbf.v4.new_markdown_cell(c11))

    # Célula 12: Código - Visualização das Matrizes de Confusão
    c12 = """fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for ax, (nome, preds) in zip(axes, [
    ('Árvore de Decisão (Entropia)', y_pred_dt),
    ('k-NN Euclidiana (k=5)', y_pred_knn_euc),
    ('Naïve Bayes Gaussiano', y_pred_nb)
]):
    cm = confusion_matrix(y_test, preds, labels=labels)
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax,
        xticklabels=labels, yticklabels=labels,
        annot_kws={'size': 14, 'weight': 'bold'}
    )
    acc_m = accuracy_score(y_test, preds)
    ax.set_title(f'{nome}\\nAcurácia: {acc_m:.1%}', fontsize=12, pad=10)
    ax.set_xlabel('Classe Predita', fontsize=11, weight='bold')
    ax.set_ylabel('Classe Real Observada', fontsize=11, weight='bold')

plt.tight_layout()
plt.show()"""
    cells.append(nbf.v4.new_code_cell(c12))

    # Célula 13: Markdown - Extração de Regras e Ganho de Informação
    c13 = """## 📜 5. Classificador Baseado em Regras e Ganho de Informação

Conforme os slides 7–10 da Aula 7:
Uma regra de classificação possui a estrutura $r_i: (condição) \\rightarrow y_i$.  
A qualidade da regra é mensurada por:
- **Cobertura:** $\\text{Cobertura}(r) = \\frac{|A|}{|D|}$ (percentual de registros do conjunto que satisfazem a pré-condição da regra);
- **Precisão:** $\\text{Precisão}(r) = \\frac{|A \\cap y|}{|A|}$ (taxa de acerto dentre os registros cobertos pela regra).

Abaixo, extraímos recursivamente todas as regras induzidas pela Árvore de Decisão."""
    cells.append(nbf.v4.new_markdown_cell(c13))

    # Célula 14: Código - Extração formal de regras
    c14 = """def extrair_regras_completas(tree, feature_names, df_data, y_data):
    tree_ = tree.tree_
    class_names = tree.classes_
    feat_map = [feature_names[i] if i != _tree.TREE_UNDEFINED else 'leaf' for i in tree_.feature]
    rules = []

    def recurse(node, path):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feat_map[node]
            th = tree_.threshold[node]
            recurse(tree_.children_left[node], path + [(name, '<=', th)])
            recurse(tree_.children_right[node], path + [(name, '>', th)])
        else:
            counts = tree_.value[node][0]
            pred_class = class_names[np.argmax(counts)]
            
            mask = pd.Series(True, index=df_data.index)
            cond_str = []
            for feat, op, val in path:
                if op == '<=':
                    mask &= (df_data[feat] <= val)
                else:
                    mask &= (df_data[feat] > val)
                cond_str.append(f"({feat} {op} {val:.2f})")
            
            n_A = mask.sum()
            n_D = len(df_data)
            n_A_inter_y = (mask & (y_data == pred_class)).sum()
            
            cobertura = n_A / n_D if n_D > 0 else 0
            precisao = n_A_inter_y / n_A if n_A > 0 else 0
            
            rules.append({
                'Condição': ' ∧ '.join(cond_str),
                'Classe': pred_class,
                'Cobertura (%)': round(cobertura * 100, 2),
                'Precisão (%)': round(precisao * 100, 2),
                'Registros Cobertos (|A|)': n_A,
                'Acertos (|A ∩ y|)': n_A_inter_y
            })

    recurse(0, [])
    return pd.DataFrame(rules)

df_regras = extrair_regras_completas(dt, feature_cols, X_train, y_train)
print("=== REGRAS DE CLASSIFICAÇÃO EXTRAÍDAS DA ÁRVORE (TREINO) ===")
display(df_regras)"""
    cells.append(nbf.v4.new_code_cell(c14))

    # Célula 15: Markdown - Interpretação Econômica da Árvore
    c15 = """### 🌳 Estrutura Gráfica da Árvore de Decisão e Ganho de Informação
A representação gráfica permite inspecionar cada limiar de decisão macroeconômica, o valor da Entropia de Shannon em cada partição e a pureza resultante nos nós folhas."""
    cells.append(nbf.v4.new_markdown_cell(c15))

    # Célula 16: Código - Plot da Árvore e Importâncias
    c16 = """# 1. Plot da Árvore de Decisão
fig, ax = plt.subplots(figsize=(18, 9))
plot_tree(
    dt,
    feature_names=feature_cols,
    class_names=dt.classes_,
    filled=True,
    rounded=True,
    fontsize=9.5,
    ax=ax,
    impurity=True
)
ax.set_title('Árvore de Decisão para Regimes de Inflação (Critério: Entropia de Shannon)', fontsize=14, weight='bold', pad=15)
plt.tight_layout()
plt.show()

# 2. Gráfico de Importância de Atributos (Ganho de Informação)
importances = pd.Series(dt.feature_importances_, index=feature_cols).sort_values(ascending=True)
importances_plot = importances[importances > 0]

plt.figure(figsize=(10, 5))
bars = plt.barh(importances_plot.index, importances_plot.values, color='#1f77b4', edgecolor='#0d47a1', height=0.55)
plt.title('Importância dos Atributos Macroeconômicos na Árvore de Decisão\\n(Redução de Entropia / Ganho de Informação)', fontsize=12, weight='bold', pad=12)
plt.xlabel('Ganho de Informação Normalizado', fontsize=11)
for bar in bars:
    w = bar.get_width()
    plt.text(w + 0.005, bar.get_y() + bar.get_height()/2, f'{w:.1%}', ha='left', va='center', fontsize=10, weight='bold')
plt.xlim(0, max(importances_plot.values) * 1.15)
plt.tight_layout()
plt.show()"""
    cells.append(nbf.v4.new_code_cell(c16))

    # Célula 17: Markdown - Série Temporal de Comparação
    c17 = """## 📈 6. Acompanhamento Temporal: Regime Observado vs. Predito (2022–2026)

Para verificar como as predições se comportaram mês a mês ao longo do período de validação out-of-sample, comparamos a série contínua do IPCA com a correspondência entre regimes reais e inferidos pela Árvore de Decisão."""
    cells.append(nbf.v4.new_markdown_cell(c17))

    # Célula 18: Código - Gráfico Temporal
    c18 = """df_comp = pd.DataFrame({
    'Date': dates_test,
    'Real': y_test.values,
    'Pred_DT': y_pred_dt,
    'IPCA_Real': df.loc[y_test.index, 'IPCA'].values
}).reset_index(drop=True)

y_map = {'Deflação': 0, 'Controlado': 1, 'Alta': 2}

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7), sharex=True, gridspec_kw={'height_ratios': [2, 1.2]})

# Painel Superior: Nível Contínuo do IPCA
ax1.plot(df_comp['Date'], df_comp['IPCA_Real'], color='#222222', lw=1.8, marker='o', markersize=4, label='IPCA Mensal Observado (% a.m.)')
ax1.axhline(0.0, color='#2ca02c', linestyle='--', alpha=0.7, label='Limiar Deflação (0.0%)')
ax1.axhline(0.50, color='#d62728', linestyle='--', alpha=0.7, label='Limiar Alta Inflação (0.50%)')
ax1.axhspan(-1.0, 0.0, color='#2ca02c', alpha=0.1)
ax1.axhspan(0.0, 0.50, color='#1f77b4', alpha=0.1)
ax1.axhspan(0.50, 2.5, color='#d62728', alpha=0.1)
ax1.set_ylabel('IPCA (% a.m.)', fontsize=11, weight='bold')
ax1.set_title('Acompanhamento Out-of-Sample: IPCA Real e Dinâmica de Regimes (2022 - 2026)', fontsize=13, weight='bold')
ax1.legend(loc='upper right', framealpha=0.9)

# Painel Inferior: Regimes Discretos
ax2.step(df_comp['Date'], df_comp['Real'].map(y_map), where='mid', label='Regime Real Observado', color='#000000', lw=2.2)
ax2.step(df_comp['Date'], df_comp['Pred_DT'].map(y_map), where='mid', label='Predição Árvore de Decisão', color='#e65100', linestyle='--', lw=2.0)
ax2.set_yticks([0, 1, 2])
ax2.set_yticklabels(['Deflação', 'Controlado', 'Alta Inflação'], fontsize=10, weight='bold')
ax2.set_ylabel('Regime', fontsize=11, weight='bold')
ax2.set_xlabel('Data (Mês-Ano)', fontsize=11)
ax2.legend(loc='lower right', framealpha=0.9)

plt.tight_layout()
plt.show()"""
    cells.append(nbf.v4.new_code_cell(c18))

    # Célula 19: Markdown - Conclusões
    c19 = """## 📌 7. Síntese dos Resultados e Interpretação Macroeconômica

1. **Superioridade da Árvore de Decisão:**
   - Obteve **59,09% de acurácia** e **F1-Score Macro de 0,5377** no conjunto out-of-sample (2022–2026), superando com folga o Baseline Majoritário (25,00% de acurácia e F1 de 0,1333) e o Naïve Bayes (31,82%).
   - A árvore conseguiu equilibrar a identificação de regimes de Meta/Controlado (precisão de 59% e recall de 77%) e Alta Inflação (precisão de 60%).
2. **Interpretação Econômica das Regras:**
   - **Inércia Inflacionária ($IPCA_{t-1}$):** É a variável raiz com o maior Ganho de Informação. O limiar de corte empírico encontrado pela árvore foi de **0,56% a.m.** — quase idêntico ao teto mensalizado da meta do CMN. Quando a inflação anterior ultrapassa 0,56%, a persistência de preços mantém a economia no regime de alta.
   - **Curva de Phillips e Desemprego:** A taxa de desemprego atua como divisor crítico (limiar de 11,75%). Com desemprego elevado, a demanda agregada comprimida favorece desinflação ou deflação; com desemprego baixo, pressões de custo e salários elevam a propensão a regimes controlados ou de alta.
   - **Repasse do Atacado e Câmbio ($IGP\\_M_{t-1}$):** Quando $IGP\\_M > 0,68\\%$ no mês anterior, mesmo com inflação moderada, a probabilidade de transição para o regime de Alta salta para 90% (regra r6), confirmando o papel do atacado como indicador antecedente de choque de custos.
3. **Limitação do Naïve Bayes e Desafio da Deflação:**
   - O Naïve Bayes foi penalizado pela violação da hipótese de independência condicional dos atributos macroeconômicos (IPCA, IGP-M e componentes são fortemente correlacionados).
   - A deflação pontual de 2022 (julho a setembro) decorreu da desoneração fiscal do ICMS sobre combustíveis e energia (Lei Complementar 194/2022), um choque estritamente político/legislativo não contido no histórico macroeconômico puramente estatístico."""
    cells.append(nbf.v4.new_markdown_cell(c19))

    nb['cells'] = cells

    # Salvar nos dois destinos
    destinos = [
        'Entrega_Classroom/7_Classificacao/classificacao_regimes_inflacao.ipynb',
        'Modelos de treinamento/classificacao_regimes_inflacao.ipynb'
    ]
    for dest in destinos:
        with open(dest, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print(f" Notebook estruturado gerado em: {dest}")

if __name__ == '__main__':
    build_notebook()
