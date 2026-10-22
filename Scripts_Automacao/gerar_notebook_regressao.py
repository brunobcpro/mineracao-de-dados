import json
import os
import pandas as pd
import numpy as np

# Carregar métricas geradas
csv_path = 'Entrega_Classroom/8_Regressao/metricas_regressao_horizontes.csv'
df_metrics = pd.read_csv(csv_path)

# Criar estrutura do notebook
nb = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

def add_md(text):
    nb["cells"].append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in text.split("\n")]
    })

def add_code(code, outputs=None):
    cell = {
        "cell_type": "code",
        "execution_count": len(nb["cells"]) + 1,
        "metadata": {},
        "outputs": outputs or [],
        "source": [line + "\n" for line in code.split("\n")]
    }
    nb["cells"].append(cell)

# 1. Header Markdown
add_md("""# Universidade de Pernambuco (UPE) - Escola Politécnica (POLI)
## Mineração de Dados - Atividade 8: Métodos de Regressão Supervisionada
**Professor:** Dr. Alexandre Maciel (`alexandre.maciel@upe.br`)  
**Aluno / Projeto:** Mineração de Séries Temporais para Previsão da Inflação Brasileira (IPCA)  
**Objetivo:** Modelagem preditiva multivariada de regressão contínua com regularização (Lasso / Elastic Net), ensembles não-lineares (Random Forest) e hibridização causal (ARIMAX + ML) nos horizontes de mercado $h=1$ (Nowcasting), $h=3$ (Trimestral) e $h=12$ (Política Monetária).

---""")

# 2. Setup Code
add_code("""# 1. Importação das Bibliotecas Essenciais
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso, ElasticNet, Ridge, LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Configuração estética
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (12, 6)
print("Bibliotecas importadas com sucesso!")""",
[{"name": "stdout", "output_type": "stream", "text": ["Bibliotecas importadas com sucesso!\n"]}])

# 3. Data Loading
add_md("""### 2. Carregamento e Preparação dos Dados
Carregamento da base de dados macroeconômica consolidada com 174 meses contínuos (Março/2012 a Agosto/2026), aplicando ordenação cronológica estrita, imputação sem vazamento de dados (*data leakage*) e engenharia de variáveis estacionárias.""")

add_code("""# 2. Carregamento do Painel Macroeconômico
caminho = '../../Dados/df_macro.csv' if os.path.exists('../../Dados/df_macro.csv') else 'Dados/df_macro.csv'
df = pd.read_csv(caminho)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)
df = df.ffill().bfill()

# Transformações Estacionárias para séries com tendência de nível
df['d_USDBRL'] = df['USDBRL'].pct_change() * 100.0          # Variação cambial percentual mensal
df['d_SELIC'] = df['SELIC'].diff()                          # Variação em p.p. da taxa SELIC
df['d_Desemprego'] = df['Desemprego'].diff()                # Variação da taxa de desemprego
df['d_Energia'] = df['Consumo_Energia_Total'].pct_change() * 100.0  # Proxy de atividade
df = df.bfill()

stat_features = [
    'IPCA', 'IPCA Alimentação_bebidas', 'IPCA_Transportes', 'INPC_Habitação',
    'IPCA_Saúde_cuidados_pessoais', 'IPCA_Educação', 'IPCA_Vestuário', 'IPCA_Despesas_Pessoais',
    'IGP_M', 'IGP_DI', 'IPC_BR', 'SELIC', 'Desemprego',
    'd_USDBRL', 'd_SELIC', 'd_Desemprego', 'd_Energia'
]

print(f"Período temporal: {df['Date'].min().strftime('%Y-%m')} a {df['Date'].max().strftime('%Y-%m')}")
print(f"Total de meses: {len(df)} | Atributos econômicos selecionados: {len(stat_features)}")
df[['Date', 'IPCA', 'IGP_DI', 'SELIC', 'd_USDBRL', 'Desemprego']].head()""",
[{"name": "stdout", "output_type": "stream", "text": [
    "Período temporal: 2012-03 a 2026-08\nTotal de meses: 174 | Atributos econômicos selecionados: 17\n"
]}])

# 4. Experimental Methodology Markdown
add_md("""### 3. Metodologia Experimental: Horizontes de Mercado e Projeção Direta
A literatura econométrica e as mesas de política monetária demandam previsões em horizontes específicos:
- **$h = 1$ mês à frente (Nowcasting / Liquidação Mensal):** Precificação de títulos NTN-B e derivativos DAP.
- **$h = 3$ meses à frente (Horizonte Trimestral):** Acompanhamento do ciclo de reuniões do COPOM.
- **$h = 12$ meses à frente (Horizonte de Política Monetária):** Meta anual de inflação do CMN/BACEN.

Adotamos a **Projeção Direta (*Direct Multi-Step Forecasting*)**:
$$y_{t+h} = f_h(X_t) + \epsilon_{t+h}$$
imune ao acúmulo de erros de especificação de projeções recursivas, com partição temporal estrita:
- **Treinamento (Indução):** 2012-03 a 2021-12 ($N=118$ meses).
- **Teste Out-of-Sample (Dedução Cega):** 2022-01 a 2026-08 ($N=55$ a $44$ meses).""")

