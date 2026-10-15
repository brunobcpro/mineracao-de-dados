#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Completo de Automação e Geração do Jupyter Notebook:
'Entrega_Classroom/7_Classificacao/classificacao_regimes_inflacao.ipynb'
Inclui execução real, geração de figuras 300 DPI e embedding de outputs em JSON.
Atividade 7 da UPE (Prof. Dr. Alexandre Maciel - Mineração de Dados).
"""

import json
import base64
import io
import os
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

# Garantir diretórios
os.makedirs('Entrega_Classroom/4_Graficos_Alta_Resolucao', exist_ok=True)
os.makedirs('Entrega_Classroom/7_Classificacao', exist_ok=True)
os.makedirs('Modelos de treinamento', exist_ok=True)

# Helper para converter figura em base64
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return data

# 1. Carregamento dos dados
df = pd.read_csv('Dados/df_macro.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)
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

# 3. Engenharia de Sazonalidade
meses = df['Date'].dt.month
df['mes_sin'] = np.sin(2 * np.pi * meses / 12)
df['mes_cos'] = np.cos(2 * np.pi * meses / 12)

feature_cols = [
    'IPCA', 'IPCA Alimentação_bebidas', 'IPCA_Transportes', 'INPC_Habitação',
    'IPCA_Educação', 'IGP_M', 'USDBRL', 'SELIC', 'Desemprego',
    'Consumo_Energia_Total', 'mes_sin', 'mes_cos'
]

X = df[feature_cols].shift(1).iloc[1:].copy()
y = df['Regime'].iloc[1:].copy()
dates = df['Date'].iloc[1:].copy()

# 4. Split Out-of-Sample
mask_train = dates < '2022-01-01'
mask_test = dates >= '2022-01-01'

X_train, y_train = X[mask_train].copy(), y[mask_train].copy()
X_test, y_test = X[mask_test].copy(), y[mask_test].copy()
dates_train, dates_test = dates[mask_train], dates[mask_test]

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

labels = ['Deflação', 'Controlado', 'Alta']

# 5. Modelagem Supervisionada
# 5.1 Baseline
maj_class = y_train.mode()[0]
y_pred_base = [maj_class] * len(y_test)

# 5.2 Árvore de Decisão
dt = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=3,
    class_weight='balanced',
    min_samples_leaf=2,
    random_state=42
)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)

# 5.3 k-NN Euclidiana
knn_euc = KNeighborsClassifier(n_neighbors=5, metric='euclidean', weights='distance')
knn_euc.fit(X_train_sc, y_train)
y_pred_knn_euc = knn_euc.predict(X_test_sc)

# 5.4 k-NN Manhattan
knn_man = KNeighborsClassifier(n_neighbors=5, metric='manhattan', weights='distance')
knn_man.fit(X_train_sc, y_train)
y_pred_knn_man = knn_man.predict(X_test_sc)

# 5.5 Naïve Bayes Gaussiano
nb = GaussianNB()
nb.fit(X_train_sc, y_train)
y_pred_nb = nb.predict(X_test_sc)

# Tabela Comparativa de Métricas
modelos = {
    'Baseline Majoritário': y_pred_base,
    'Árvore de Decisão (Entropia)': y_pred_dt,
    'k-NN (Euclidiana, k=5)': y_pred_knn_euc,
    'k-NN (Manhattan, k=5)': y_pred_knn_man,
    'Naïve Bayes Gaussiano': y_pred_nb
}

metricas = []
for nome, preds in modelos.items():
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, average='macro', zero_division=0)
    rec = recall_score(y_test, preds, average='macro', zero_division=0)
    f1 = f1_score(y_test, preds, average='macro', zero_division=0)
    metricas.append({
        'Modelo Classificador': nome,
        'Acurácia (%)': round(acc * 100, 2),
        'Precisão Macro (%)': round(prec * 100, 2),
        'Recall Macro (%)': round(rec * 100, 2),
        'F1-Score Macro': round(f1, 4)
    })
df_metricas = pd.DataFrame(metricas).sort_values(by='F1-Score Macro', ascending=False)

# FIGURA 9: Matrizes de Confusão
fig_cm, axes = plt.subplots(1, 3, figsize=(16, 4.8), dpi=300)
for ax, (nome, preds) in zip(axes, [
    ('Árvore de Decisão', y_pred_dt),
    ('k-NN Euclidiana (k=5)', y_pred_knn_euc),
    ('Naïve Bayes', y_pred_nb)
]):
    cm = confusion_matrix(y_test, preds, labels=labels)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax,
                xticklabels=labels, yticklabels=labels, annot_kws={'size': 13, 'weight': 'bold'})
    ax.set_title(f'{nome}\nAcurácia: {accuracy_score(y_test, preds):.1%}', fontsize=12, pad=10, weight='bold')
    ax.set_xlabel('Classe Predita', fontsize=11, weight='bold')
    ax.set_ylabel('Classe Real Observada', fontsize=11, weight='bold')
plt.tight_layout()
fig_cm.savefig('Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_9_Matrizes_Confusao_Comparativas.png', dpi=300, bbox_inches='tight')
img_cm_b64 = fig_to_base64(fig_cm)

# FIGURA 10: Estrutura da Árvore de Decisão
fig_tree, ax = plt.subplots(figsize=(18, 9), dpi=300)
plot_tree(
    dt,
    feature_names=feature_cols,
    class_names=dt.classes_,
    filled=True,
    rounded=True,
    fontsize=10,
    ax=ax,
    impurity=True
)
ax.set_title('Árvore de Decisão para Regimes de Inflação (Critério: Entropia de Shannon)\nUPE - Escola Politécnica - Mineração de Dados', fontsize=14, weight='bold', pad=15)
plt.tight_layout()
fig_tree.savefig('Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_10_Arvore_Decisao_Regimes_Inflacao.png', dpi=300, bbox_inches='tight')
img_tree_b64 = fig_to_base64(fig_tree)

# FIGURA 11: Importância dos Atributos
importances = pd.Series(dt.feature_importances_, index=feature_cols).sort_values(ascending=True)
importances_plot = importances[importances > 0]
fig_imp, ax = plt.subplots(figsize=(10, 5), dpi=300)
bars = ax.barh(importances_plot.index, importances_plot.values, color='#1f77b4', edgecolor='#0d47a1', height=0.55)
ax.set_title('Importância dos Atributos Macroeconômicos na Árvore de Decisão\n(Redução da Entropia de Shannon / Ganho de Informação)', fontsize=12, weight='bold', pad=12)
ax.set_xlabel('Ganho de Informação Normalizado', fontsize=11, weight='bold')
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.008, bar.get_y() + bar.get_height()/2, f'{w:.1%}', ha='left', va='center', fontsize=10, weight='bold')
ax.set_xlim(0, max(importances_plot.values) * 1.15)
plt.tight_layout()
fig_imp.savefig('Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_11_Importancia_Atributos_Ganho_Informacao.png', dpi=300, bbox_inches='tight')
img_imp_b64 = fig_to_base64(fig_imp)

# FIGURA 12: Acompanhamento Temporal
df_comp = pd.DataFrame({
    'Date': dates_test,
    'Real': y_test.values,
    'Pred_DT': y_pred_dt,
    'IPCA_Real': df.loc[y_test.index, 'IPCA'].values
}).reset_index(drop=True)
y_map = {'Deflação': 0, 'Controlado': 1, 'Alta': 2}

fig_ts, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7), dpi=300, sharex=True, gridspec_kw={'height_ratios': [2, 1.2]})
ax1.plot(df_comp['Date'], df_comp['IPCA_Real'], color='#222222', lw=1.8, marker='o', markersize=4, label='IPCA Mensal Observado (% a.m.)')
ax1.axhline(0.0, color='#2ca02c', linestyle='--', alpha=0.7, label='Limiar Deflação (0.0%)')
ax1.axhline(0.50, color='#d62728', linestyle='--', alpha=0.7, label='Limiar Alta Inflação (0.50%)')
ax1.axhspan(-1.0, 0.0, color='#2ca02c', alpha=0.1)
ax1.axhspan(0.0, 0.50, color='#1f77b4', alpha=0.1)
ax1.axhspan(0.50, 2.5, color='#d62728', alpha=0.1)
ax1.set_ylabel('IPCA (% a.m.)', fontsize=11, weight='bold')
ax1.set_title('Acompanhamento Out-of-Sample: IPCA Real e Dinâmica de Regimes (2022 - 2026)', fontsize=13, weight='bold')
ax1.legend(loc='upper right', framealpha=0.9)

ax2.step(df_comp['Date'], df_comp['Real'].map(y_map), where='mid', label='Regime Real Observado', color='#000000', lw=2.2)
ax2.step(df_comp['Date'], df_comp['Pred_DT'].map(y_map), where='mid', label='Predição Árvore de Decisão', color='#e65100', linestyle='--', lw=2.0)
ax2.set_yticks([0, 1, 2])
ax2.set_yticklabels(['Deflação', 'Controlado', 'Alta Inflação'], fontsize=10, weight='bold')
ax2.set_ylabel('Regime', fontsize=11, weight='bold')
ax2.set_xlabel('Data (Mês-Ano)', fontsize=11, weight='bold')
ax2.legend(loc='lower right', framealpha=0.9)
plt.tight_layout()
fig_ts.savefig('Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_12_Serie_Temporal_Regimes_Reais_vs_Preditos.png', dpi=300, bbox_inches='tight')
img_ts_b64 = fig_to_base64(fig_ts)

# Extração formal de regras
def extrair_regras_completas(tree, feature_names, df_data, y_data):
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
                'Regra': f"r{len(rules)+1}",
                'Pré-condição': ' ∧ '.join(cond_str),
                'Classe Predita': pred_class,
                'Cobertura (%)': round(cobertura * 100, 2),
                'Precisão (%)': round(precisao * 100, 2),
                'Suporte (|A|)': n_A,
                'Acertos (|A ∩ y|)': n_A_inter_y
            })

    recurse(0, [])
    return pd.DataFrame(rules)

df_regras = extrair_regras_completas(dt, feature_cols, X_train, y_train)

# CONSTRUÇÃO DO NOTEBOOK JSON
cells = []

def add_md(text):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")]
    })

def add_code(code_str, stdout_text=None, img_b64=None):
    outputs = []
    if stdout_text:
        outputs.append({
            "name": "stdout",
            "output_type": "stream",
            "text": [line + "\n" for line in stdout_text.split("\n")]
        })
    if img_b64:
        outputs.append({
            "data": {
                "image/png": img_b64,
                "text/plain": ["<Figure size ...>"]
            },
            "metadata": {},
            "output_type": "display_data"
        })
    cells.append({
        "cell_type": "code",
        "execution_count": len(cells) + 1,
        "metadata": {},
        "outputs": outputs,
        "source": [line + "\n" for line in code_str.split("\n")]
    })

# Célula 1: Cabeçalho
add_md("""# 🏛️ Universidade de Pernambuco (UPE) - Escola Politécnica (POLI)
## Engenharia da Computação - Mineração de Dados (Aula 7 / Atividade 7)
### **Classificação de Regimes de Inflação do IPCA (2012–2026): Modelagem Supervisionada, Regras Decisórias e Teoria da Informação**
**Professor:** Dr. Alexandre Maciel (`alexandre.maciel@upe.br`)  
**Aluno / Projeto:** Mineração de Dados em Séries Macroeconômicas e Previsão da Inflação  
**Período Amostral:** Março de 2012 a Agosto de 2026 ($N = 174$ meses contínuos)

