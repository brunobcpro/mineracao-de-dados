#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Universidade de Pernambuco (UPE) - Escola Politécnica (POLI)
Programa de Graduação e Pós-Graduação em Engenharia da Computação
Disciplina: Mineração de Dados - Atividade 9: Mineração de Regras de Associação
Professor: Dr. Alexandre Maciel (alexandre.maciel@upe.br)

Projeto: Mineração de Séries Temporais para Previsão da Inflação Brasileira (IPCA)
Script: Pipeline Estado da Arte (SOTA) - Foco em Variáveis Macroeconômicas Exógenas
        (Eliminação completa de correlações triviais/contábeis entre subíndices do IPCA)
Autores: Equipe de Pesquisa em Mineração de Dados (2026)
"""

import os
import sys
import math
from itertools import combinations
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

# Configuração estética dos gráficos para publicação acadêmica (300 DPI)
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#cccccc"
plt.rcParams["axes.linewidth"] = 0.8
plt.rcParams["figure.autolayout"] = True


def localizar_base_dados():
    """Localiza o arquivo df_macro.csv a partir do diretório de execução."""
    candidatos = [
        "Dados/df_macro.csv",
        "../../Dados/df_macro.csv",
        "../Dados/df_macro.csv",
        os.path.join(os.path.dirname(__file__), "../../Dados/df_macro.csv"),
        os.path.join(os.path.dirname(__file__), "Dados/df_macro.csv"),
    ]
    for c in candidatos:
        if os.path.exists(c):
            return os.path.abspath(c)
    raise FileNotFoundError("Base de dados df_macro.csv não encontrada nos caminhos padrão.")


# ==============================================================================
# 1. IMPLEMENTAÇÃO DO ALGORITMO APRIORI (ESTADO DA ARTE)
# ==============================================================================

class AprioriMiner:
    """
    Implementação pura e autônoma do Algoritmo Apriori (Agrawal & Srikant, 1994)
    com poda por antimonotonicidade do suporte e cálculo de métricas SOTA:
    - Suporte (Sup), Confiança (Conf), Lift, Convicção, Alavancagem e Teste de Fisher.
    """

    def __init__(self, min_sup=0.08, min_conf=0.55, min_lift=1.15):
        self.min_sup = min_sup
        self.min_conf = min_conf
        self.min_lift = min_lift
        self.frequent_itemsets = {}
        self.rules = []

    def fit(self, transactions):
        N = len(transactions)
        if N == 0:
            return self

        # 1. Geração de 1-itemsets frequentes (L1)
        item_counts = {}
        for t in transactions:
            for item in t:
                k = frozenset([item])
                item_counts[k] = item_counts.get(k, 0) + 1

        current_L = {item: count / N for item, count in item_counts.items() if count / N >= self.min_sup}
        self.frequent_itemsets = dict(current_L)
        k = 2

        # 2. Busca em nível com poda anti-monótona
        while current_L:
            prev_items = list(current_L.keys())
            candidates = set()
            m = len(prev_items)
            for i in range(m):
                for j in range(i + 1, m):
                    union = prev_items[i] | prev_items[j]
                    if len(union) == k:
                        if all(frozenset(sub) in current_L for sub in combinations(union, k - 1)):
                            candidates.add(union)

            c_counts = {}
            for t in transactions:
                for c in candidates:
                    if c.issubset(t):
                        c_counts[c] = c_counts.get(c, 0) + 1

            current_L = {c: count / N for c, count in c_counts.items() if count / N >= self.min_sup}
            self.frequent_itemsets.update(current_L)
            k += 1

        # 3. Geração de Regras de Associação Válidas
        self.rules = []
        for itemset, sup_itemset in self.frequent_itemsets.items():
            if len(itemset) >= 2:
                for r in range(1, len(itemset)):
                    for ant in combinations(itemset, r):
                        ant = frozenset(ant)
                        cons = itemset - ant
                        sup_ant = self.frequent_itemsets.get(ant)
                        sup_cons = self.frequent_itemsets.get(cons)
                        if sup_ant and sup_cons:
                            conf = sup_itemset / sup_ant
                            if conf >= self.min_conf:
                                lift = conf / sup_cons
                                if lift >= self.min_lift:
                                    leverage = sup_itemset - (sup_ant * sup_cons)
                                    conv = (1.0 - sup_cons) / (1.0 - conf) if conf < 1.0 else 999.0
                                    
                                    # Teste Exato de Fisher
                                    a = int(round(sup_itemset * N))
                                    b = int(round((sup_ant - sup_itemset) * N))
                                    c = int(round((sup_cons - sup_itemset) * N))
                                    d = N - a - b - c
                                    try:
                                        _, pval = stats.fisher_exact([[a, b], [c, d]], alternative="greater")
                                    except Exception:
                                        pval = 1.0

                                    self.rules.append({
                                        "antecedente": sorted(list(ant)),
                                        "consequente": sorted(list(cons)),
                                        "ant_str": " & ".join(sorted(list(ant))),
                                        "cons_str": " & ".join(sorted(list(cons))),
                                        "tam_ant": len(ant),
                                        "tam_cons": len(cons),
                                        "suporte": sup_itemset,
                                        "sup_ant": sup_ant,
                                        "sup_cons": sup_cons,
                                        "confianca": conf,
                                        "lift": lift,
                                        "conviccao": conv,
                                        "alavancagem": leverage,
                                        "p_valor": pval
                                    })
        return self


# ==============================================================================
# 2. DISCRETIZAÇÃO MACROECONÔMICA PURA (SEM DECOMPOSIÇÃO DO IPCA)
# ==============================================================================

def construir_transacoes(df):
    """
    Constrói a base transacional puramente MACROECONÔMICA.
    Remove totalmente correlações internas contábeis entre subíndices de preços
    (Alimentação, Transportes, etc.) e foca nos fatores geradores de inflação:
    Câmbio, Atacado/Commodities, Juros, Mercado de Trabalho, Demanda e Choques.
    """
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    df["Desemprego"] = df["Desemprego"].ffill()
    df["Consumo_Energia_Total"] = df["Consumo_Energia_Total"].ffill()
    df["Produção_Derivados_Petróleo"] = df["Produção_Derivados_Petróleo"].ffill()
    df["Consumo_Gasolina"] = df["Consumo_Gasolina"].ffill()
    df["Estoque_Empregos_Formais_Total"] = df["Estoque_Empregos_Formais_Total"].ffill()

    transacoes_sincronas = []
    transacoes_temporais = []

    for i in range(len(df)):
        row = df.iloc[i]
        items_sinc = set()

        # 1. Alvo Único Macroeconômico: Regime do IPCA Geral (CMN / BACEN)
        if row["IPCA"] > 0.50:
            items_sinc.add("IPCA_Alta")
        elif row["IPCA"] <= 0.00:
            items_sinc.add("IPCA_Deflacao")
        else:
            items_sinc.add("IPCA_Meta")

        # 2. Câmbio e Repasse Cambial (Exchange Rate Pass-Through)
        if row["USDBRL"] > 5.00:
            items_sinc.add("Dolar_Alto")
        elif row["USDBRL"] < 3.20:
            items_sinc.add("Dolar_Baixo")

        # 3. Custos no Atacado e Cadeia de Insumos (IGP-M)
        if row["IGP_M"] > 0.80:
            items_sinc.add("IGP_M_Alto")
        elif row["IGP_M"] < 0.00:
            items_sinc.add("IGP_M_Deflacao")

        # 4. Política Monetária (Taxa SELIC)
        if row["SELIC"] > 0.90:  # > 11.3% a.a.
            items_sinc.add("SELIC_Restritiva")
        elif row["SELIC"] < 0.55:  # < 6.8% a.a.
            items_sinc.add("SELIC_Estimulativa")

        # 5. Mercado de Trabalho e Atividade Real (Curva de Phillips)
        if row["Desemprego"] < 8.5:
            items_sinc.add("Desemprego_Baixo")
        elif row["Desemprego"] > 11.5:
            items_sinc.add("Desemprego_Alto")

        # 6. Dinâmica Mensal e Choques Exógenos
        if i > 0:
            prev = df.iloc[i - 1]
            if row["USDBRL"] - prev["USDBRL"] > 0.05:
                items_sinc.add("Dolar_Acelerando")
            if row["SELIC"] - prev["SELIC"] > 0.00:
                items_sinc.add("SELIC_Aperto")
            if row["Consumo_Energia_Total"] - prev["Consumo_Energia_Total"] > 500:
                items_sinc.add("Energia_Demanda_Alta")
            if row["Produção_Derivados_Petróleo"] - prev["Produção_Derivados_Petróleo"] > 100:
                items_sinc.add("Petroleo_Choque_Oferta")

        transacoes_sincronas.append(items_sinc)

        # Transação Causal-Temporal: Antecedentes estritamente em t-1, Consequente em t
        if i > 0:
            prev = df.iloc[i - 1]
            items_temp = set()

            if prev["IPCA"] > 0.50:
                items_temp.add("IPCA_Alta_lag1")
            elif prev["IPCA"] <= 0.00:
                items_temp.add("IPCA_Deflacao_lag1")
            else:
                items_temp.add("IPCA_Meta_lag1")

            if prev["USDBRL"] > 5.00:
                items_temp.add("Dolar_Alto_lag1")
            elif prev["USDBRL"] < 3.20:
                items_temp.add("Dolar_Baixo_lag1")
            if row["USDBRL"] - prev["USDBRL"] > 0.05:
                items_temp.add("Dolar_Acelerando_lag1")

            if prev["IGP_M"] > 0.80:
                items_temp.add("IGP_M_Alto_lag1")
            elif prev["IGP_M"] < 0.00:
                items_temp.add("IGP_M_Deflacao_lag1")

            if prev["SELIC"] > 0.90:
                items_temp.add("SELIC_Restritiva_lag1")
            if row["SELIC"] - prev["SELIC"] > 0.00:
                items_temp.add("SELIC_Aperto_lag1")

            if prev["Desemprego"] < 8.5:
                items_temp.add("Desemprego_Baixo_lag1")
            elif prev["Desemprego"] > 11.5:
                items_temp.add("Desemprego_Alto_lag1")

            # Alvo Contemporâneo em t
            if row["IPCA"] > 0.50:
                items_temp.add("TARGET_IPCA_Alta")
            elif row["IPCA"] <= 0.00:
                items_temp.add("TARGET_IPCA_Deflacao")
            else:
                items_temp.add("TARGET_IPCA_Meta")

            transacoes_temporais.append(items_temp)

    return transacoes_sincronas, transacoes_temporais, df


# ==============================================================================
# 3. GERAÇÃO DE VISUALIZAÇÕES EM ALTA RESOLUÇÃO (300 DPI)
# ==============================================================================

def gerar_graficos_publicacao(df_regras_sinc, df_regras_temp, itemsets_dict, output_dirs):
    """Gera o comitê oficial de figuras em 300 DPI focado puramente em macroeconomia."""
    for d in output_dirs:
        os.makedirs(d, exist_ok=True)

    # FIGURA 18: Dispersão Suporte vs Confiança colorido por Lift
    plt.figure(figsize=(10, 6), dpi=300)
    sc = plt.scatter(
        df_regras_sinc["suporte"] * 100,
        df_regras_sinc["confianca"] * 100,
        c=df_regras_sinc["lift"],
        s=df_regras_sinc["tam_ant"] * 70,
        cmap="viridis",
        alpha=0.88,
        edgecolors="k",
        linewidth=0.6
    )
    cbar = plt.colorbar(sc)
    cbar.set_label("Lift (Razão de Dependência Estatística)", fontsize=11, fontweight="bold")
    plt.title("Figura 18 – Espaço de Regras Macroeconômicas Exógenas: Suporte vs Confiança",
              fontsize=12, fontweight="bold", pad=15)
    plt.xlabel("Suporte Amostral (%)", fontsize=11, fontweight="bold")
    plt.ylabel("Confiança Condicional (%)", fontsize=11, fontweight="bold")
    plt.grid(True, linestyle="--", alpha=0.5)

    top_regras = df_regras_sinc.sort_values("lift", ascending=False).head(3)
    for _, r in top_regras.iterrows():
        plt.annotate(
            f"{r['ant_str'][:22]}... → {r['cons_str']}\n(Lift: {r['lift']:.2f})",
            xy=(r["suporte"] * 100, r["confianca"] * 100),
            xytext=(r["suporte"] * 100 + 0.6, r["confianca"] * 100 - 3),
            fontsize=8,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc="#ffffcc", ec="gray", lw=0.5),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2", color="black", lw=0.7)
        )

    plt.tight_layout()
    for d in output_dirs:
        plt.savefig(os.path.join(d, "Figura_18_Dispersao_Suporte_Confianca_Lift.png"), dpi=300)
    plt.close()

    # FIGURA 19: Grafo Bipartido de Rede de Regras Macroeconômicas
    plt.figure(figsize=(12, 7), dpi=300)
    ax = plt.subplot(111)

    regras_rede = df_regras_sinc[df_regras_sinc["consequente"].apply(
        lambda c: "IPCA_Alta" in c or "IPCA_Meta" in c or "SELIC_Restritiva" in c
    )].sort_values("lift", ascending=False).head(8)

    antecedentes_unicos = list(dict.fromkeys([r["ant_str"] for _, r in regras_rede.iterrows()]))
    consequentes_unicos = list(dict.fromkeys([r["cons_str"] for _, r in regras_rede.iterrows()]))

    y_ant = np.linspace(0.85, 0.15, len(antecedentes_unicos))
    y_cons = np.linspace(0.75, 0.25, len(consequentes_unicos))

    pos_ant = {ant: (0.15, y) for ant, y in zip(antecedentes_unicos, y_ant)}
    pos_cons = {cons: (0.85, y) for cons, y in zip(consequentes_unicos, y_cons)}

    for _, r in regras_rede.iterrows():
        p1 = pos_ant[r["ant_str"]]
        p2 = pos_cons[r["cons_str"]]
        lw = min(4.0, max(1.2, r["confianca"] * 3.5))
        alpha = min(0.9, max(0.4, (r["lift"] - 1.0) / 2.0))
        ax.annotate(
            "",
            xy=p2, xycoords="data",
            xytext=p1, textcoords="data",
            arrowprops=dict(arrowstyle="-|>", color="#1f77b4", lw=lw, alpha=alpha,
                            mutation_scale=15, connectionstyle="arc3,rad=0.08")
        )
        mid_x = (p1[0] + p2[0]) / 2.0
        mid_y = (p1[1] + p2[1]) / 2.0 + 0.02
        ax.text(mid_x, mid_y, f"Lift: {r['lift']:.2f}\nConf: {r['confianca']:.0%}",
                fontsize=7.5, color="#333333", ha="center",
                bbox=dict(boxstyle="square,pad=0.2", fc="white", ec="lightgray", lw=0.5, alpha=0.9))

    for ant, (x, y) in pos_ant.items():
        ax.scatter(x, y, s=550, color="#2ca02c", edgecolors="k", zorder=5)
        ax.text(x - 0.02, y, ant, fontsize=8.5, fontweight="bold", ha="right", va="center")

    for cons, (x, y) in pos_cons.items():
        cor = "#d62728" if "Alta" in cons else "#1f77b4"
        ax.scatter(x, y, s=700, color=cor, edgecolors="k", zorder=5)
        ax.text(x + 0.02, y, cons, fontsize=9.5, fontweight="bold", ha="left", va="center")

    ax.set_xlim(-0.35, 1.35)
    ax.set_ylim(0.05, 0.95)
    ax.axis("off")
    plt.title("Figura 19 – Grafo Relacional Macroeconômico: Choques Exógenos → Regimes de Inflação & SELIC",
              fontsize=12, fontweight="bold", pad=15)
    plt.tight_layout()
    for d in output_dirs:
        plt.savefig(os.path.join(d, "Figura_19_Grafo_Rede_Regras_Associacao.png"), dpi=300)
    plt.close()

    # FIGURA 20: Distribuição de Itemsets Frequentes por Tamanho k
    plt.figure(figsize=(10, 5), dpi=300)
    tamanhos = [len(itemset) for itemset in itemsets_dict.keys()]
    contagem_tam = pd.Series(tamanhos).value_counts().sort_index()

    ax = sns.barplot(x=contagem_tam.index, y=contagem_tam.values, palette="Blues_d", hue=contagem_tam.index, legend=False, edgecolor="black")
    for p in ax.patches:
        ax.annotate(f"{int(p.get_height())}",
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="center", xytext=(0, 7), textcoords="offset points",
                    fontsize=10, fontweight="bold")

    plt.title("Figura 20 – Distribuição de Itemsets Frequentes Macroeconômicos por Tamanho k (MinSup = 8%)",
              fontsize=12, fontweight="bold", pad=15)
    plt.xlabel("Tamanho do Itemset (k-itemset)", fontsize=11, fontweight="bold")
    plt.ylabel("Quantidade de Itemsets Descobertos", fontsize=11, fontweight="bold")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    for d in output_dirs:
        plt.savefig(os.path.join(d, "Figura_20_Distribuicao_Itemsets_Frequentes.png"), dpi=300)
    plt.close()

    # FIGURA 21: Matriz de Calor de Interações Antecedente vs Consequente
    plt.figure(figsize=(11, 6), dpi=300)
    top_10 = df_regras_sinc[df_regras_sinc["consequente"].apply(lambda c: any("IPCA" in x or "SELIC" in x for x in c))].sort_values("lift", ascending=False).head(10)
    pivot_table = top_10.pivot_table(index="ant_str", columns="cons_str", values="lift", fill_value=1.0)

    sns.heatmap(pivot_table, annot=True, fmt=".2f", cmap="YlOrRd", cbar_kws={"label": "Lift Médio"},
                linewidths=1, linecolor="gray")
    plt.title("Figura 21 – Matriz de Dependência (Lift): Choques Macroeconômicos vs Regimes de Inflação",
              fontsize=12, fontweight="bold", pad=15)
    plt.xlabel("Consequente (Regime de Preços / Política Monetária)", fontsize=11, fontweight="bold")
    plt.ylabel("Antecedente (Conjunto de Choques Exógenos)", fontsize=11, fontweight="bold")
    plt.xticks(rotation=15, ha="right", fontsize=9)
    plt.yticks(rotation=0, fontsize=8.5)
    plt.tight_layout()
    for d in output_dirs:
        plt.savefig(os.path.join(d, "Figura_21_Matriz_Interacoes_Antecedente_Consequente.png"), dpi=300)
    plt.close()

    # FIGURA 22: Ranking de Regras Temporais Causais (Alerta Antecipado t-1 -> t)
    if len(df_regras_temp) > 0:
        plt.figure(figsize=(11, 6), dpi=300)
        top_temp = df_regras_temp.sort_values("lift", ascending=False).head(10)

        y_pos = np.arange(len(top_temp))
        bars = plt.barh(y_pos, top_temp["lift"], color="#2b5c8f", edgecolor="black", alpha=0.85)

        for i, (b, (_, r)) in enumerate(zip(bars, top_temp.iterrows())):
            plt.text(b.get_width() + 0.03, b.get_y() + b.get_height() / 2,
                     f"Lift: {r['lift']:.2f} | Conf: {r['confianca']:.0%} (p={r['p_valor']:.1e})",
                     va="center", fontsize=8.5, fontweight="bold", color="#111111")

        plt.yticks(y_pos, [f"{r['ant_str'][:35]} → {r['cons_str']}" for _, r in top_temp.iterrows()],
                   fontsize=8.5)
        plt.gca().invert_yaxis()
        plt.title("Figura 22 – Top 10 Regras Temporais Causais de Alerta Antecipado (t-1 → t) por Lift",
                  fontsize=12, fontweight="bold", pad=15)
        plt.xlabel("Lift (Razão de Dependência Estatística)", fontsize=11, fontweight="bold")
        plt.xlim(0, max(top_temp["lift"]) * 1.35)
        plt.grid(axis="x", linestyle="--", alpha=0.6)
        plt.tight_layout()
        for d in output_dirs:
            plt.savefig(os.path.join(d, "Figura_22_Regras_Temporais_Causais_Alerta.png"), dpi=300)
        plt.close()


# ==============================================================================
# 4. EXECUÇÃO INTEGRAL DO PIPELINE
# ==============================================================================

def main():
    print("=" * 80)
    print("🏛️ MINERAÇÃO MACROECONÔMICA PURA (SEM DECOMPOSIÇÃO CONTÁBIL DO IPCA)")
    print("Disciplina: Mineração de Dados - POLI / UPE | Prof. Dr. Alexandre Maciel")
    print("=" * 80)

    caminho_csv = localizar_base_dados()
    df = pd.read_csv(caminho_csv)
    print(f"✓ Base carregada com sucesso: {df.shape[0]} meses (2012–2026), {df.shape[1]} atributos.")

    trans_sinc, trans_temp, df_ordenado = construir_transacoes(df)
    print(f"✓ Transações Síncronas (h=0): {len(trans_sinc)} períodos.")
    print(f"✓ Transações Temporais (t-1 → t): {len(trans_temp)} períodos.")

    print("\n[Etapa 1/4] Executando Algoritmo Apriori Macroeconômico (MinSup=0.08, MinConf=0.55)...")
    miner_sinc = AprioriMiner(min_sup=0.08, min_conf=0.55, min_lift=1.15)
    miner_sinc.fit(trans_sinc)

    # Filtrar regras onde o consequente é o regime do IPCA ou Política SELIC (sem auto-correlação interna)
    regras_sinc_puras = [
        r for r in miner_sinc.rules
        if any("IPCA" in x or "SELIC" in x for x in r["consequente"]) and
           not (any("IPCA" in x for x in r["antecedente"]) and any("IPCA" in x for x in r["consequente"]))
    ]
    df_regras_sinc = pd.DataFrame(regras_sinc_puras).sort_values("lift", ascending=False).reset_index(drop=True)
    print(f"  → Itemsets Frequentes descobertos: {len(miner_sinc.frequent_itemsets)}")
    print(f"  → Regras Macroeconômicas Puras geradas: {len(df_regras_sinc)}")

    print("\n[Etapa 2/4] Executando Mineração Causal Multi-Horizonte (t-1 → t)...")
    miner_temp = AprioriMiner(min_sup=0.08, min_conf=0.50, min_lift=1.20)
    miner_temp.fit(trans_temp)

    regras_causais_filtradas = [
        r for r in miner_temp.rules
        if all(x.startswith("TARGET_") for x in r["consequente"]) and
           all(not x.startswith("TARGET_") for x in r["antecedente"])
    ]
    df_regras_temp = pd.DataFrame(regras_causais_filtradas).sort_values("lift", ascending=False).reset_index(drop=True)
    print(f"  → Regras Causais de Alerta geradas: {len(df_regras_temp)}")

    print("\n[Etapa 3/4] Avaliando a Consistência Temporal Out-of-Sample (OOS)...")
    df_ordenado["Date"] = pd.to_datetime(df_ordenado["Date"])
    mask_treino = df_ordenado["Date"] < "2022-01-01"
    idx_split = mask_treino.sum()

    trans_treino = trans_sinc[:idx_split]
    trans_teste = trans_sinc[idx_split:]
    N_tr = len(trans_treino)
    N_te = len(trans_teste)

    estabilidade = []
    for _, r in df_regras_sinc.iterrows():
        ant_set = frozenset(r["antecedente"])
        cons_set = frozenset(r["consequente"])
        uniao = ant_set | cons_set

        sup_ant_tr = sum(1 for t in trans_treino if ant_set.issubset(t)) / N_tr
        sup_uni_tr = sum(1 for t in trans_treino if uniao.issubset(t)) / N_tr
        conf_tr = sup_uni_tr / sup_ant_tr if sup_ant_tr > 0 else 0.0

        sup_ant_te = sum(1 for t in trans_teste if ant_set.issubset(t)) / N_te
        sup_uni_te = sum(1 for t in trans_teste if uniao.issubset(t)) / N_te
        conf_te = sup_uni_te / sup_ant_te if sup_ant_te > 0 else 0.0

        delta_conf = conf_te - conf_tr
        estabilidade.append({
            "conf_treino_2012_2021": conf_tr,
            "conf_teste_2022_2026": conf_te,
            "delta_conf_oos": delta_conf
        })

    df_estabilidade = pd.DataFrame(estabilidade)
    df_regras_sinc = pd.concat([df_regras_sinc, df_estabilidade], axis=1)

    print("\n[Etapa 4/4] Exportando Tabelas e Gráficos em Alta Resolução (300 DPI)...")
    diretorios_graficos = [
        os.path.abspath("Entrega_Classroom/9_Associacao/graficos"),
        os.path.abspath("Entrega_Classroom/4_Graficos_Alta_Resolucao")
    ]

    gerar_graficos_publicacao(df_regras_sinc, df_regras_temp, miner_sinc.frequent_itemsets, diretorios_graficos)

    caminho_regras = "Entrega_Classroom/9_Associacao/regras_associacao_sota.csv"
    caminho_itemsets = "Entrega_Classroom/9_Associacao/itemsets_frequentes_sota.csv"
    caminho_causais = "Entrega_Classroom/9_Associacao/regras_temporais_causais.csv"

    df_regras_sinc.to_csv(caminho_regras, index=False, encoding="utf-8")
    df_regras_temp.to_csv(caminho_causais, index=False, encoding="utf-8")

    itemsets_export = [
        {"itemset": " & ".join(sorted(list(k))), "tam": len(k), "suporte": v}
        for k, v in miner_sinc.frequent_itemsets.items()
    ]
    pd.DataFrame(itemsets_export).sort_values(["tam", "suporte"], ascending=[True, False]).to_csv(
        caminho_itemsets, index=False, encoding="utf-8"
    )

    print(f"✓ Tabela de Regras Síncronas salva: {caminho_regras}")
    print(f"✓ Tabela de Regras Causais salva: {caminho_causais}")
    print(f"✓ Tabela de Itemsets Frequentes salva: {caminho_itemsets}")

    print("\n" + "=" * 80)
    print("🏆 TOP 10 REGRAS MACROECONÔMICAS EXÓGENAS POR LIFT (SEM DECOMPOSIÇÃO)")
    print("=" * 80)
    cols_show = ["ant_str", "cons_str", "suporte", "confianca", "lift", "p_valor", "conf_teste_2022_2026"]
    print(df_regras_sinc[cols_show].head(10).to_string(index=False))

    print("\n" + "=" * 80)
    print("⚡ TOP 5 REGRAS TEMPORAIS CAUSAIS DE ALERTA ANTECIPADO (t-1 → t)")
    print("=" * 80)
    cols_temp = ["ant_str", "cons_str", "suporte", "confianca", "lift", "p_valor"]
    print(df_regras_temp[cols_temp].head(5).to_string(index=False))

    print("\n✓ Pipeline concluído com sucesso!")


if __name__ == "__main__":
    main()