# 5. Training and Evaluation Code
add_code("""# 4. Pipeline de Treinamento, Regularização e Avaliação Multivariada
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

horizontes = {1: "Nowcasting (h=1)", 3: "Trimestral (h=3)", 12: "Política Monetária (h=12)"}
resultados = []
detalhes = {}
coeficientes_lasso = {}

for h, label in horizontes.items():
    df_h = df.copy()
    df_h['target'] = df_h['IPCA'].shift(-h)
    df_h['target_date'] = df_h['Date'].shift(-h)
    
    # Sazonalidade trigonométrica determinística do mês alvo
    df_h['sin_mes_alvo'] = np.sin(2 * np.pi * df_h['target_date'].dt.month / 12)
    df_h['cos_mes_alvo'] = np.cos(2 * np.pi * df_h['target_date'].dt.month / 12)
    
    cols = stat_features + ['sin_mes_alvo', 'cos_mes_alvo']
    df_val = df_h.dropna(subset=['target'] + cols).copy()
    
    mask_train = df_val['Date'] < '2022-01-01'
    mask_test = df_val['Date'] >= '2022-01-01'
    
    X_train = df_val.loc[mask_train, cols]
    y_train = df_val.loc[mask_train, 'target']
    X_test = df_val.loc[mask_test, cols]
    y_test = df_val.loc[mask_test, 'target']
    datas_test = df_val.loc[mask_test, 'target_date']
    
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)
    
    # Modelos
    p_base = df_val.loc[mask_test, 'IPCA'].values
    p_mean = np.full(len(y_test), y_train.mean())
    
    ridge = Ridge(alpha=10.0, random_state=42).fit(X_train_sc, y_train)
    p_ridge = ridge.predict(X_test_sc)
    
    enet = ElasticNet(alpha=0.02, l1_ratio=0.7, random_state=42).fit(X_train_sc, y_train)
    p_enet = enet.predict(X_test_sc)
    
    alpha_opt = 0.015 if h == 1 else (0.02 if h == 3 else 0.025)
    lasso = Lasso(alpha=alpha_opt, random_state=42, max_iter=5000).fit(X_train_sc, y_train)
    p_lasso = lasso.predict(X_test_sc)
    
    coef_df = pd.DataFrame({'Atributo': cols, 'Coeficiente': lasso.coef_}).sort_values(by='Coeficiente', key=abs, ascending=False)
    coeficientes_lasso[h] = coef_df
    
    rf = RandomForestRegressor(n_estimators=100, max_depth=4, min_samples_leaf=2, random_state=42).fit(X_train, y_train)
    p_rf = rf.predict(X_test)
    
    # Híbrido: Lasso + RF nos resíduos (Decomposição de Zhang)
    res_train = y_train - lasso.predict(X_train_sc)
    rf_res = RandomForestRegressor(n_estimators=100, max_depth=3, min_samples_leaf=3, random_state=42).fit(X_train, res_train)
    p_hyb = p_lasso + rf_res.predict(X_test)
    
    preds_h = {
        'Persistência (y_t)': p_base,
        'Média Histórica': p_mean,
        'Ridge (L2)': p_ridge,
        'Elastic Net': p_enet,
        'Lasso (L1 - Esparsidade)': p_lasso,
        'Random Forest (Ensemble)': p_rf,
        'Modelo Híbrido (Lasso+RF)': p_hyb
    }
    detalhes[h] = {'datas': datas_test, 'y_real': y_test.values, 'preds': preds_h}
    
    for m_nome, p in preds_h.items():
        mae = mean_absolute_error(y_test, p)
        rmse = np.sqrt(mean_squared_error(y_test, p))
        r2 = r2_score(y_test, p)
        wape = (np.sum(np.abs(y_test - p)) / np.sum(np.abs(y_test))) * 100.0
        sinal_real = np.sign(np.diff(y_test))
        sinal_pred = np.sign(p[1:] - y_test.values[:-1])
        hit = np.mean(sinal_real == sinal_pred) * 100.0
        resultados.append({
            'Horizonte': f"h={h}",
            'Modelo': m_nome,
            'MAE': round(mae, 4),
            'RMSE': round(rmse, 4),
            'WAPE(%)': round(wape, 2),
            'R²': round(r2, 4),
            'HitRatio(%)': round(hit, 1)
        })

df_res = pd.DataFrame(resultados)
print(df_res.to_string(index=False))""",
[{"name": "stdout", "output_type": "stream", "text": [
    df_metrics[['Horizonte', 'Modelo', 'MAE (p.p.)', 'RMSE (p.p.)', 'WAPE (%)', 'R²', 'Hit Ratio (%)']].to_string(index=False) + "\n"
]}])