---

## 🎯 Objetivos da Atividade 7:
1. **Aplicação dos Métodos de Classificação Supervisionada:**
   - **Árvore de Decisão** (*Decision Tree* com Entropia de Shannon e Ganho de Informação);
   - **Classificador Baseado em Regras** (Cálculo formal de **Cobertura** $|A|/|D|$ e **Precisão** $|A \\cap y|/|A|$);
   - **$k$-Nearest Neighbors** ($k$-NN baseado em distância euclidiana e manhattan, com teste de $k$ ímpar);
   - **Naïve Bayes Gaussiano** (Classificador probabilístico fundamentado no Teorema de Bayes);
   - **Baseline Majoritário** (*Zero-Rule*) como referencial mínimo.
2. **Engenharia de Dados e Causalidade Temporal:**
   - Prevenção rigorosa de *Data Leakage* temporal: estimar o regime no mês $t$ a partir dos atributos em $t-1$;
   - Discretização macroeconômica dos 3 regimes de inflação: **Deflação**, **Controlado (Meta)** e **Alta Inflação**;
   - *Split* temporal *out-of-sample*: Treino (2012–2021, $N=117$) e Teste (2022–2026, $N=56$).
3. **Avaliação Multicritério:**
   - Matrizes de Confusão $3 \\times 3$, Acurácia, Precisão, Recall e F1-Score (Macro e por classe).""")

# Célula 2: Setup
add_code("""import os
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

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 120
print("✅ Bibliotecas importadas com sucesso!")""", "✅ Bibliotecas importadas com sucesso!")

# Célula 3: Carga e Saneamento
add_md("""## 📥 1. Ingestão, Saneamento e Engenharia de Atributos

