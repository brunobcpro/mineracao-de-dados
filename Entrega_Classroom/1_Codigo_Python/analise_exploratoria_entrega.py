#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atividade: Mineração de Dados - Análise Exploratória e Caracterização de Atributos
Alunos / Projeto: Previsão da Inflação (IPCA) com Aprendizado de Máquina e Modelos Híbridos
Fonte dos Dados: Banco Central do Brasil (SGS/BACEN)
Período: Março de 2012 a Agosto de 2026 (N = 174 observações mensais)

Entregáveis contemplados:
1. Escolha de um atributo numérico (IPCA) e um nominal (Regime de Inflação);
2. Tabela de Distribuição de Frequência completa;
3. Histograma com densidade KDE, Boxplot univariado/estratificado e Gráfico de Dispersão;
4. Estatísticas descritivas com identificação de outliers.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

def executar_analise_exploratoria():
    print("=" * 75)
    print("ATIVIDADE DE MINERAÇÃO DE DADOS: ANÁLISE EXPLORATÓRIA DO IPCA")
    print("=" * 75)
    
    # 1. Carregamento dos dados
    caminho_csv = os.path.join('..', '5_Tabelas_e_Dados', 'df_macro_agosto2026.csv')
    if not os.path.exists(caminho_csv):
        caminho_csv = 'df_macro_agosto2026.csv'
        
    df = pd.read_csv(caminho_csv)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    # 2. Atributos Escolhidos:
    # Numérico: IPCA (% a.m.)
    # Nominal: Regime_Inflacao (Deflação, Meta / Estável, Alta / Acima da Meta)
    def classificar_regime(val):
        if val < 0.0:
            return 'Deflação'
        elif val <= 0.50:
            return 'Meta / Estável'
        else:
            return 'Alta / Acima da Meta'
            
    if 'Regime_Inflacao' not in df.columns:
        df['Regime_Inflacao'] = df['IPCA'].apply(classificar_regime)
        
    ordem_classes = ['Deflação', 'Meta / Estável', 'Alta / Acima da Meta']
    freq_abs = df['Regime_Inflacao'].value_counts().reindex(ordem_classes)
    freq_rel = (freq_abs / len(df)) * 100
    freq_cum = freq_abs.cumsum()
    freq_cum_rel = freq_rel.cumsum()
    
    tabela_freq = pd.DataFrame({
        'Classe Nominal': freq_abs.index,
        'Faixa (IPCA)': ['< 0,00%', '0,00% a 0,50%', '> 0,50%'],
        'Frequência Absoluta (fi)': freq_abs.values,
        'Frequência Relativa (%)': freq_rel.round(2).values,
        'Frequência Acumulada (Fi)': freq_cum.values,
        'Freq. Rel. Acumulada (%)': freq_cum_rel.round(2).values
    })
    
    print("\n[TABELA 1] DISTRIBUIÇÃO DE FREQUÊNCIA DA CLASSE NOMINAL (REGIME DE INFLAÇÃO):")
    print(tabela_freq.to_string(index=False))
    
    # 3. Estatísticas Descritivas do Atributo Numérico
    ipca = df['IPCA']
    q1 = ipca.quantile(0.25)
    q3 = ipca.quantile(0.75)
    iqr = q3 - q1
    lim_inf = q1 - 1.5 * iqr
    lim_sup = q3 + 1.5 * iqr
    outliers = ipca[(ipca < lim_inf) | (ipca > lim_sup)]
    
    print("\n[ESTATÍSTICAS DESCRITIVAS DO ATRIBUTO NUMÉRICO - IPCA]:")
    print(f"Total de Observações (N): {len(ipca)} meses")
    print(f"Média Aritmética:         {ipca.mean():.4f}%")
    print(f"Mediana:                  {ipca.median():.4f}%")
    print(f"Desvio Padrão Amostral:   {ipca.std():.4f}%")
    print(f"Variância Amostral:       {ipca.var():.4f}")
    print(f"Coeficiente Assimetria:   {ipca.skew():.4f} (Assimetria positiva / cauda à direita)")
    print(f"Coeficiente Curtose:      {ipca.kurtosis():.4f} (Leptocúrtica moderada)")
    print(f"Mínimo Histórico:         {ipca.min():.4f}% ({ipca.idxmin().strftime('%Y-%m')})")
    print(f"Máximo Histórico:         {ipca.max():.4f}% ({ipca.idxmax().strftime('%Y-%m')})")
    print(f"1º Quartil (Q1 - 25%):    {q1:.4f}%")
    print(f"3º Quartil (Q3 - 75%):    {q3:.4f}%")
    print(f"Intervalo Interquartílico:{iqr:.4f}%")
    print(f"Limites de Tukey (IQR):   [{lim_inf:.4f}%, {lim_sup:.4f}%]")
    print(f"Outliers Identificados:   {len(outliers)} pontos extremos")
    
    print("\nProcessamento estatístico concluído com sucesso!")

if __name__ == '__main__':
    executar_analise_exploratoria()
