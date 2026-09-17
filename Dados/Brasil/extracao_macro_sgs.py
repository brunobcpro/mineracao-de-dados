#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Extração Automatizada de Dados Macroeconômicos - SGS / Banco Central do Brasil
Projeto: Mineração de Dados e Previsão da Inflação (IPCA)
Período: 01/03/2012 a 31/08/2026 (Até Agosto/2026)
"""

import urllib.request
import json
import time
import os
import pandas as pd
import numpy as np

SERIES_BCB = {
    'IPCA': 4447,
    'IPCA_Transportes': 1639,
    'IPCA Alimentação_bebidas': 1635,
    'INPC_Habitação': 1636,
    'IPCA_Saúde_cuidados_pessoais': 1641,
    'IPCA_Vestuário': 1638,
    'IPCA_Educação': 1643,
    'IPCA_Despesas_Pessoais': 1642,
    'USDBRL': 3696,
    'Reservas Internacionais': 3546,
    'Desemprego': 24369,
    'SELIC': 4390,
    'SalMinimo': 1619,
    'PIB Mensal': 4380,
    'QteOvos': 1310,
    'INPC': 188,
    'IGP_M': 189,
    'IGP_DI': 190,
    'IPC_BR': 191,
    'Produção_Derivados_Petróleo': 1391,
    'Consumo_Gasolina': 1393,
    'Consumo_Óleo_Combustível': 1395,
    'Consumo_Energia_Comercial': 1402,
    'Consumo_Energia_Residencial': 1403,
    'Consumo_Energia_Total': 1406,
    'Estoque_Empregos_Formais_Total': 28763,
    'Estoque_Empregos_Formais_Agropecuária': 28764,
    'Estoque_Empregos_Formais_Construção': 28770
}

START_DATE = '01/03/2012'
END_DATE = '31/08/2026'

def fetch_sgs_series(code: int, name: str, start: str = START_DATE, end: str = END_DATE, max_retries: int = 3) -> pd.Series:
    """Busca uma série temporal da API oficial do SGS/BACEN com retentativas automáticas."""
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados?formato=json&dataInicial={start}&dataFinal={end}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode('utf-8'))
            
            df_temp = pd.DataFrame(data)
            if df_temp.empty:
                print(f"⚠️ Atenção: Série {name} ({code}) retornou vazia da API.")
                return pd.Series(dtype=float, name=name)
            
            df_temp['data'] = pd.to_datetime(df_temp['data'], format='%d/%m/%Y')
            df_temp['valor'] = pd.to_numeric(df_temp['valor'], errors='coerce')
            df_temp = df_temp.drop_duplicates(subset=['data']).sort_values('data')
            df_temp.set_index('data', inplace=True)
            
            # Se tiver frequência diária, agrega pela média mensal (MS)
            if len(df_temp) > 200:
                s = df_temp['valor'].resample('MS').mean()
            else:
                s = df_temp['valor'].resample('MS').first()
                
            s.name = name
            print(f"✓ [{name}] ({code}): {len(s)} observações extraídas ({s.index.min().strftime('%Y-%m')} a {s.index.max().strftime('%Y-%m')}).")
            return s
        except Exception as e:
            print(f"Tentativa {attempt}/{max_retries} falhou para {name} ({code}): {e}")
            time.sleep(1.5)
            
    raise RuntimeError(f"Falha definitiva ao obter a série {name} ({code}) após {max_retries} tentativas.")

def extract_all_macro_features() -> pd.DataFrame:
    """Extrai todas as 29 variáveis macroeconômicas e consolida em DataFrame indexado mensalmente."""
    print("=" * 70)
    print(f"Iniciando Extração de Dados Macroeconômicos do SGS/BACEN ({START_DATE} a {END_DATE})")
    print("=" * 70)
    
    date_range = pd.date_range(start='2012-03-01', end='2026-08-01', freq='MS')
    df_macro = pd.DataFrame(index=date_range)
    df_macro.index.name = 'Date'
    
    for name, code in SERIES_BCB.items():
        s = fetch_sgs_series(code, name)
        df_macro = df_macro.join(s, how='left')
        time.sleep(0.12)
        
    print("\nExtração finalizada com sucesso!")
    print(f"Dimensões do DataFrame bruto: {df_macro.shape}")
    print(f"Período temporal: {df_macro.index.min()} a {df_macro.index.max()}")
    nulls = df_macro.isnull().sum()
    if (nulls > 0).any():
        print("Nulos por coluna identificados:")
        print(nulls[nulls > 0])
    else:
        print("Nenhum valor nulo identificado.")
    
    return df_macro

if __name__ == '__main__':
    df = extract_all_macro_features()
    
    df_out = df.reset_index()
    df_out['Date'] = df_out['Date'].dt.strftime('%Y-%m-%d')
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    base_paths = [
        os.path.join(base_dir, 'Dados', 'df_macro.csv'),
        os.path.join(base_dir, 'Dados', 'Brasil', 'df_macro.csv')
    ]
    
    for p in base_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        df_out.to_csv(p, index=False)
        print(f"Arquivo consolidado gravado em: {p}")
