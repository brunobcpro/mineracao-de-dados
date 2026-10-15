#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Automação para Classificação de Regimes de Inflação (Atividade 7 - UPE)
Gera o notebook Jupyter com execução completa e as figuras em alta resolução (300 DPI).
"""

import os
import json
import base64
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
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

# Configuração de estilo visual
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

os.makedirs('Entrega_Classroom/4_Graficos_Alta_Resolucao', exist_ok=True)
os.makedirs('Entrega_Classroom/7_Classificacao', exist_ok=True)
os.makedirs('Modelos de treinamento', exist_ok=True)

# 1. Carregamento dos dados
df = pd.read_csv('Dados/df_macro.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)
df = df.ffill().bfill()

# 2. Definição do Target Supervisionado (Regime de Inflação)
def classificar_regime(val):
    if val <= 0.0:
        return 'Deflação'
    elif val <= 0.50:
        return 'Controlado'
    else:
        return 'Alta'

df['Regime'] = df['IPCA'].apply(classificar_regime)

# 3. Engenharia de Atributos e Sazonalidade
meses = df['Date'].dt.month
df['mes_sin'] = np.sin(2 * np.pi * meses / 12)
df['mes_cos'] = np.cos(2 * np.pi * meses / 12)

feature_cols = [
    'IPCA', 'IPCA Alimentação_bebidas', 'IPCA_Transportes', 'INPC_Habitação',
    'IPCA_Educação', 'IGP_M', 'USDBRL', 'SELIC', 'Desemprego',
    'Consumo_Energia_Total', 'mes_sin', 'mes_cos'
]

# Defasagem estrita em t-1
X = df[feature_cols].shift(1).iloc[1:].copy()
y = df['Regime'].iloc[1:].copy()
dates = df['Date'].iloc[1:].copy()

split_idx = int(len(X) * 0.75)  # 129 treino (~75%), 44 teste (~25%)
X_train, X_test = X.iloc[:split_idx].copy(), X.iloc[split_idx:].copy()
y_train, y_test = y.iloc[:split_idx].copy(), y.iloc[split_idx:].copy()
dates_train, dates_test = dates.iloc[:split_idx], dates.iloc[split_idx:]

labels = ['Deflação', 'Controlado', 'Alta']

# 4. Modelos Supervisionados
# 4.1 Baseline Majoritário
majoritaria = y_train.mode()[0]
y_pred_base = [majoritaria] * len(y_test)

# 4.2 Árvore de Decisão (Entropia e Ganho de Informação)
dt = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=3,
    class_weight='balanced',
    min_samples_leaf=2,
    random_state=42
)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)

# 4.3 Naïve Bayes Gaussiano
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc = scaler.transform(X_test)

nb = GaussianNB()
nb.fit(X_train_sc, y_train)
y_pred_nb = nb.predict(X_test_sc)

# 4.4 k-NN (k=5)
knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean', weights='distance')
knn.fit(X_train_sc, y_train)
y_pred_knn = knn.predict(X_test_sc)

# 4.5 k-NN Manhattan (k=5)
knn_man = KNeighborsClassifier(n_neighbors=5, metric='manhattan', weights='distance')
knn_man.fit(X_train_sc, y_train)
y_pred_knn_man = knn_man.predict(X_test_sc)

# Resumo de Desempenho
models_dict = {
    'Baseline Majoritário': y_pred_base,
    'Árvore de Decisão (Entropia)': y_pred_dt,
    'k-NN (Euclidiana, k=5)': y_pred_knn,
    'k-NN (Manhattan, k=5)': y_pred_knn_man,
    'Naïve Bayes Gaussiano': y_pred_nb
}

res_list = []
for name, preds in models_dict.items():
    acc = accuracy_score(y_test, preds)
    prec_macro = precision_score(y_test, preds, average='macro', zero_division=0)
    rec_macro = recall_score(y_test, preds, average='macro', zero_division=0)
    f1_macro = f1_score(y_test, preds, average='macro', zero_division=0)
    res_list.append({
        'Modelo': name,
        'Acurácia': acc,
        'Precisão Macro': prec_macro,
        'Recall Macro': rec_macro,
        'F1-Score Macro': f1_macro
    })

df_metrics = pd.DataFrame(res_list)
print("=== TABELA COMPARATIVA DE RESULTADOS ===")
print(df_metrics.to_string(index=False))

# 5. Geração de Figuras em Alta Resolução (300 DPI)

# FIGURA 9: Matrizes de Confusão Comparativas
fig, axes = plt.subplots(1, 3, figsize=(18, 5), dpi=300)
palette = 'Blues'

for ax, (name, preds) in zip(axes, [
    ('Árvore de Decisão', y_pred_dt),
    ('k-NN (k=5)', y_pred_knn),
    ('Naïve Bayes', y_pred_nb)
]):
    cm = confusion_matrix(y_test, preds, labels=labels)
    sns.heatmap(cm, annot=True, fmt='d', cmap=palette, cbar=False, ax=ax,
                xticklabels=labels, yticklabels=labels, annot_kws={'size': 14, 'weight': 'bold'})
    ax.set_title(f'{name}\nAcurácia: {accuracy_score(y_test, preds):.1%}', fontsize=12, pad=10, weight='bold')
    ax.set_xlabel('Classe Predita', fontsize=11)
    ax.set_ylabel('Classe Real', fontsize=11)

plt.tight_layout()
fig_path_9 = 'Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_9_Matrizes_Confusao_Comparativas.png'
fig.savefig(fig_path_9, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"Salvo: {fig_path_9}")

# FIGURA 10: Estrutura da Árvore de Decisão
fig, ax = plt.subplots(figsize=(18, 10), dpi=300)
plot_tree(
    dt,
    feature_names=feature_cols,
    class_names=labels,
    filled=True,
    rounded=True,
    fontsize=10,
    ax=ax,
    impurity=True
)
ax.set_title('Árvore de Decisão para Regimes de Inflação (Critério: Entropia de Shannon)\nEscola Politécnica de Pernambuco - Mineração de Dados', fontsize=14, weight='bold', pad=15)
plt.tight_layout()
fig_path_10 = 'Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_10_Arvore_Decisao_Regimes_Inflacao.png'
fig.savefig(fig_path_10, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"Salvo: {fig_path_10}")

# FIGURA 11: Importância dos Atributos (Ganho de Informação)
importances = pd.Series(dt.feature_importances_, index=feature_cols).sort_values(ascending=True)
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
importances_plot = importances[importances > 0]
bars = ax.barh(importances_plot.index, importances_plot.values, color='#1f77b4', edgecolor='#0d47a1', height=0.6)
ax.set_title('Importância dos Atributos Macroeconômicos na Árvore de Decisão\n(Redução Total da Entropia / Ganho de Informação)', fontsize=12, weight='bold', pad=12)
ax.set_xlabel('Ganho de Informação Normalizado', fontsize=11)
ax.set_xlim(0, max(importances_plot.values) * 1.15)
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.008, bar.get_y() + bar.get_height()/2, f'{w:.1%}', ha='left', va='center', fontsize=10, weight='bold')
ax.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
fig_path_11 = 'Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_11_Importancia_Atributos_Ganho_Informacao.png'
fig.savefig(fig_path_11, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"Salvo: {fig_path_11}")

# FIGURA 12: Série Temporal de Regimes Reais vs. Preditos (Teste 2023-2026)
df_comp = pd.DataFrame({
    'Date': dates_test,
    'Real': y_test.values,
    'Pred_DT': y_pred_dt,
    'IPCA_Real': df.loc[y_test.index, 'IPCA'].values
}).reset_index(drop=True)

color_map = {'Deflação': '#2ca02c', 'Controlado': '#1f77b4', 'Alta': '#d62728'}
y_map = {'Deflação': 0, 'Controlado': 1, 'Alta': 2}

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7), dpi=300, sharex=True, gridspec_kw={'height_ratios': [2, 1.2]})

# Painel Superior: Linha do IPCA Real com faixas
ax1.plot(df_comp['Date'], df_comp['IPCA_Real'], color='#333333', lw=1.8, marker='o', markersize=4, label='IPCA Mensal Real (% a.m.)')
ax1.axhline(0.0, color='#2ca02c', linestyle='--', alpha=0.7, label='Limiar Deflação (0.0%)')
ax1.axhline(0.50, color='#d62728', linestyle='--', alpha=0.7, label='Limiar Alta Inflação (0.50%)')
ax1.axhspan(-1.0, 0.0, color='#2ca02c', alpha=0.1)
ax1.axhspan(0.0, 0.50, color='#1f77b4', alpha=0.1)
ax1.axhspan(0.50, 2.5, color='#d62728', alpha=0.1)
ax1.set_ylabel('IPCA (% a.m.)', fontsize=11, weight='bold')
ax1.set_title('Acompanhamento Out-of-Sample: IPCA Real e Classificação de Regimes (2023 - 2026)', fontsize=13, weight='bold')
ax1.legend(loc='upper right', framealpha=0.9)
ax1.grid(True, linestyle=':', alpha=0.6)

# Painel Inferior: Regimes Reais vs Preditos pela Árvore
ax2.step(df_comp['Date'], df_comp['Real'].map(y_map), where='mid', label='Regime Real Observado', color='#000000', lw=2.2)
ax2.step(df_comp['Date'], df_comp['Pred_DT'].map(y_map), where='mid', label='Predição Árvore de Decisão', color='#e65100', linestyle='--', lw=2.0)
ax2.set_yticks([0, 1, 2])
ax2.set_yticklabels(['Deflação', 'Controlado', 'Alta Inflação'], fontsize=10, weight='bold')
ax2.set_ylabel('Regime', fontsize=11, weight='bold')
ax2.set_xlabel('Data (Mês-Ano)', fontsize=11)
ax2.legend(loc='lower right', framealpha=0.9)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
fig_path_12 = 'Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_12_Serie_Temporal_Regimes_Reais_vs_Preditos.png'
fig.savefig(fig_path_12, dpi=300, bbox_inches='tight')
plt.close(fig)
print(f"Salvo: {fig_path_12}")

print("=== Execução de modelagem e gráficos concluída com sucesso! ===")