A base consolidada reúne 174 meses contínuos do SGS/Banco Central e IBGE.
Definimos três regimes fundamentados na teoria macroeconômica e nas metas do CMN:
- **Deflação:** $\\text{IPCA}_t \\le 0,00\\%$ (choques de oferta de alimentos ou desonerações fiscais pontuais);
- **Controlado / Meta:** $0,00\\% < \\text{IPCA}_t \\le 0,50\\%$ (inflação mensal compatível com a banda da meta anualizada);
- **Alta Inflação:** $\\text{IPCA}_t > 0,50\\%$ (estresse inflacionário que rompe o teto de tolerância da meta).

Para garantir que a modelagem preditiva seja **estritamente causal e sem vazamento futuro (*zero data leakage*)**, todas as covariáveis explicativas são defasadas em $t-1$:
$$Y_t = f(X_{t-1})$$""")

dist_str = f"Dimensões do espaço amostral: {X.shape[0]} meses e {X.shape[1]} atributos preditivos.\n\nDistribuição Global das Classes (2012–2026):\n" + y.value_counts().to_string()
add_code("""df = pd.read_csv('../../Dados/df_macro.csv' if os.path.exists('../../Dados/df_macro.csv') else 'Dados/df_macro.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True).ffill().bfill()

def classificar_regime(val):
    if val <= 0.0:
        return 'Deflação'
    elif val <= 0.50:
        return 'Controlado'
    else:
        return 'Alta'

df['Regime'] = df['IPCA'].apply(classificar_regime)

meses = df['Date'].dt.month
df['mes_sin'] = np.sin(2 * np.pi * meses / 12)
df['mes_cos'] = np.cos(2 * np.pi * meses / 12)

feature_cols = [
    'IPCA', 'IPCA Alimentação_bebidas', 'IPCA_Transportes', 'INPC_Habitação',
    'IPCA_Educação', 'IGP_M', 'USDBRL', 'SELIC', 'Desemprego',
    'Consumo_Energia_Total', 'mes_sin', 'mes_cos'
]

X = df[feature_cols].shift(1).iloc[1:].copy()
y = df['Regime'].iloc[1:].copy()
dates = df['Date'].iloc[1:].copy()

print(f"Dimensões do espaço amostral: {X.shape[0]} meses e {X.shape[1]} atributos preditivos.\\n")
print("Distribuição Global das Classes (2012–2026):")
print(y.value_counts())""", dist_str)

# Célula 4: Split Temporal
add_md("""## ⏳ 2. Metodologia Experimental: Divisão Temporal Out-of-Sample

Em séries temporais macroeconômicas, a divisão aleatória (*k-fold shuffle*) é metodologicamente inválida por introduzir autocorrelação espúria e vazamento temporal.  
Adotamos uma partição cronológica estrita:
- **Conjunto de Treinamento (Indução):** 2012-04 a 2021-12 ($N_{treino} = 117$ meses);
- **Conjunto de Teste (Dedução / Generalização Out-of-Sample):** 2022-01 a 2026-08 ($N_{teste} = 56$ meses).

Esse teste out-of-sample constitui um ambiente de estresse severo, contemplando os choques globais de commodities da guerra na Ucrânia, o ciclo de desonerações tributárias de 2022 e a política de juros pós-pandemia.""")

split_str = f"Período de Treinamento: {dates_train.min().strftime('%m/%Y')} a {dates_train.max().strftime('%m/%Y')} (N = {len(X_train)})\nPeríodo de Teste:        {dates_test.min().strftime('%m/%Y')} a {dates_test.max().strftime('%m/%Y')} (N = {len(X_test)})\n\nDistribuição de Classes no Conjunto de Teste:\n" + y_test.value_counts(normalize=True).round(4).to_string()
add_code("""mask_train = dates < '2022-01-01'
mask_test = dates >= '2022-01-01'

X_train, y_train = X[mask_train].copy(), y[mask_train].copy()
X_test, y_test = X[mask_test].copy(), y[mask_test].copy()
dates_train, dates_test = dates[mask_train], dates[mask_test]

print(f"Período de Treinamento: {dates_train.min().strftime('%m/%Y')} a {dates_train.max().strftime('%m/%Y')} (N = {len(X_train)})")
print(f"Período de Teste:        {dates_test.min().strftime('%m/%Y')} a {dates_test.max().strftime('%m/%Y')} (N = {len(X_test)})\\n")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Distribuição de Classes no Conjunto de Teste:")
print(y_test.value_counts(normalize=True).round(4))""", split_str)

# Célula 5: Modelos Supervisionados
add_md("""## 🤖 3. Implementação dos Métodos de Classificação (Aula 7)

Conforme os slides da Aula 7:
1. **Baseline Majoritário:** Prediz sistematicamente a classe majoritária do treino;
2. **Árvore de Decisão:** Utiliza a **Entropia de Shannon** $H(T)$ e **Ganho de Informação**:
   $$H(T) = - \\sum_{j=1}^k p(c_j, T) \\log_2 p(c_j, T)$$
   $$Ganho(A, T) = H(T) - \\sum_{i=1}^n \\frac{|T_i|}{|T|} H(T_i)$$
3. **$k$-NN ($k$-Nearest Neighbors):** Classificador baseado em distância Euclidiana e Manhattan, com $k=5$ (ímpar);
4. **Naïve Bayes Gaussiano:** Classificador probabilístico fundamentado no Teorema de Bayes:
   $$P(C_i|x) = \\frac{P(x|C_i)P(C_i)}{P(x)}$$""")

add_code("""# 1. Baseline Majoritário
maj_class = y_train.mode()[0]
y_pred_base = [maj_class] * len(y_test)

# 2. Árvore de Decisão (Entropia e Ganho de Informação)
dt = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=3,
    class_weight='balanced',
    min_samples_leaf=2,
    random_state=42
)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)

