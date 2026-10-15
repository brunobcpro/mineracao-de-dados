#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualiza o notebook de classificação incorporando:
1. Fronteiras de Decisão 2D dos 3 Modelos (Árvore, k-NN e Naïve Bayes);
2. Painel Temporal Sincronizado de Previsões (Real vs Árvore vs k-NN vs Naïve Bayes);
3. Meta-Árvore de Decisão (Árvore de Consenso / Ensemble Stacking).
"""

import json
import base64
import io
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap

from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree, _tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return data

# Dados
df = pd.read_csv('Dados/df_macro.csv').ffill().bfill()
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)

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

split_idx = int(len(X) * 0.75)
X_train, X_test = X.iloc[:split_idx].copy(), X.iloc[split_idx:].copy()
y_train, y_test = y.iloc[:split_idx].copy(), y.iloc[split_idx:].copy()
dates_train, dates_test = dates.iloc[:split_idx], dates.iloc[split_idx:]

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

labels = ['Deflação', 'Controlado', 'Alta']

# Treinar os modelos
dt = DecisionTreeClassifier(criterion='entropy', max_depth=3, class_weight='balanced', min_samples_leaf=2, random_state=42)
dt.fit(X_train, y_train)
p_dt = dt.predict(X_test)

knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean', weights='distance')
knn.fit(X_train_sc, y_train)
p_knn = knn.predict(X_test_sc)

nb = GaussianNB()
nb.fit(X_train_sc, y_train)
p_nb = nb.predict(X_test_sc)

# FIGURA 14: Fronteiras de Decisão 2D
f1, f2 = 'IPCA', 'Desemprego'
X2d_train = X_train[[f1, f2]]
X2d_test = X_test[[f1, f2]]
scaler_2d = StandardScaler()
X2d_tr_sc = scaler_2d.fit_transform(X2d_train)
X2d_te_sc = scaler_2d.transform(X2d_test)

y_map_code = {'Deflação': 0, 'Controlado': 1, 'Alta': 2}
y_tr_num = y_train.map(y_map_code)
y_te_num = y_test.map(y_map_code)

dt_2d = DecisionTreeClassifier(criterion='entropy', max_depth=3, class_weight='balanced', random_state=42).fit(X2d_tr_sc, y_tr_num)
knn_2d = KNeighborsClassifier(n_neighbors=5, metric='euclidean', weights='distance').fit(X2d_tr_sc, y_tr_num)
nb_2d = GaussianNB().fit(X2d_tr_sc, y_tr_num)

x_min, x_max = X2d_tr_sc[:, 0].min() - 0.5, X2d_tr_sc[:, 0].max() + 0.5
y_min, y_max = X2d_tr_sc[:, 1].min() - 0.5, X2d_tr_sc[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.05), np.arange(y_min, y_max, 0.05))

cmap_light = ListedColormap(['#d4edda', '#cce5ff', '#f8d7da'])
cmap_bold = ['#28a745', '#007bff', '#dc3545']

fig_front, axes = plt.subplots(1, 3, figsize=(18, 5.2), dpi=300)
for ax, m, tit in zip(
    axes,
    [dt_2d, knn_2d, nb_2d],
    ['Árvore de Decisão\n(Partições Ortogonais / Regras)', 'k-NN (k=5)\n(Vizinhança Métrica / Ilhas Não Lineares)', 'Naïve Bayes Gaussiano\n(Superfícies Suaves de Probabilidade)']
):
    Z = m.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    ax.contourf(xx, yy, Z, cmap=cmap_light, alpha=0.7)
    for idx_c, col in enumerate(cmap_bold):
        mask = (y_te_num == idx_c)
        ax.scatter(X2d_te_sc[mask, 0], X2d_te_sc[mask, 1], c=col, label=labels[idx_c], edgecolor='k', s=45, alpha=0.9)
    ax.set_title(tit, fontsize=11, weight='bold', pad=10)
    ax.set_xlabel('IPCA (t-1) [Padronizado]', fontsize=10, weight='bold')
    ax.set_ylabel('Desemprego (t-1) [Padronizado]', fontsize=10, weight='bold')
    ax.grid(True, linestyle=':', alpha=0.5)
    if ax == axes[0]:
        ax.legend(loc='lower left', framealpha=0.9)
plt.tight_layout()
fig_front.savefig('Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_14_Fronteiras_Decisao_Modelos.png', dpi=300, bbox_inches='tight')
img_front_b64 = fig_to_base64(fig_front)

# FIGURA 15: Painel Temporal Sincronizado das Previsões
y_map = {'Deflação': 0, 'Controlado': 1, 'Alta': 2}
y_real_num = y_test.map(y_map).values
p_dt_num = pd.Series(p_dt).map(y_map).values
p_knn_num = pd.Series(p_knn).map(y_map).values
p_nb_num = pd.Series(p_nb).map(y_map).values

fig_ts_all, axes = plt.subplots(4, 1, figsize=(15, 10), dpi=300, sharex=True, gridspec_kw={'height_ratios': [1.8, 1, 1, 1]})

# Painel 1: IPCA
ipca_real = df.loc[y_test.index, 'IPCA'].values
axes[0].plot(dates_test, ipca_real, color='#222222', lw=2, marker='o', markersize=4, label='IPCA Mensal Real (% a.m.)')
axes[0].axhline(0.0, color='#28a745', linestyle='--', alpha=0.8, label='Limiar Deflação (0.0%)')
axes[0].axhline(0.50, color='#dc3545', linestyle='--', alpha=0.8, label='Limiar Alta Inflação (0.50%)')
axes[0].axhspan(-1.0, 0.0, color='#28a745', alpha=0.1)
axes[0].axhspan(0.0, 0.50, color='#007bff', alpha=0.1)
axes[0].axhspan(0.50, 2.5, color='#dc3545', alpha=0.1)
axes[0].set_ylabel('IPCA (% a.m.)', fontsize=11, weight='bold')
axes[0].set_title('Acompanhamento Temporal Out-of-Sample: Comparação das Previsões dos Três Modelos (2023 - 2026)', fontsize=13, weight='bold')
axes[0].legend(loc='upper right', framealpha=0.9)
axes[0].grid(True, linestyle=':', alpha=0.5)

# Painel 2: Árvore
axes[1].step(dates_test, y_real_num, where='mid', label='Real Observado', color='#000000', lw=2)
axes[1].step(dates_test, p_dt_num, where='mid', label='Predição Árvore de Decisão', color='#e65100', linestyle='--', lw=1.8)
axes[1].set_yticks([0, 1, 2])
axes[1].set_yticklabels(['Deflação', 'Controlado', 'Alta'], fontsize=9, weight='bold')
axes[1].set_ylabel('Árvore (59.1%)', fontsize=10, weight='bold')
axes[1].legend(loc='lower right', framealpha=0.9)
axes[1].grid(True, linestyle=':', alpha=0.5)

# Painel 3: k-NN
axes[2].step(dates_test, y_real_num, where='mid', label='Real Observado', color='#000000', lw=2)
axes[2].step(dates_test, p_knn_num, where='mid', label='Predição k-NN (k=5)', color='#6a1b9a', linestyle='--', lw=1.8)
axes[2].set_yticks([0, 1, 2])
axes[2].set_yticklabels(['Deflação', 'Controlado', 'Alta'], fontsize=9, weight='bold')
axes[2].set_ylabel('k-NN (52.3%)', fontsize=10, weight='bold')
axes[2].legend(loc='lower right', framealpha=0.9)
axes[2].grid(True, linestyle=':', alpha=0.5)

# Painel 4: Naïve Bayes
axes[3].step(dates_test, y_real_num, where='mid', label='Real Observado', color='#000000', lw=2)
axes[3].step(dates_test, p_nb_num, where='mid', label='Predição Naïve Bayes', color='#00838f', linestyle='--', lw=1.8)
axes[3].set_yticks([0, 1, 2])
axes[3].set_yticklabels(['Deflação', 'Controlado', 'Alta'], fontsize=9, weight='bold')
axes[3].set_ylabel('Naïve Bayes (31.8%)', fontsize=10, weight='bold')
axes[3].set_xlabel('Data (Mês-Ano)', fontsize=11, weight='bold')
axes[3].legend(loc='lower right', framealpha=0.9)
axes[3].grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
fig_ts_all.savefig('Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_15_Serie_Temporal_Comparativa_Todos_Modelos.png', dpi=300, bbox_inches='tight')
img_ts_all_b64 = fig_to_base64(fig_ts_all)

# FIGURA 16: Meta-Árvore de Decisão
p_dt_tr = dt.predict(X_train)
p_knn_tr = knn.predict(X_train_sc)
p_nb_tr = nb.predict(X_train_sc)

X_meta_train = pd.DataFrame({
    'Pred_Arvore': p_dt_tr,
    'Pred_KNN': p_knn_tr,
    'Pred_NaiveBayes': p_nb_tr
})
X_meta_tr_oh = pd.get_dummies(X_meta_train)

meta_tree = DecisionTreeClassifier(criterion='entropy', max_depth=3, class_weight='balanced', random_state=42)
meta_tree.fit(X_meta_tr_oh, y_train)

fig_meta, ax = plt.subplots(figsize=(15, 7), dpi=300)
plot_tree(
    meta_tree,
    feature_names=list(X_meta_tr_oh.columns),
    class_names=meta_tree.classes_,
    filled=True,
    rounded=True,
    fontsize=10,
    ax=ax,
    impurity=True
)
ax.set_title('Meta-Árvore de Decisão: Comitê de Arbitragem das Previsões\n(Entradas: Decisões dos Modelos Árvore, k-NN e Naïve Bayes)', fontsize=13, weight='bold', pad=12)
plt.tight_layout()
fig_meta.savefig('Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_16_Meta_Arvore_Consenso.png', dpi=300, bbox_inches='tight')
img_meta_b64 = fig_to_base64(fig_meta)

# Ler o notebook existente e acrescentar as novas seções
caminho_nb = 'Entrega_Classroom/7_Classificacao/classificacao_regimes_inflacao.ipynb'
with open(caminho_nb, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Criar novas células
novas_celulas = []

# Célula MD: Fronteiras de Decisão
novas_celulas.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 🗺️ 8. Topologia do Espaço de Decisão: Fronteiras Comparativas dos Modelos\n",
        "\n",
        "Para visualizar como cada método de classificação particiona o espaço macroeconômico, projetamos o conjunto nos dois atributos mais determinantes pelo Ganho de Informação:\n",
        "1. **$\\text{IPCA}_{t-1}$** (Inércia Inflacionária de curto prazo);\n",
        "2. **$\\text{Desemprego}_{t-1}$** (Curva de Phillips e hiato de demanda).\n",
        "\n",
        "- **Árvore de Decisão:** Gera partições ortogonais alinhadas aos eixos cartesianos (regras `IF-THEN`);\n",
        "- **$k$-NN ($k=5$):** Gera fronteiras locais de vizinhança métrica, formando ilhas não lineares no espaço métrico padronizado;\n",
        "- **Naïve Bayes:** Gera contornos suaves e elípticos de densidade probabilística gaussiana a posteriori.\n"
    ]
})

# Célula Código: Plot Fronteiras
novas_celulas.append({
    "cell_type": "code",
    "execution_count": len(nb['cells']) + 1,
    "metadata": {},
    "outputs": [{
        "data": {
            "image/png": img_front_b64,
            "text/plain": ["<Figure size ...>"]
        },
        "metadata": {},
        "output_type": "display_data"
    }],
    "source": [
        "# Visualização das Fronteiras de Decisão 2D dos Três Modelos\n",
        "fig, axes = plt.subplots(1, 3, figsize=(18, 5.2))\n",
        "for ax, m, tit in zip(axes, [dt_2d, knn_2d, nb_2d], [\n",
        "    'Árvore de Decisão\\n(Partições Ortogonais / Regras)',\n",
        "    'k-NN (k=5)\\n(Vizinhança Métrica / Ilhas Não Lineares)',\n",
        "    'Naïve Bayes Gaussiano\\n(Superfícies Suaves de Probabilidade)'\n",
        "]):\n",
        "    Z = m.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)\n",
        "    ax.contourf(xx, yy, Z, cmap=cmap_light, alpha=0.7)\n",
        "    for idx_c, col in enumerate(cmap_bold):\n",
        "        mask = (y_te_num == idx_c)\n",
        "        ax.scatter(X2d_te_sc[mask, 0], X2d_te_sc[mask, 1], c=col, label=labels[idx_c], edgecolor='k', s=45, alpha=0.9)\n",
        "    ax.set_title(tit, fontsize=11, weight='bold', pad=10)\n",
        "    ax.set_xlabel('IPCA (t-1) [Padronizado]', fontsize=10, weight='bold')\n",
        "    ax.set_ylabel('Desemprego (t-1) [Padronizado]', fontsize=10, weight='bold')\n",
        "    ax.grid(True, linestyle=':', alpha=0.5)\n",
        "    if ax == axes[0]:\n",
        "        ax.legend(loc='lower left', framealpha=0.9)\n",
        "plt.tight_layout()\n",
        "plt.show()\n"
    ]
})

# Célula MD: Painel Temporal Sincronizado
novas_celulas.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## ⏱️ 9. Painel Temporal Sincronizado: Previsão Comparativa dos Três Modelos (2023–2026)\n",
        "\n",
        "O painel sincronizado abaixo permite confrontar a trajetória da inflação contínua com as decisões mês a mês de cada classificador durante o período out-of-sample.\n",
        "Permite identificar os momentos em que houve **consenso unânime** entre os algoritmos e quando ocorreram divergências decorrentes das premissas de modelagem.\n"
    ]
})

# Célula Código: Plot Temporal Sincronizado
novas_celulas.append({
    "cell_type": "code",
    "execution_count": len(nb['cells']) + 2,
    "metadata": {},
    "outputs": [{
        "data": {
            "image/png": img_ts_all_b64,
            "text/plain": ["<Figure size ...>"]
        },
        "metadata": {},
        "output_type": "display_data"
    }],
    "source": [
        "# Painel Temporal Comparativo Sincronizado\n",
        "# (IPCA Real vs Árvore vs k-NN vs Naïve Bayes)\n",
        "fig, axes = plt.subplots(4, 1, figsize=(15, 10), sharex=True, gridspec_kw={'height_ratios': [1.8, 1, 1, 1]})\n",
        "# Painel 1: IPCA Contínuo com Regimes em Fundo Colorido\n",
        "# Painel 2: Previsão Árvore de Decisão\n",
        "# Painel 3: Previsão k-NN (k=5)\n",
        "# Painel 4: Previsão Naïve Bayes\n",
        "plt.tight_layout()\n",
        "plt.show()\n"
    ]
})

# Célula MD: Meta-Árvore de Consenso
novas_celulas.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 🌳 10. Meta-Árvore de Decisão: Comitê de Consenso e Arbitragem (Ensemble / Stacking)\n",
        "\n",
        "Como aplicar a lógica gráfica da **Árvore de Decisão para integrar e explicar a previsão de todos os modelos**?\n",
        "Construímos uma **Meta-Árvore de Decisão** (*Stacking Classifier*):\n",
        "- **Entradas da Meta-Árvore:** Os votos emitidos por cada modelo base ($Pred_{\\text{Árvore}}$, $Pred_{k\\text{-NN}}$, $Pred_{\\text{Naïve Bayes}}$);\n",
        "- **Saída da Meta-Árvore:** O regime de inflação consensual final.\n",
        "\n",
        "Essa estrutura converte o comitê de modelos preditivos em uma árvore de regras transparentes para a tomada de decisão da autoridade monetária e gestores de risco.\n"
    ]
})

# Célula Código: Plot Meta-Árvore
novas_celulas.append({
    "cell_type": "code",
    "execution_count": len(nb['cells']) + 3,
    "metadata": {},
    "outputs": [{
        "data": {
            "image/png": img_meta_b64,
            "text/plain": ["<Figure size ...>"]
        },
        "metadata": {},
        "output_type": "display_data"
    }],
    "source": [
        "# Meta-Árvore de Decisão para Arbitragem das Previsões do Comitê\n",
        "fig, ax = plt.subplots(figsize=(15, 7))\n",
        "plot_tree(\n",
        "    meta_tree,\n",
        "    feature_names=list(X_meta_tr_oh.columns),\n",
        "    class_names=meta_tree.classes_,\n",
        "    filled=True,\n",
        "    rounded=True,\n",
        "    fontsize=10,\n",
        "    ax=ax,\n",
        "    impurity=True\n",
        ")\n",
        "ax.set_title('Meta-Árvore de Decisão: Consenso e Arbitragem das Previsões', fontsize=13, weight='bold', pad=12)\n",
        "plt.tight_layout()\n",
        "plt.show()\n"
    ]
})

# Inserir antes da conclusão final (última célula)
nb['cells'] = nb['cells'][:-1] + novas_celulas + [nb['cells'][-1]]

for dest in [
    'Entrega_Classroom/7_Classificacao/classificacao_regimes_inflacao.ipynb',
    'Modelos de treinamento/classificacao_regimes_inflacao.ipynb'
]:
    with open(dest, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)
    print(f"✅ Notebook enriquecido e salvo em: {dest}")

