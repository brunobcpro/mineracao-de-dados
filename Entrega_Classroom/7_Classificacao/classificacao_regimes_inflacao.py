#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universidade de Pernambuco (UPE) - Escola Politécnica (POLI)
Mineração de Dados - Atividade 7: Classificação Supervisionada de Regimes de Inflação
Professor: Dr. Alexandre Maciel
"""

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

def main():
    print("=" * 80)
    print("UPE / POLI - MINERAÇÃO DE DADOS: CLASSIFICAÇÃO DE REGIMES DE INFLAÇÃO (IPCA)")
    print("=" * 80)

    # 1. Carregamento dos dados
    caminho = '../../Dados/df_macro.csv' if os.path.exists('../../Dados/df_macro.csv') else 'Dados/df_macro.csv'
    df = pd.read_csv(caminho)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True).ffill().bfill()

    # 2. Definição dos Regimes Nominais
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

    # Previsão estritamente causal (t-1 -> t)
    X = df[feature_cols].shift(1).iloc[1:].copy()
    y = df['Regime'].iloc[1:].copy()
    dates = df['Date'].iloc[1:].copy()

    # 4. Split Out-of-Sample
    mask_train = dates < '2022-01-01'
    mask_test = dates >= '2022-01-01'

    X_train, y_train = X[mask_train].copy(), y[mask_train].copy()
    X_test, y_test = X[mask_test].copy(), y[mask_test].copy()

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)

    # 5. Modelos
    # 5.1 Baseline
    y_pred_base = [y_train.mode()[0]] * len(y_test)

    # 5.2 Árvore de Decisão (Entropia)
    dt = DecisionTreeClassifier(
        criterion='entropy',
        max_depth=3,
        class_weight='balanced',
        min_samples_leaf=2,
        random_state=42
    )
    dt.fit(X_train, y_train)
    y_pred_dt = dt.predict(X_test)

    # 5.3 k-NN (k=5)
    knn_euc = KNeighborsClassifier(n_neighbors=5, metric='euclidean', weights='distance')
    knn_euc.fit(X_train_sc, y_train)
    y_pred_knn_euc = knn_euc.predict(X_test_sc)

    # 5.4 Naïve Bayes
    nb = GaussianNB()
    nb.fit(X_train_sc, y_train)
    y_pred_nb = nb.predict(X_test_sc)

    # 6. Avaliação
    modelos = {
        'Baseline Majoritário': y_pred_base,
        'Árvore de Decisão (Entropia)': y_pred_dt,
        'k-NN (Euclidiana, k=5)': y_pred_knn_euc,
        'Naïve Bayes Gaussiano': y_pred_nb
    }

    print("\n--- RESULTADOS NO CONJUNTO DE TESTE (2022 a 2026) ---")
    res = []
    for nome, preds in modelos.items():
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, average='macro', zero_division=0)
        rec = recall_score(y_test, preds, average='macro', zero_division=0)
        f1 = f1_score(y_test, preds, average='macro', zero_division=0)
        res.append({
            'Modelo': nome,
            'Acurácia (%)': round(acc * 100, 2),
            'Precisão Macro (%)': round(prec * 100, 2),
            'Recall Macro (%)': round(rec * 100, 2),
            'F1-Score Macro': round(f1, 4)
        })
    print(pd.DataFrame(res).to_string(index=False))

    print("\n--- REGRAS EXTRAÍDAS DA ÁRVORE DE DECISÃO ---")
    print(export_text(dt, feature_names=feature_cols))

if __name__ == '__main__':
    main()