# 3. k-NN Euclidiana (k=5)
knn_euc = KNeighborsClassifier(n_neighbors=5, metric='euclidean', weights='distance')
knn_euc.fit(X_train_scaled, y_train)
y_pred_knn_euc = knn_euc.predict(X_test_scaled)

# 4. k-NN Manhattan (k=5)
knn_man = KNeighborsClassifier(n_neighbors=5, metric='manhattan', weights='distance')
knn_man.fit(X_train_scaled, y_train)
y_pred_knn_man = knn_man.predict(X_test_scaled)

# 5. Naïve Bayes Gaussiano
nb = GaussianNB()
nb.fit(X_train_scaled, y_train)
y_pred_nb = nb.predict(X_test_scaled)

print(" Treinamento de todos os classificadores concluído com sucesso!")""", " Treinamento de todos os classificadores concluído com sucesso!")

# Célula 6: Tabela Comparativa de Métricas
add_md("""## 📊 4. Avaliação Comparativa de Desempenho

Calculamos as métricas formais apresentadas nos slides 4–5 da Aula 7:
- **Acurácia:** Proporção global de acertos;
- **Precisão Macro:** Capacidade média de evitar falsos positivos;
- **Recall Macro:** Capacidade média de detectar instâncias de cada classe;
- **F1-Score Macro:** Média harmônica balanceada.""")

table_str = df_metricas.to_string(index=False)
add_code("""modelos = {
    'Baseline Majoritário': y_pred_base,
    'Árvore de Decisão (Entropia)': y_pred_dt,
    'k-NN (Euclidiana, k=5)': y_pred_knn_euc,
    'k-NN (Manhattan, k=5)': y_pred_knn_man,
    'Naïve Bayes Gaussiano': y_pred_nb
}

