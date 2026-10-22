import os

codigo = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universidade de Pernambuco (UPE) - Escola Politécnica (POLI)
Programa de Pós-Graduação / Graduação em Engenharia da Computação
Disciplina: Mineração de Dados - Atividade 8: Métodos de Regressão Supervisionada
Professor: Dr. Alexandre Maciel (alexandre.maciel@upe.br)

Projeto: Mineração de Séries Temporais para Previsão da Inflação Brasileira (IPCA)
Script: Modelagem Preditiva Multivariada de Regressão com Horizontes de Mercado (h=1, 3, 12)
Autores: Equipe do Projeto de Mineração de Dados (2026)
"""

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

# Configuração estética dos gráficos
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8


def localizar_base_dados():
    """Localiza o arquivo df_macro.csv em diferentes diretórios de execução."""
    candidatos = [
        'Dados/df_macro.csv',
        '../../Dados/df_macro.csv',
        '../Dados/df_macro.csv',
        os.path.join(os.path.dirname(__file__), '../../Dados/df_macro.csv')
    ]
    for c in candidatos:
        if os.path.exists(c):
            return os.path.abspath(c)
    raise FileNotFoundError("Base de dados 'df_macro.csv' não encontrada nos caminhos padrão.")


def carregar_e_preparar_dados():
    """
    Carrega o painel macroeconômico mensal (174 meses, 2012–2026),
    aplica ordenação cronológica estrita, imputação sem vazamento de dados
    e engenharia de atributos econômicos estacionários.
    """
    caminho = localizar_base_dados()
    print(f"[*] Carregando base de dados: {caminho}")
    df = pd.read_csv(caminho)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)
    
    # Imputação temporal causal
    df = df.ffill().bfill()
    
    # Transformações Estacionárias para séries com tendência de nível
    df['d_USDBRL'] = df['USDBRL'].pct_change() * 100.0          # Variação cambial percentual mensal
    df['d_SELIC'] = df['SELIC'].diff()                          # Variação em pontos percentuais da taxa SELIC
    df['d_Desemprego'] = df['Desemprego'].diff()                # Variação da taxa de desemprego
    df['d_Energia'] = df['Consumo_Energia_Total'].pct_change() * 100.0  # Proxy de atividade econômica
    df = df.bfill()
    
    # Lista de preditores fundamentados no projeto e na literatura macroeconômica
    stat_features = [
        'IPCA', 'IPCA Alimentação_bebidas', 'IPCA_Transportes', 'INPC_Habitação',
        'IPCA_Saúde_cuidados_pessoais', 'IPCA_Educação', 'IPCA_Vestuário', 'IPCA_Despesas_Pessoais',
        'IGP_M', 'IGP_DI', 'IPC_BR', 'SELIC', 'Desemprego',
        'd_USDBRL', 'd_SELIC', 'd_Desemprego', 'd_Energia'
    ]
    
    print(f"[*] Base carregada: {len(df)} observações mensais ({df['Date'].min().strftime('%Y-%m')} a {df['Date'].max().strftime('%Y-%m')})")
    print(f"[*] Atributos econômicos selecionados: {len(stat_features)} dimensões.")
    return df, stat_features


def calcular_metricas(y_real, y_pred, y_treino_mean=None):
    """Calcula conjunto abrangente de métricas econométricas e de mercado."""
    mae = mean_absolute_error(y_real, y_pred)
    mse = mean_squared_error(y_real, y_pred)
    rmse = np.sqrt(mse)
    
    # MAPE com proteção contra divisão por zero
    denominador = np.where(np.abs(y_real) < 0.05, 0.05, np.abs(y_real))
    mape = np.mean(np.abs((y_real - y_pred) / denominador)) * 100.0
    
    # WAPE (Weighted Absolute Percentage Error - Padrão de Mercado)
    wape = (np.sum(np.abs(y_real - y_pred)) / np.sum(np.abs(y_real))) * 100.0
    
    # R² convencional
    r2 = r2_score(y_real, y_pred)
    
    # Hit Ratio Direcional (Acerto do sinal de aceleração/desaceleração da inflação)
    if len(y_real) > 1:
        sinal_real = np.sign(np.diff(y_real))
        sinal_pred = np.sign(y_pred[1:] - y_real[:-1])
        hit_ratio = np.mean(sinal_real == sinal_pred) * 100.0
    else:
        hit_ratio = np.nan
        
    return {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'MAPE': mape,
        'WAPE': wape,
        'R2': r2,
        'HitRatio': hit_ratio
    }


def executar_pipeline_regressao():
    """
    Executa a modelagem preditiva direta (Direct Multi-Step Forecasting)
    para os horizontes h=1, h=3 e h=12 meses à frente.
    """
    df, stat_features = carregar_e_preparar_dados()
    
    horizontes = {
        1: "Nowcasting / 1 Mês à Frente (Curto Prazo / DAP e NTN-B)",
        3: "Horizonte Trimestral / 3 Meses à Frente (Reuniões do COPOM)",
        12: "Horizonte Relevante / 12 Meses à Frente (Meta Anualizada do BACEN)"
    }
    
    resultados_gerais = []
    detalhes_previsoes = {}
    coeficientes_lasso_todos = {}
    
    for h, desc in horizontes.items():
        print("\n" + "=" * 90)
        print(f"🚀 EXECUTANDO MODELAGEM PREDITIVA PARA HORIZONTE h={h}: {desc}")
        print("=" * 90)
        
        df_h = df.copy()
        df_h['target'] = df_h['IPCA'].shift(-h)
        
        # Sazonalidade determinística do mês de destino (t+h)
        target_dates = df_h['Date'].shift(-h)
        df_h['sin_mes_alvo'] = np.sin(2 * np.pi * target_dates.dt.month / 12)
        df_h['cos_mes_alvo'] = np.cos(2 * np.pi * target_dates.dt.month / 12)
        
        colunas_preditoras = stat_features + ['sin_mes_alvo', 'cos_mes_alvo']
        df_valido = df_h.dropna(subset=['target'] + colunas_preditoras).copy()
        
        # Partição Cronológica Causal Out-of-Sample (sem embaralhamento)
        mask_treino = df_valido['Date'] < '2022-01-01'
        mask_teste = df_valido['Date'] >= '2022-01-01'
        
        X_treino = df_valido.loc[mask_treino, colunas_preditoras].copy()
        y_treino = df_valido.loc[mask_treino, 'target'].copy()
        
        X_teste = df_valido.loc[mask_teste, colunas_preditoras].copy()
        y_teste = df_valido.loc[mask_teste, 'target'].copy()
        datas_teste = target_dates.loc[mask_teste].copy()
        
        print(f"[*] Amostra de Treinamento (Indução): {len(X_treino)} meses (2012 a 2021)")
        print(f"[*] Amostra de Teste (Dedução Cega):  {len(X_teste)} meses (2022 a 2026)")
        
        # Padronização Z-Score calibrada estritamente no conjunto de treino
        scaler = StandardScaler()
        X_treino_sc = scaler.fit_transform(X_treino)
        X_teste_sc = scaler.transform(X_teste)
        
        # 1. Baseline 1: Persistência do Último Mês Realizado (y_t)
        y_pred_persistencia = df_valido.loc[mask_teste, 'IPCA'].values
        
        # 2. Baseline 2: Média Histórica do Conjunto de Treinamento
        y_pred_media = np.full(len(y_teste), y_treino.mean())
        
        # 3. Regressão Ridge (Regularização L2)
        ridge = Ridge(alpha=10.0, random_state=42)
        ridge.fit(X_treino_sc, y_treino)
        y_pred_ridge = ridge.predict(X_teste_sc)
        
        # 4. Regressão Elastic Net (Penalização L1 + L2 Convexa)
        enet = ElasticNet(alpha=0.02, l1_ratio=0.7, random_state=42, max_iter=5000)
        enet.fit(X_treino_sc, y_treino)
        y_pred_enet = enet.predict(X_teste_sc)
        
        # 5. Regressão Lasso (Regularização L1 com Seleção Esparsa de Features)
        alpha_opt = 0.015 if h == 1 else (0.02 if h == 3 else 0.025)
        lasso = Lasso(alpha=alpha_opt, random_state=42, max_iter=5000)
        lasso.fit(X_treino_sc, y_treino)
        y_pred_lasso = lasso.predict(X_teste_sc)
        
        # Guardar coeficientes para interpretação macroeconômica
        coef_df = pd.DataFrame({
            'Atributo': colunas_preditoras,
            'Coeficiente': lasso.coef_
        }).sort_values(by='Coeficiente', key=abs, ascending=False)
        coeficientes_lasso_todos[h] = coef_df
        
        # 6. Random Forest Regressor (Ensemble Não-Linear)
        rf = RandomForestRegressor(
            n_estimators=100,
            max_depth=4,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        rf.fit(X_treino, y_treino)
        y_pred_rf = rf.predict(X_teste)
        
        # 7. Modelo Híbrido Causal: Lasso + Random Forest nos Resíduos (Decomposição de Zhang)
        residuos_treino = y_treino - lasso.predict(X_treino_sc)
        rf_res = RandomForestRegressor(
            n_estimators=100,
            max_depth=3,
            min_samples_leaf=3,
            random_state=42,
            n_jobs=-1
        )
        rf_res.fit(X_treino, residuos_treino)
        y_pred_hibrido = y_pred_lasso + rf_res.predict(X_teste)
        
        # Consolidar Previsões do Horizonte
        modelos_h = {
            'Baseline Persistência (y_t)': y_pred_persistencia,
            'Baseline Média Histórica': y_pred_media,
            'Regressão Ridge (L2)': y_pred_ridge,
            'Regressão Elastic Net': y_pred_enet,
            'Regressão Lasso (L1 - Seleção Esparsa)': y_pred_lasso,
            'Random Forest Regressor (Ensemble)': y_pred_rf,
            'Modelo Híbrido (Lasso + RF Resíduos)': y_pred_hibrido
        }
        
        detalhes_previsoes[h] = {
            'datas': datas_teste,
            'y_real': y_teste.values,
            'preds': modelos_h
        }
        
        print(f"\\n{'Modelo':<40} | {'MAE':<7} | {'RMSE':<7} | {'R²':<7} | {'WAPE(%)':<8} | {'HitRatio':<8}")
        print("-" * 88)
        for nome, preds in modelos_h.items():
            m = calcular_metricas(y_teste.values, preds, y_treino.mean())
            resultados_gerais.append({
                'Horizonte': f"h={h} ({'1 mês' if h==1 else ('3 meses' if h==3 else '12 meses')})",
                'Modelo': nome,
                'MAE (p.p.)': round(m['MAE'], 4),
                'RMSE (p.p.)': round(m['RMSE'], 4),
                'MSE': round(m['MSE'], 4),
                'MAPE (%)': round(m['MAPE'], 2),
                'WAPE (%)': round(m['WAPE'], 2),
                'R²': round(m['R2'], 4),
                'Hit Ratio (%)': round(m['HitRatio'], 1)
            })
            print(f"{nome:<40} | {m['MAE']:<7.4f} | {m['RMSE']:<7.4f} | {m['R2']:<+7.4f} | {m['WAPE']:<8.2f} | {m['HitRatio']:<7.1f}%")
            
        print("\\n[*] Coeficientes Mais Relevantes Selecionados pelo Lasso (L1):")
        nonzero = coef_df[coef_df['Coeficiente'].abs() > 0.0001].head(8)
        for _, row in nonzero.iterrows():
            sinal = "📈 (+) Pressão Inflacionária" if row['Coeficiente'] > 0 else "📉 (-) Efeito Desinflacionário"
            print(f"    - {row['Atributo']:<30}: {row['Coeficiente']:+.5f}  [{sinal}]")
            
    df_res = pd.DataFrame(resultados_gerais)
    return df_res, detalhes_previsoes, coeficientes_lasso_todos


def gerar_graficos_alta_resolucao(detalhes_previsoes, coeficientes_lasso_todos, pasta_saida):
    """Gera e salva 4 figuras acadêmicas em alta resolução (300 DPI)."""
    os.makedirs(pasta_saida, exist_ok=True)
    pasta_oficial_4 = os.path.abspath("Entrega_Classroom/4_Graficos_Alta_Resolucao")
    os.makedirs(pasta_oficial_4, exist_ok=True)
    
    print("\\n" + "=" * 90)
    print("🎨 GERANDO FIGURAS DE ALTA RESOLUÇÃO (300 DPI) PARA O ARTIGO...")
    print("=" * 90)
    
    # -------------------------------------------------------------
    # FIGURA 14: Comparativo de Métricas nos 3 Horizontes de Mercado
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), sharey=True)
    modelos_plot = [
        'Baseline Persistência (y_t)',
        'Regressão Ridge (L2)',
        'Regressão Elastic Net',
        'Regressão Lasso (L1 - Seleção Esparsa)',
        'Random Forest Regressor (Ensemble)',
        'Modelo Híbrido (Lasso + RF Resíduos)'
    ]
    
    for idx, (h, ax) in enumerate(zip([1, 3, 12], axes)):
        y_real = detalhes_previsoes[h]['y_real']
        maes = [mean_absolute_error(y_real, detalhes_previsoes[h]['preds'][m]) for m in modelos_plot]
        rmses = [np.sqrt(mean_squared_error(y_real, detalhes_previsoes[h]['preds'][m])) for m in modelos_plot]
        
        x = np.arange(len(modelos_plot))
        width = 0.38
        
        rects1 = ax.bar(x - width/2, maes, width, label='MAE (p.p.)', color='#2b5c8f', alpha=0.9)
        rects2 = ax.bar(x + width/2, rmses, width, label='RMSE (p.p.)', color='#e76f51', alpha=0.9)
        
        rotulos_h = {1: "Curto Prazo (h=1 mês)", 3: "Trimestral (h=3 meses)", 12: "Política Monetária (h=12 meses)"}
        ax.set_title(f"Horizonte: {rotulos_h[h]}", fontsize=12, fontweight='bold', pad=10)
        ax.set_xticks(x)
        ax.set_xticklabels([
            'Persistência', 'Ridge', 'ElasticNet', 'Lasso (L1)', 'RandomForest', 'Híbrido'
        ], rotation=35, ha='right', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.5)
        if idx == 0:
            ax.set_ylabel("Erro de Previsão (Pontos Percentuais)", fontsize=11, fontweight='bold')
            ax.legend(frameon=True, facecolor='white', framealpha=0.9)
            
        for rect in rects1:
            h_val = rect.get_height()
            ax.annotate(f'{h_val:.2f}', xy=(rect.get_x() + rect.get_width()/2, h_val),
                        xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8)
                        
    plt.suptitle("Figura 14 – Comparativo de Desempenho (MAE e RMSE) nos Três Horizontes de Mercado (2022–2026)",
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    f14_path1 = os.path.join(pasta_saida, "Figura_14_Comparativo_Regressores_Horizontes.png")
    f14_path2 = os.path.join(pasta_oficial_4, "Figura_14_Comparativo_Regressores_Horizontes.png")
    fig.savefig(f14_path1, dpi=300, bbox_inches='tight')
    fig.savefig(f14_path2, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Salvo: {f14_path1}")
    
    # -------------------------------------------------------------
    # FIGURA 15: Séries Temporais Real vs Predito Out-of-Sample (h=1)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(15, 6))
    datas = detalhes_previsoes[1]['datas']
    y_real = detalhes_previsoes[1]['y_real']
    
    ax.plot(datas, y_real, label='IPCA Real (IBGE)', color='#111111', linewidth=2.5, marker='o', markersize=4)
    ax.plot(datas, detalhes_previsoes[1]['preds']['Regressão Lasso (L1 - Seleção Esparsa)'],
            label='Regressão Lasso (L1)', color='#2a9d8f', linewidth=2.0, linestyle='--')
    ax.plot(datas, detalhes_previsoes[1]['preds']['Random Forest Regressor (Ensemble)'],
            label='Random Forest', color='#e76f51', linewidth=1.8, linestyle=':')
    ax.plot(datas, detalhes_previsoes[1]['preds']['Modelo Híbrido (Lasso + RF Resíduos)'],
            label='Modelo Híbrido (Lasso + RF)', color='#9d0208', linewidth=2.2, linestyle='-')
            
    # Linha zero de deflação e sombreamento de regime
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.7)
    ax.axvspan(pd.to_datetime('2022-07-01'), pd.to_datetime('2022-09-01'),
               color='#f4a261', alpha=0.25, label='Choque Tributário ICMS (Deflação 2022)')
               
    ax.set_title("Figura 15 – Série Temporal de Previsão Out-of-Sample do IPCA Mensal (2022 a 2026, h=1 Mês)",
                 fontsize=14, fontweight='bold', pad=12)
    ax.set_ylabel("Variação Mensal do IPCA (%)", fontsize=12, fontweight='bold')
    ax.set_xlabel("Ano / Mês de Divulgação", fontsize=12, fontweight='bold')
    ax.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper right', fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    f15_path1 = os.path.join(pasta_saida, "Figura_15_Serie_Temporal_Real_vs_Predito_Regressao.png")
    f15_path2 = os.path.join(pasta_oficial_4, "Figura_15_Serie_Temporal_Real_vs_Predito_Regressao.png")
    fig.savefig(f15_path1, dpi=300, bbox_inches='tight')
    fig.savefig(f15_path2, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Salvo: {f15_path1}")
    
    # -------------------------------------------------------------
    # FIGURA 16: Coeficientes do Lasso (Sparsity e Transição Econômica)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharex=False)
    for idx, (h, ax) in enumerate(zip([1, 3, 12], axes)):
        c_df = coeficientes_lasso_todos[h]
        top_c = c_df[c_df['Coeficiente'].abs() > 0.0001].copy().head(9)
        top_c = top_c.sort_values(by='Coeficiente', ascending=True)
        
        cores_barras = ['#e76f51' if v < 0 else '#2a9d8f' for v in top_c['Coeficiente']]
        ax.barh(top_c['Atributo'], top_c['Coeficiente'], color=cores_barras, alpha=0.85, edgecolor='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.8, linestyle='--')
        
        rotulos_h = {1: "Curto Prazo (h=1) -> Inércia & Atacado",
                     3: "Trimestral (h=3) -> Transição Causal",
                     12: "Horizonte Relevante (h=12) -> Domínio da SELIC"}
        ax.set_title(rotulos_h[h], fontsize=11, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.tick_params(axis='y', labelsize=9)
        if idx == 0:
            ax.set_xlabel("Impacto Padronizado (Coeficiente L1)", fontsize=10, fontweight='bold')
            
    plt.suptitle("Figura 16 – Seleção Esparsa de Atributos via Lasso (L1): Transição da Inércia para a Política Monetária",
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    f16_path1 = os.path.join(pasta_saida, "Figura_16_Coeficientes_Lasso_Sparsity_Horizontes.png")
    f16_path2 = os.path.join(pasta_oficial_4, "Figura_16_Coeficientes_Lasso_Sparsity_Horizontes.png")
    fig.savefig(f16_path1, dpi=300, bbox_inches='tight')
    fig.savefig(f16_path2, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Salvo: {f16_path1}")
    
    # -------------------------------------------------------------
    # FIGURA 17: Diagnóstico de Dispersão e Resíduos (Real vs Predito)
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    y_r = detalhes_previsoes[1]['y_real']
    y_p = detalhes_previsoes[1]['preds']['Regressão Lasso (L1 - Seleção Esparsa)']
    residuos = y_r - y_p
    
    # Dispersão
    ax1.scatter(y_r, y_p, color='#2b5c8f', edgecolors='k', alpha=0.75, s=55)
    limites = [min(min(y_r), min(y_p)) - 0.1, max(max(y_r), max(y_p)) + 0.1]
    ax1.plot(limites, limites, color='#d00000', linestyle='--', linewidth=1.5, label='Previsão Perfeita (45°)')
    ax1.set_xlim(limites)
    ax1.set_ylim(limites)
    ax1.set_title("Dispersão: IPCA Real vs. Predito pelo Lasso (h=1)", fontsize=12, fontweight='bold')
    ax1.set_xlabel("IPCA Real Observado (%)", fontsize=11, fontweight='bold')
    ax1.set_ylabel("IPCA Predito pelo Modelo (%)", fontsize=11, fontweight='bold')
    ax1.legend(frameon=True, facecolor='white')
    ax1.grid(True, linestyle='--', alpha=0.5)
    
    # Histograma dos Resíduos
    sns.histplot(residuos, kde=True, ax=ax2, color='#2a9d8f', bins=12, edgecolor='black', linewidth=0.6)
    ax2.axvline(0, color='red', linestyle='--', linewidth=1.2, label=f'Média dos Resíduos ({np.mean(residuos):+.3f})')
    ax2.axvline(np.mean(residuos) + np.std(residuos), color='gray', linestyle=':', label=f'+1 Desvio Padrão ({np.std(residuos):.3f})')
    ax2.axvline(np.mean(residuos) - np.std(residuos), color='gray', linestyle=':')
    ax2.set_title("Distribuição dos Resíduos de Previsão Out-of-Sample", fontsize=12, fontweight='bold')
    ax2.set_xlabel("Erro Residual ($e_t = y_t - \\hat{y}_t$ em p.p.)", fontsize=11, fontweight='bold')
    ax2.set_ylabel("Frequência de Meses", fontsize=11, fontweight='bold')
    ax2.legend(frameon=True, facecolor='white')
    ax2.grid(True, linestyle='--', alpha=0.5)
    
    plt.suptitle("Figura 17 – Diagnóstico Econométrico de Resíduos e Aderência Linear da Regressão Lasso",
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    f17_path1 = os.path.join(pasta_saida, "Figura_17_Dispersao_Residuos_Diagnostico.png")
    f17_path2 = os.path.join(pasta_oficial_4, "Figura_17_Dispersao_Residuos_Diagnostico.png")
    fig.savefig(f17_path1, dpi=300, bbox_inches='tight')
    fig.savefig(f17_path2, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Salvo: {f17_path1}")


def main():
    print("=" * 90)
    print("🏛️ UNIVERSIDADE DE PERNAMBUCO (UPE) - ESCOLA POLITÉCNICA (POLI)")
    print("📚 DISCIPLINA: MINERAÇÃO DE DADOS - PROF. DR. ALEXANDRE MACIEL")
    print("📈 ATIVIDADE 8: MODELAGEM SUPERVISIONADA DE REGRESSÃO EM SÉRIES MACROECONÔMICAS")
    print("=" * 90)
    
    df_resultados, detalhes_previsoes, coeficientes_lasso_todos = executar_pipeline_regressao()
    
    pasta_saida_graficos = os.path.abspath("Entrega_Classroom/8_Regressao/graficos")
    gerar_graficos_alta_resolucao(detalhes_previsoes, coeficientes_lasso_todos, pasta_saida_graficos)
    
    # Salvar tabela de resultados em CSV
    caminho_csv = os.path.abspath("Entrega_Classroom/8_Regressao/metricas_regressao_horizontes.csv")
    df_resultados.to_csv(caminho_csv, index=False)
    print(f"\\n✅ Tabela de métricas salva com sucesso em: {caminho_csv}")
    
    print("\\n" + "=" * 90)
    print("🏆 SÍNTESE FINAL DE RESULTADOS CONSOLIDADOS (CONJUNTO DE TESTE 2022–2026)")
    print("=" * 90)
    print(df_resultados.to_string(index=False))
    print("=" * 90)
    print("Pipeline de Regressão concluído com êxito!")


if __name__ == '__main__':
    main()
'''

caminho_py = 'Entrega_Classroom/8_Regressao/regressao_previsao_inflacao.py'
os.makedirs(os.path.dirname(caminho_py), exist_ok=True)
with open(caminho_py, 'w', encoding='utf-8') as f:
    f.write(codigo)
print(f"✅ Arquivo salvo: {caminho_py}")