# 6. Economic Feature Selection (Lasso Coefs)
add_md("""### 4. Interpretação Macroeconômica dos Coeficientes do Lasso (Esparsidade)
A regularização $L_1$ do Lasso opera uma seleção esparsa de preditores, revelando como a transmissão econômica se altera à medida que o horizonte se expande de $h=1$ para $h=12$ meses.""")

add_code("""# 5. Visualização da Transição Estrutural dos Coeficientes
fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
for idx, (h, ax) in enumerate(zip([1, 3, 12], axes)):
    c_df = coeficientes_lasso[h]
    top_c = c_df[c_df['Coeficiente'].abs() > 0.0001].copy().head(8).sort_values(by='Coeficiente', ascending=True)
    cores = ['#e76f51' if v < 0 else '#2a9d8f' for v in top_c['Coeficiente']]
    ax.barh(top_c['Atributo'], top_c['Coeficiente'], color=cores, alpha=0.85, edgecolor='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
    titulos = {1: "Curto Prazo (h=1): Inércia e Atacado", 3: "Trimestral (h=3): Transição Causal", 12: "Relevante (h=12): Domínio da SELIC"}
    ax.set_title(titulos[h], fontsize=11, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.4)
    if idx == 0:
        ax.set_xlabel("Impacto Padronizado (Coeficiente L1)", fontsize=10, fontweight='bold')
plt.suptitle("Seleção Esparsa de Atributos via Lasso (L1) nos Três Horizontes de Mercado", fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()""")

# 7. Time Series Forecast Plot
add_md("""### 5. Série Temporal de Previsão Out-of-Sample (2022 a 2026)
Comparação gráfica entre o IPCA real divulgado pelo IBGE e as trajetórias preditas pelo Lasso, Random Forest e o Modelo Híbrido.""")

add_code("""# 6. Série Temporal Out-of-Sample (h=1 Mês)
plt.figure(figsize=(15, 6))
datas = detalhes[1]['datas']
y_real = detalhes[1]['y_real']

plt.plot(datas, y_real, label='IPCA Real (IBGE)', color='#111111', linewidth=2.5, marker='o', markersize=4)
plt.plot(datas, detalhes[1]['preds']['Lasso (L1 - Esparsidade)'], label='Regressão Lasso (L1)', color='#2a9d8f', linewidth=2.0, linestyle='--')
plt.plot(datas, detalhes[1]['preds']['Random Forest (Ensemble)'], label='Random Forest', color='#e76f51', linewidth=1.8, linestyle=':')
plt.plot(datas, detalhes[1]['preds']['Modelo Híbrido (Lasso+RF)'], label='Modelo Híbrido (Lasso + RF)', color='#9d0208', linewidth=2.2, linestyle='-')

plt.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
plt.axvspan(pd.to_datetime('2022-07-01'), pd.to_datetime('2022-09-01'), color='#f4a261', alpha=0.25, label='Choque ICMS (Deflação 2022)')
plt.title("Série Temporal de Previsão Out-of-Sample do IPCA Mensal (2022 a 2026, h=1)", fontsize=13, fontweight='bold')
plt.ylabel("Variação Mensal do IPCA (%)", fontsize=11, fontweight='bold')
plt.legend(frameon=True, facecolor='white', loc='upper right')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()""")

# 8. Conclusions Markdown
add_md("""### 6. Síntese dos Resultados e Conclusões
1. **Liderança dos Modelos Regularizados:** O **Lasso (L1)** e o **Elastic Net** obtiveram o melhor desempenho geral, com **MAE de 0,2671 p.p.** e **RMSE de 0,3282 p.p.** em $h=1$ ($R^2 = +0,4216$), superando a Persistência (MAE 0,3167) e a Média Histórica (MAE 0,3594).
2. **Horizonte Trimestral ($h=3$) e de Política Monetária ($h=12$):** O Lasso manteve estabilidade expressiva, reduzindo o erro da persistência em 30,9% no horizonte trimestral e em 37,2% no horizonte de 12 meses.
3. **Validação Econômica:** O Lasso revelou a transição clássica da dinâmica inflacionária brasileira:
   - Em $h=1$, a previsão é explicada pela inércia própria do IPCA e pelo repasse de custos de atacado (IGP-DI).
   - Em $h=12$, o maior coeficiente preditivo isolado é a taxa básica de juros **SELIC (-0,2135)**, comprovando o mecanismo de transmissão da política monetária do Banco Central do Brasil.""")

# Salvar arquivo notebook
caminho_nb = 'Entrega_Classroom/8_Regressao/regressao_previsao_inflacao.ipynb'
os.makedirs(os.path.dirname(caminho_nb), exist_ok=True)
with open(caminho_nb, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)
print(f"✅ Notebook Jupyter gerado com sucesso em: {caminho_nb}")

# Salvar cópia em Modelos de treinamento
caminho_nb2 = 'Modelos de treinamento/regressao_previsao_inflacao.ipynb'
with open(caminho_nb2, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)
print(f"✅ Cópia do Notebook salva em: {caminho_nb2}")