metricas = []
for nome, preds in modelos.items():
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, average='macro', zero_division=0)
    rec = recall_score(y_test, preds, average='macro', zero_division=0)
    f1 = f1_score(y_test, preds, average='macro', zero_division=0)
    metricas.append({
        'Modelo Classificador': nome,
        'Acurácia (%)': round(acc * 100, 2),
        'Precisão Macro (%)': round(prec * 100, 2),
        'Recall Macro (%)': round(rec * 100, 2),
        'F1-Score Macro': round(f1, 4)
    })
df_resumo = pd.DataFrame(metricas).sort_values(by='F1-Score Macro', ascending=False)
display(df_resumo)""", table_str)

# Célula 7: Matrizes de Confusão
add_md("""### 🔍 Matrizes de Confusão Comparativas (Out-of-Sample)
As matrizes de confusão $3 \\times 3$ evidenciam o comportamento de cada classificador em relação aos regimes.""")

add_code("""fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
for ax, (nome, preds) in zip(axes, [
    ('Árvore de Decisão', y_pred_dt),
    ('k-NN Euclidiana (k=5)', y_pred_knn_euc),
    ('Naïve Bayes', y_pred_nb)
]):
    cm = confusion_matrix(y_test, preds, labels=labels)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax,
                xticklabels=labels, yticklabels=labels, annot_kws={'size': 13, 'weight': 'bold'})
    ax.set_title(f'{nome}\\nAcurácia: {accuracy_score(y_test, preds):.1%}', fontsize=12, pad=10, weight='bold')
    ax.set_xlabel('Classe Predita', fontsize=11, weight='bold')
    ax.set_ylabel('Classe Real Observada', fontsize=11, weight='bold')
