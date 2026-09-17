# 📁 Guia de Dados e Fontes Macroeconômicas

Este diretório armazena todas as bases de dados macroeconômicos e os respectivos scripts de coleta automatizada via API utilizados no projeto de pesquisa.

---

## 🗺️ 1. Estrutura de Pastas e Arquivos

```
Dados/
│
├── README.md                            # Guia geral e governança dos dados (este arquivo)
│
├── Brasil/                              # 🇧🇷 Base de dados do Brasil (Banco Central / SGS)
│   ├── README_BRASIL.md                 # Dicionário detalhado com códigos SGS/BACEN
│   ├── df_macro.csv                     # Base consolidada mensal (2012 a 2026)
│   └── coleta_dados_brasil_bcb.ipynb    # Script de coleta automatizada via API python-bcb
│
├── USA/                                 # 🇺🇸 Base de dados dos EUA (Federal Reserve / FRED)
│   ├── README_USA.md                    # Dicionário detalhado com códigos FRED
│   ├── dados_macroeconomicos_usa.csv    # Base consolidada mensal (2010 a 2026)
│   └── coleta_dados_usa_fred.ipynb      # Script de coleta automatizada via API FRED
│
└── [Arquivos de Compatibilidade]        # Mantidos na raiz para retrocompatibilidade com notebooks legados
    ├── df_macro.csv
    ├── dados_macro.ipynb
    └── dados_USA/
```

---

## 🏛️ 2. Resumo Comparativo das Fontes Oficiais

| Parâmetro | 🇧🇷 Brasil (`Dados/Brasil/`) | 🇺🇸 Estados Unidos (`Dados/USA/`) |
| :--- | :--- | :--- |
| **Fonte Primária** | **Banco Central do Brasil (BACEN)** | **Federal Reserve Bank of St. Louis** |
| **Sistema / API** | SGS (*Sistema Gerenciador de Séries Temporais*) via `python-bcb` | FRED (*Federal Reserve Economic Data*) via `pandas_datareader` |
| **Variável Alvo ($y$)** | **`IPCA`** (Índice de Preços ao Consumidor Amplo - Var. % Mensal) | **`Inflacao_CPI`** (Consumer Price Index for All Urban Consumers) |
| **Período Histórico** | Março/2012 a 2026 (marco metodológico PNAD/POF) | Janeiro/2010 a 2026 |
| **Periodicidade Final** | Mensal (`MS` - Month Start) | Mensal (`MS` - Month Start) |
| **Total de Variáveis** | 29 variáveis (1 Alvo + 28 Exógenas) | 20 variáveis (1 Alvo + 19 Exógenas) |
| **Tratamento de Faltantes**| Preenchimento estocástico / interpolação sem *lookahead bias* | Reamostragem (`first()`) para diários e *Forward Fill* (`ffill`) para trimestrais |

> [!NOTE]
> **Marco Amostral Inicial (Março/2012):** A escolha de 2012 fundamenta-se na mudança de critério na mensuração do desemprego pelo IBGE (substituição da PME restrita a 6 capitais pela PNAD Contínua de abrangência nacional), na atualização da matriz de ponderação do IPCA (POF 2008-2009) e na padronização contínua das séries desagregadas do SGS/BACEN, prevenindo quebras estruturais espúrias.

---

## 📊 3. Categorização das Variáveis Coletadas

### 🇧🇷 Brasil
1. **Índices de Preços e Desagregações:** `IPCA` *(Target)*, `IPCA_Transportes`, `IPCA Alimentação_bebidas`, `INPC_Habitação`, `IPCA_Saúde_cuidados_pessoais`, `IPCA_Vestuário`, `IPCA_Educação`, `IPCA_Despesas_Pessoais`, `INPC`, `IGP_M`, `IGP_DI`, `IPC_BR`.
2. **Setor Financeiro e Câmbio:** `SELIC` (Taxa de Juros Over), `USDBRL` (Taxa de Câmbio PTAX), `Reservas Internacionais`.
3. **Atividade Econômica e Emprego:** `PIB Mensal`, `Desemprego` (PNAD Contínua), `SalMinimo`, `Estoque_Empregos_Formais_Total` (CAGED), `Estoque_Empregos_Formais_Agropecuária`, `Estoque_Empregos_Formais_Construção`, `QteOvos`.
4. **Energia e Combustíveis:** `Produção_Derivados_Petróleo`, `Consumo_Gasolina`, `Consumo_Óleo_Combustível`, `Consumo_Energia_Comercial`, `Consumo_Energia_Residencial`, `Consumo_Energia_Total`.

### 🇺🇸 Estados Unidos
1. **Índices de Preços e Inflação:** `Inflacao_CPI` *(Target)*, `Inflacao_CPI_Core` (Núcleo de Inflação), `PCE` (Índice de Preços dos Gastos de Consumo Pessoal), `PCE_Core`, `Deflator_PIB`.
2. **Mercado Financeiro e Títulos:** `Taxa_Juros_Fed` (Federal Funds Rate), `Indice_Dolar` (Trade Weighted U.S. Dollar Index), `TIPS_5_anos_nominal`, `TIPS_5_anos_infl_ajustado` (Títulos do Tesouro indexados à inflação).
3. **Mercado de Trabalho e Salários:** `Desemprego` (Civilian Unemployment Rate), `Desemprego_menos_27_semanas`, `Emprego_Total_Nao_Agricola` (Total Nonfarm Payrolls), `Salario_Medio`, `Salario_Medio_Real_Hora`.
4. **Atividade Econômica e Indústria:** `PIB`, `PIB_Real`, `Producao_Industrial`, `Capacidade_Instalada` (Total Capacity Utilization), `Permissoes_Construcao` (New Private Housing Units Authorized).

---

## 🔄 4. Como Atualizar as Bases de Dados

Para reexecutar a extração e puxar dados atualizados diretamente das APIs:

* **Brasil:** Abra e execute o notebook [`Dados/Brasil/coleta_dados_brasil_bcb.ipynb`](file:///c:/Users/Operador/Desktop/Mineração%20de%20dados/Dados/Brasil/coleta_dados_brasil_bcb.ipynb).
* **EUA:** Abra e execute o notebook [`Dados/USA/coleta_dados_usa_fred.ipynb`](file:///c:/Users/Operador/Desktop/Mineração%20de%20dados/Dados/USA/coleta_dados_usa_fred.ipynb).
