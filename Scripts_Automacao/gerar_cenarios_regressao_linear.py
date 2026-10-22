#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Geração dos 3 Cenários de Seleção de Features e Regressão Linear:
- Cenário 1: Todas as variáveis (Full Kitchen Sink - 29 variáveis)
- Cenário 2: Estado da Arte com Filtro de Baixa Colinearidade (9 variáveis)
- Cenário 3: Modelo Otimizador Bioinspirado (Algoritmo Genético / PSO - 7 variáveis)
"""

import os
import json
import base64
import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Configuração estética limpa e profissional
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return data

# 1. Carregamento dos dados
caminho = 'Dados/df_macro.csv'
df = pd.read_csv(caminho)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True).ffill().bfill()

# Transformações Estacionárias
df['d_USDBRL'] = df['USDBRL'].pct_change() * 100.0
df['d_SELIC'] = df['SELIC'].diff()
df['d_Desemprego'] = df['Desemprego'].diff()
df['d_Energia'] = df['Consumo_Energia_Total'].pct_change() * 100.0
df['d_SalMinimo'] = df['SalMinimo'].pct_change() * 100.0
df['d_PIB'] = df['PIB Mensal'].pct_change() * 100.0
df = df.bfill()

# Alvo h=1
df['target'] = df['IPCA'].shift(-1)
df['target_date'] = df['Date'].shift(-1)
df['sin_m'] = np.sin(2 * np.pi * df['target_date'].dt.month / 12)
df['cos_m'] = np.cos(2 * np.pi * df['target_date'].dt.month / 12)

# DEFINIÇÃO FORMAL DOS 3 CENÁRIOS
# Cenário 1: Todas as 29 variáveis candidatas
cenario_1_cols = [
    'IPCA', 'IPCA Alimentação_bebidas', 'IPCA_Transportes', 'INPC_Habitação',
    'IPCA_Saúde_cuidados_pessoais', 'IPCA_Educação', 'IPCA_Vestuário', 'IPCA_Despesas_Pessoais',
    'IGP_M', 'IGP_DI', 'IPC_BR', 'INPC', 'USDBRL', 'Reservas Internacionais', 'SELIC',
    'Desemprego', 'SalMinimo', 'PIB Mensal', 'Produção_Derivados_Petróleo',
    'Consumo_Gasolina', 'Consumo_Energia_Total', 'd_USDBRL', 'd_SELIC', 'd_Desemprego',
    'd_Energia', 'd_SalMinimo', 'd_PIB', 'sin_m', 'cos_m'
]

# Cenário 2: Estado da Arte Macroeconômico (Filtrado por Baixa Colinearidade / VIF / Correlação < 0.70)
cenario_2_cols = [
    'IPCA', 'IGP_DI', 'IPCA Alimentação_bebidas', 'IPCA_Transportes',
    'd_USDBRL', 'd_SELIC', 'Desemprego', 'sin_m', 'cos_m'
]

# Cenário 3: Modelo Otimizador (Algoritmo Genético GA / PSO do Projeto)
cenario_3_cols = [
    'IPCA', 'IPCA_Transportes', 'IPCA Alimentação_bebidas', 'IPCA_Vestuário',
    'IPCA_Despesas_Pessoais', 'IPC_BR', 'USDBRL'
]

cenarios_dict = {
    'Cenário 1: Todas as Variáveis (29 vars)': cenario_1_cols,
    'Cenário 2: Estado da Arte (Filtro Colinearidade - 9 vars)': cenario_2_cols,
    'Cenário 3: Modelo Otimizador (GA/PSO - 7 vars)': cenario_3_cols
}

# Execução e extração de métricas
res_cenarios = []
modelos_por_cenario = {}

for nome, feats in cenarios_dict.items():
    df_val = df.dropna(subset=['target'] + feats).copy()
    mask_tr = df_val['Date'] < '2022-01-01'
    mask_te = df_val['Date'] >= '2022-01-01'
    
    X_tr, y_tr = df_val.loc[mask_tr, feats], df_val.loc[mask_tr, 'target']
    X_te, y_te = df_val.loc[mask_te, feats], df_val.loc[mask_te, 'target']
    datas_te = df_val.loc[mask_te, 'target_date']
    
    scaler = StandardScaler()
    X_tr_sc = scaler.fit_transform(X_tr)
    X_te_sc = scaler.transform(X_te)
    
    # 1. Regressão Linear OLS
    ols = LinearRegression().fit(X_tr_sc, y_tr)
    p_ols = ols.predict(X_te_sc)
    
    # 2. Regressão Lasso (L1)
    lasso = Lasso(alpha=0.015, random_state=42).fit(X_tr_sc, y_tr)
    p_lasso = lasso.predict(X_te_sc)
    
    # Métricas OLS
    mae_ols = mean_absolute_error(y_te, p_ols)
    rmse_ols = np.sqrt(mean_squared_error(y_te, p_ols))
    r2_ols = r2_score(y_te, p_ols)
    
    # Métricas Lasso
    mae_lasso = mean_absolute_error(y_te, p_lasso)
    rmse_lasso = np.sqrt(mean_squared_error(y_te, p_lasso))
    r2_lasso = r2_score(y_te, p_lasso)
    
    res_cenarios.append({
        'Cenário': nome,
        'N_Features': len(feats),
        'OLS MAE': round(mae_ols, 4),
        'OLS RMSE': round(rmse_ols, 4),
        'OLS R²': round(r2_ols, 4),
        'Lasso MAE': round(mae_lasso, 4),
        'Lasso RMSE': round(rmse_lasso, 4),
        'Lasso R²': round(r2_lasso, 4)
    })
    
    modelos_por_cenario[nome] = {
        'feats': feats,
        'ols': ols,
        'lasso': lasso,
        'p_ols': p_ols,
        'p_lasso': p_lasso,
        'y_te': y_te.values,
        'datas': datas_te
    }

df_cenarios = pd.DataFrame(res_cenarios)
print(df_cenarios.to_string(index=False))

# -------------------------------------------------------------
# FIGURA 20: COMPARATIVO DOS 3 CENÁRIOS NA REGRESSÃO LINEAR (OLS) E LASSO
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5))

x = np.arange(len(cenarios_dict))
width = 0.35

labels_cenarios = ['Cenário 1\n(Todas - 29 vars)', 'Cenário 2\n(Estado da Arte - 9 vars)', 'Cenário 3\n(Otimizador GA - 7 vars)']

# MAE
rects1 = ax1.bar(x - width/2, df_cenarios['OLS MAE'], width, label='Regressão Linear (OLS)', color='#e76f51', alpha=0.9, edgecolor='black', linewidth=0.5)
rects2 = ax1.bar(x + width/2, df_cenarios['Lasso MAE'], width, label='Regressão Lasso (L1)', color='#2a9d8f', alpha=0.9, edgecolor='black', linewidth=0.5)
ax1.set_title("Erro Médio Absoluto (MAE em p.p.) nos 3 Cenários", fontsize=11.5, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(labels_cenarios, fontsize=10)
ax1.set_ylabel("MAE (Pontos Percentuais)", fontsize=10.5, fontweight='bold')
ax1.legend(frameon=True, facecolor='white', loc='upper right')
ax1.grid(True, linestyle='--', alpha=0.5)

for rect in rects1:
    h = rect.get_height()
    ax1.annotate(f'{h:.3f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')
for rect in rects2:
    h = rect.get_height()
    ax1.annotate(f'{h:.3f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')

# R² Out-of-Sample
rects3 = ax2.bar(x - width/2, df_cenarios['OLS R²'], width, label='Regressão Linear (OLS)', color='#e76f51', alpha=0.9, edgecolor='black', linewidth=0.5)
rects4 = ax2.bar(x + width/2, df_cenarios['Lasso R²'], width, label='Regressão Lasso (L1)', color='#2a9d8f', alpha=0.9, edgecolor='black', linewidth=0.5)
ax2.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax2.set_title("Coeficiente de Determinação (R² Out-of-Sample)", fontsize=11.5, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(labels_cenarios, fontsize=10)
ax2.set_ylabel("R² Out-of-Sample", fontsize=10.5, fontweight='bold')
ax2.legend(frameon=True, facecolor='white', loc='lower left')
ax2.grid(True, linestyle='--', alpha=0.5)

for rect in rects3:
    h = rect.get_height()
    va = 'bottom' if h >= 0 else 'top'
    ax2.annotate(f'{h:+.2f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3 if h>=0 else -10), textcoords="offset points", ha='center', va=va, fontsize=9, fontweight='bold')
for rect in rects4:
    h = rect.get_height()
    ax2.annotate(f'{h:+.2f}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.suptitle("Figura 20 – Comparativo dos 3 Cenários de Seleção de Atributos: OLS vs. Lasso (2022–2026)", fontsize=13.5, fontweight='bold', y=1.02)
plt.tight_layout()

b64_fig_cenarios = fig_to_base64(fig)
fig.savefig('Entrega_Classroom/8_Regressao/graficos/Figura_20_Comparativo_3_Cenarios_OLS_Lasso.png', dpi=300, bbox_inches='tight')
fig.savefig('Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_20_Comparativo_3_Cenarios_OLS_Lasso.png', dpi=300, bbox_inches='tight')
plt.close(fig)

# -------------------------------------------------------------
# FIGURA 21: MATRIZ DE CORRELAÇÃO DO CENÁRIO 2 (BAIXA COLINEARIDADE)
# -------------------------------------------------------------
corr_s2 = df[cenario_2_cols].corr()
fig, ax = plt.subplots(figsize=(9.5, 7.5))
mask = np.triu(np.ones_like(corr_s2, dtype=bool))
sns.heatmap(corr_s2, mask=mask, annot=True, fmt=".2f", cmap='coolwarm', vmin=-0.6, vmax=0.8,
            square=True, linewidths=0.5, cbar_kws={"shrink": .8}, ax=ax)
ax.set_title("Figura 21 – Matriz de Correlação do Cenário 2 (Estado da Arte sem Colinearidade)", fontsize=12, fontweight='bold', pad=12)
plt.tight_layout()

b64_fig_corr = fig_to_base64(fig)
fig.savefig('Entrega_Classroom/8_Regressao/graficos/Figura_21_Matriz_Correlacao_Estado_da_Arte.png', dpi=300, bbox_inches='tight')
fig.savefig('Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_21_Matriz_Correlacao_Estado_da_Arte.png', dpi=300, bbox_inches='tight')
plt.close(fig)

# -------------------------------------------------------------
# FIGURA 22: COEFICIENTES OLS E IMPACTO NA PREVISÃO NO ESTADO DA ARTE
# -------------------------------------------------------------
ols_s2 = modelos_por_cenario['Cenário 2: Estado da Arte (Filtro Colinearidade - 9 vars)']['ols']
coef_ols_df = pd.DataFrame({
    'Atributo': cenario_2_cols,
    'Coeficiente': ols_s2.coef_
}).sort_values(by='Coeficiente', ascending=True)

fig, ax = plt.subplots(figsize=(10, 5.5))
cores_barras = ['#e76f51' if v < 0 else '#2a9d8f' for v in coef_ols_df['Coeficiente']]
ax.barh(coef_ols_df['Atributo'], coef_ols_df['Coeficiente'], color=cores_barras, alpha=0.85, edgecolor='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_title("Figura 22 – Coeficientes Padronizados da Regressão Linear (OLS) no Estado da Arte", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Impacto Padronizado sobre o IPCA t+1 (Coeficiente OLS)", fontsize=10.5, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.5)

for i, v in enumerate(coef_ols_df['Coeficiente']):
    sinal = "+" if v >= 0 else ""
    ax.text(v + (0.005 if v >= 0 else -0.025), i, f"{sinal}{v:.4f}", va='center', fontsize=9.5, fontweight='bold')

plt.tight_layout()
b64_fig_ols_coefs = fig_to_base64(fig)
fig.savefig('Entrega_Classroom/8_Regressao/graficos/Figura_22_Coeficientes_OLS_Estado_da_Arte.png', dpi=300, bbox_inches='tight')
fig.savefig('Entrega_Classroom/4_Graficos_Alta_Resolucao/Figura_22_Coeficientes_OLS_Estado_da_Arte.png', dpi=300, bbox_inches='tight')
plt.close(fig)

# Salvar resumo CSV dos cenários
df_cenarios.to_csv('Entrega_Classroom/8_Regressao/comparativo_3_cenarios_ols_lasso.csv', index=False)
print("✅ Gráficos e tabela dos 3 cenários gerados com sucesso!")