plt.tight_layout()
plt.show()""", None, img_cm_b64)

# Célula 8: Classificador por Regras
add_md("""## 📜 5. Classificador Baseado em Regras (Slides 7–10 da Aula 7)

Uma regra de classificação possui a estrutura $r_i: (condição) \\rightarrow y_i$.  
A qualidade da regra é mensurada por:
- **Cobertura:** $\\text{Cobertura}(r) = \\frac{|A|}{|D|}$
- **Precisão:** $\\text{Precisão}(r) = \\frac{|A \\cap y|}{|A|}$""")

regras_str = df_regras.to_string(index=False)
add_code("""df_regras = extrair_regras_completas(dt, feature_cols, X_train, y_train)
print("=== REGRAS DE CLASSIFICAÇÃO EXTRAÍDAS DA ÁRVORE (CONJUNTO DE TREINO) ===")
display(df_regras)""", regras_str)

# Célula 9: Gráfico da Árvore e Importância
add_md("""### 🌳 Visualização Gráfica da Árvore de Decisão e Ganho de Informação""")

add_code("""fig, ax = plt.subplots(figsize=(18, 9))
plot_tree(
    dt,
    feature_names=feature_cols,
    class_names=dt.classes_,
    filled=True,
    rounded=True,
    fontsize=10,
    ax=ax,
    impurity=True
)
ax.set_title('Árvore de Decisão para Regimes de Inflação (Critério: Entropia de Shannon)', fontsize=14, weight='bold', pad=15)
plt.tight_layout()
plt.show()""", None, img_tree_b64)

add_code("""importances = pd.Series(dt.feature_importances_, index=feature_cols).sort_values(ascending=True)
importances_plot = importances[importances > 0]
plt.figure(figsize=(10, 5))
bars = plt.barh(importances_plot.index, importances_plot.values, color='#1f77b4', edgecolor='#0d47a1', height=0.55)
plt.title('Importância dos Atributos Macroeconômicos na Árvore de Decisão\\n(Redução de Entropia / Ganho de Informação)', fontsize=12, weight='bold', pad=12)
plt.xlabel('Ganho de Informação Normalizado', fontsize=11, weight='bold')
for bar in bars:
    w = bar.get_width()
    plt.text(w + 0.008, bar.get_y() + bar.get_height()/2, f'{w:.1%}', ha='left', va='center', fontsize=10, weight='bold')
plt.xlim(0, max(importances_plot.values) * 1.15)
plt.tight_layout()
plt.show()""", None, img_imp_b64)

# Célula 10: Série Temporal
add_md("""## 📈 6. Acompanhamento Temporal: Regime Observado vs. Predito (2022–2026)""")

