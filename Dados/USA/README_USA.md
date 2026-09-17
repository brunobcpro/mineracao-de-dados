# 🇺🇸 Dicionário de Dados Macroeconômicos: Estados Unidos

- **Fonte Oficial:** Federal Reserve Bank of St. Louis / FRED (*Federal Reserve Economic Data*)
- **Arquivo de Dados:** [`dados_macroeconomicos_usa.csv`](file:///c:/Users/Operador/Desktop/Mineração%20de%20dados/Dados/USA/dados_macroeconomicos_usa.csv)
- **Script de Coleta:** [`coleta_dados_usa_fred.ipynb`](file:///c:/Users/Operador/Desktop/Mineração%20de%20dados/Dados/USA/coleta_dados_usa_fred.ipynb)
- **Período Histórico:** Janeiro de 2010 a 2026 (frequência mensal contínua)
- **Frequência Final:** Mensal (`MS` - Início do Mês)

---

## 📋 Tabela Completa de Metadados e Variáveis

| Nome da Coluna | Código FRED | Categoria | Frequência Original / Tratamento | Descrição / Significado Econômico |
| :--- | :---: | :--- | :--- | :--- |
| **`DATE`** | - | Temporal | Mensal (`AAAA-MM-DD`) | Data de referência da observação mensal. |
| **`Inflacao_CPI`** *(Target)* | **`CPIAUCNS`** | **Índice de Preços** | Mensal | **Consumer Price Index for All Urban Consumers (Índice de Preços ao Consumidor EUA)**. |
| `Inflacao_CPI_Core` | `CPILFESL` | Índice de Preços | Mensal | Core CPI (Núcleo de Inflação sem Alimentos e Energia). |
| `PCE_Core` | `PCEPILFE` | Índice de Preços | Mensal | Core PCE Price Index (Medida de inflação preferencial do Federal Reserve). |
| `PCE` | `PCECTPI` | Índice de Preços | Trimestral (*Forward Fill* mensal) | Personal Consumption Expenditures: Chain-type Price Index. |
| `Deflator_PIB` | `GDPDEF` | Índice de Preços | Trimestral (*Forward Fill* mensal) | Gross Domestic Product: Implicit Price Deflator. |
| `Taxa_Juros_Fed` | `FEDFUNDS` | Taxa de Juros | Mensal | Federal Funds Effective Rate (Taxa básica de juros do Fed). |
| `Desemprego` | `UNRATE` | Mercado de Trabalho | Mensal | Civilian Unemployment Rate (Taxa de desocupação da população civil). |
| `Desemprego_menos_27_semanas` | `LNS13025701` | Mercado de Trabalho | Mensal | Número de desempregados por menos de 27 semanas (desemprego de curto prazo). |
| `Emprego_Total_Nao_Agricola` | `PAYEMS` | Mercado de Trabalho | Mensal | All Employees, Total Nonfarm (Total de empregados não agrícolas - Payroll). |
| `Salario_Medio` | `CES0500000003` | Salários | Mensal | Average Hourly Earnings of All Employees (Salário médio nominal por hora). |
| `Salario_Medio_Real_Hora` | `AHETPI` | Salários | Mensal | Average Hourly Earnings adjusted for inflation (Salário real por hora). |
| `Permissoes_Construcao` | `PERMIT` | Construção / Atividade | Mensal | New Privately Owned Housing Units Authorized in Permit-Issuing Places. |
| `Producao_Industrial` | `INDPRO` | Atividade Industrial | Mensal | Industrial Production Index (Índice de produção industrial geral). |
| `Capacidade_Instalada` | `TCU` | Atividade Industrial | Mensal | Total Capacity Utilization (Grau de utilização da capacidade instalada da indústria). |
| `PIB_Real` | `GDPC1` | Atividade Econômica | Trimestral (*Forward Fill* mensal) | Real Gross Domestic Product (PIB real ajustado pela inflação, US$ Bilhões). |
| `PIB` | `GDP` | Atividade Econômica | Trimestral (*Forward Fill* mensal) | Gross Domestic Product (PIB nominal em dólares correntes, US$ Bilhões). |
| `Indice_Dolar` | `DTWEXAFEGS` | Câmbio / Mercado | Diário (*Resample MS - First value*) | Trade Weighted U.S. Dollar Index: Advanced Foreign Economies. |
| `TIPS_5_anos_nominal` | `DGS5` | Renda Fixa / Títulos | Diário (*Resample MS - First value*) | Market Yield on U.S. Treasury Securities at 5-Year Constant Maturity. |
| `TIPS_5_anos_infl_ajustado` | `DFII5` | Expectativa de Inflação | Diário (*Resample MS - First value*) | 5-Year Treasury Inflation-Indexed Security (Yield real implícito de 5 anos). |