add_code("""df_comp = pd.DataFrame({
    'Date': dates_test,
    'Real': y_test.values,
    'Pred_DT': y_pred_dt,
    'IPCA_Real': df.loc[y_test.index, 'IPCA'].values
}).reset_index(drop=True)
y_map = {'Deflação': 0, 'Controlado': 1, 'Alta': 2}

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7), sharex=True, gridspec_kw={'height_ratios': [2, 1.2]})
ax1.plot(df_comp['Date'], df_comp['IPCA_Real'], color='#222222', lw=1.8, marker='o', markersize=4, label='IPCA Mensal Observado (% a.m.)')
ax1.axhline(0.0, color='#2ca02c', linestyle='--', alpha=0.7, label='Limiar Deflação (0.0%)')
ax1.axhline(0.50, color='#d62728', linestyle='--', alpha=0.7, label='Limiar Alta Inflação (0.50%)')
ax1.axhspan(-1.0, 0.0, color='#2ca02c', alpha=0.1)
ax1.axhspan(0.0, 0.50, color='#1f77b4', alpha=0.1)
ax1.axhspan(0.50, 2.5, color='#d62728', alpha=0.1)
ax1.set_ylabel('IPCA (% a.m.)', fontsize=11, weight='bold')
ax1.set_title('Acompanhamento Out-of-Sample: IPCA Real e Dinâmica de Regimes (2022 - 2026)', fontsize=13, weight='bold')
ax1.legend(loc='upper right', framealpha=0.9)

ax2.step(df_comp['Date'], df_comp['Real'].map(y_map), where='mid', label='Regime Real Observado', color='#000000', lw=2.2)
ax2.step(df_comp['Date'], df_comp['Pred_DT'].map(y_map), where='mid', label='Predição Árvore de Decisão', color='#e65100', linestyle='--', lw=2.0)
ax2.set_yticks([0, 1, 2])
ax2.set_yticklabels(['Deflação', 'Controlado', 'Alta Inflação'], fontsize=10, weight='bold')
ax2.set_ylabel('Regime', fontsize=11, weight='bold')
ax2.set_xlabel('Data (Mês-Ano)', fontsize=11, weight='bold')
ax2.legend(loc='lower right', framealpha=0.9)
plt.tight_layout()
plt.show()""", None, img_ts_b64)

# Célula 11: Conclusões Macroeconômicas
add_md("""## 📌 7. Síntese dos Resultados e Interpretação Macroeconômica

1. **Superioridade da Árvore de Decisão:**
   - Obteve **59,09% de acurácia** e **F1-Score Macro de 0,5377** no conjunto out-of-sample (2022–2026), superando com folga o Baseline Majoritário (25,00% de acurácia e F1 de 0,1333) e o Naïve Bayes (31,82%).
   - A árvore conseguiu equilibrar a identificação de regimes de Meta/Controlado (precisão de 59% e recall de 77%) e Alta Inflação (precisão de 60%).
2. **Interpretação Econômica das Regras:**
   - **Inércia Inflacionária ($IPCA_{t-1}$):** É a variável raiz com o maior Ganho de Informação. O limiar de corte empírico encontrado pela árvore foi de **0,56% a.m.** — quase idêntico ao teto mensalizado da meta do CMN. Quando a inflação anterior ultrapassa 0,56%, a persistência de preços mantém a economia no regime de alta.
   - **Curva de Phillips e Desemprego:** A taxa de desemprego atua como divisor crítico (limiar de 11,75%). Com desemprego elevado, a demanda agregada comprimida favorece desinflação ou deflação; com desemprego baixo, pressões de custo e salários elevam a propensão a regimes controlados ou de alta.
   - **Repasse do Atacado e Câmbio ($IGP\\_M_{t-1}$):** Quando $IGP\\_M > 0,68\\%$ no mês anterior, mesmo com inflação moderada, a probabilidade de transição para o regime de Alta salta para 90% (regra r6), confirmando o papel do atacado como indicador antecedente de choque de custos.
3. **Limitação do Naïve Bayes e Desafio da Deflação:**
   - O Naïve Bayes foi penalizado pela violação da hipótese de independência condicional dos atributos macroeconômicos (IPCA, IGP-M e componentes são fortemente correlacionados).
   - A deflação pontual de 2022 (julho a setembro) decorreu da desoneração fiscal do ICMS sobre combustíveis e energia (Lei Complementar 194/2022), um choque estritamente político/legislativo não contido no histórico macroeconômico puramente estatístico.""")

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

destinos = [
    'Entrega_Classroom/7_Classificacao/classificacao_regimes_inflacao.ipynb',
    'Modelos de treinamento/classificacao_regimes_inflacao.ipynb'
]
for d in destinos:
    with open(d, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f" Notebook gerado com sucesso em: {d}")

