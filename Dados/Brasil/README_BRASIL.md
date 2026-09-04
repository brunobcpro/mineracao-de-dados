# 🇧🇷 Dicionário de Dados Macroeconômicos: Brasil

- **Fonte Oficial:** Banco Central do Brasil (BACEN) / Sistema Gerenciador de Séries Temporais (SGS)
- **Arquivo de Dados:** [`df_macro.csv`](file:///c:/Users/Operador/Desktop/Mineração%20de%20dados/Dados/Brasil/df_macro.csv)
- **Script de Coleta:** [`coleta_dados_brasil_bcb.ipynb`](file:///c:/Users/Operador/Desktop/Mineração%20de%20dados/Dados/Brasil/coleta_dados_brasil_bcb.ipynb)
- **Período Histórico:** Março de 2012 a 2026 (frequência mensal contínua)
- **Frequência:** Mensal (`MS` - Início do Mês)

### 📌 Por que o marco inicial em Março de 2012?
A série histórica foi delimitada a partir de **março de 2012** devido a critérios metodológicos essenciais das fontes estatísticas oficiais:
1. **Transição Metodológica do Desemprego (PME ➔ PNAD Contínua):** Até o início de 2012, o IBGE mensurava o desemprego pela PME, restrita a 6 regiões metropolitanas. Em 2012 iniciou-se a PNAD Contínua com cobertura nacional e padrão OIT. As duas séries são estatisticamente incompatíveis e empilhá-las provocaria uma severa quebra estrutural (*structural break*).
2. **Atualização da Ponderação do IPCA (POF 2008-2009):** Em janeiro de 2012 entrou em vigor a nova matriz de ponderação da cesta de consumo do IPCA baseada na POF 2008-2009, reestruturando a relevância de grupos essenciais como Alimentação e Transportes.
3. **Painel Balanceado no SGS/BACEN:** Diversas séries setoriais de energia, refino de derivados e estoques compatibilizados do CAGED passaram a ser disponibilizadas com preenchimento ininterrupto a partir do início de 2012, permitindo a construção de um painel balanceado sem necessidade de imputações artificiais.

---

## 📋 Tabela Completa de Metadados e Variáveis

| Nome da Coluna | Código SGS (BACEN) | Categoria | Unidade | Descrição / Significado Econômico |
| :--- | :---: | :--- | :--- | :--- |
| **`Date`** | - | Temporal | `AAAA-MM-DD` | Data de referência da observação mensal. |
| **`IPCA`** *(Target)* | **4447** | **Índice de Preços** | % a.m. | **Índice Nacional de Preços ao Consumidor Amplo (Meta de Inflação do BACEN)**. |
| `IPCA_Transportes` | 1639 | Desagregação IPCA | % a.m. | Variação mensal do grupo Transportes (combustíveis, passagens, veículos). |
| `IPCA Alimentação_bebidas` | 1635 | Desagregação IPCA | % a.m. | Variação mensal do grupo Alimentação e Bebidas no domicílio e fora. |
| `INPC_Habitação` | 1636 / 1645 | Desagregação IPCA | % a.m. | Variação mensal de custos de habitação (aluguel, energia elétrica residencial). |
| `IPCA_Saúde_cuidados_pessoais` | 1641 | Desagregação IPCA | % a.m. | Variação de produtos farmacêuticos, planos de saúde e serviços pessoais. |
| `IPCA_Vestuário` | 1638 | Desagregação IPCA | % a.m. | Variação de roupas, calçados e acessórios. |
| `IPCA_Educação` | 1643 | Desagregação IPCA | % a.m. | Variação de mensalidades escolares, cursos e material didático. |
| `IPCA_Despesas_Pessoais` | 1642 | Desagregação IPCA | % a.m. | Variação de serviços diversos, lazer e recreação. |
| `INPC` | 188 | Índice de Preços | % a.m. | Índice Nacional de Preços ao Consumidor (famílias com renda de 1 a 5 salários mínimos). |
| `IGP_M` | 189 | Índice de Preços | % a.m. | Índice Geral de Preços do Mercado (FGV) - sensível ao atacado e câmbio. |
| `IGP_DI` | 190 | Índice de Preços | % a.m. | Índice Geral de Preços - Disponibilidade Interna (FGV). |
| `IPC_BR` | 191 | Índice de Preços | % a.m. | Índice de Preços ao Consumidor - Brasil (FGV). |
| `SELIC` | 4390 | Setor Financeiro | % a.m. | Taxa de juros média nominal fixada pelo COPOM (Taxa Over/Selic). |
| `USDBRL` | 3696 | Câmbio | R$/US$ | Taxa de câmbio do Dólar Comercial (PTAX de venda fim de período). |
| `Reservas Internacionais` | 3546 | Setor Externo | US$ Milhões | Volume total de reservas internacionais de liquidez do Brasil. |
| `PIB Mensal` | 4380 | Atividade Econômica | R$ Milhões | Estimativa mensal do Produto Interno Bruto (valores correntes). |
| `Desemprego` | 24369 | Mercado de Trabalho| % | Taxa de desocupação mensal da PNAD Contínua (IBGE). |
| `SalMinimo` | 1619 | Mercado de Trabalho| R$ | Valor nominal do Salário Mínimo nacional fixado por lei. |
| `Estoque_Empregos_Formais_Total` | 28763 | Emprego Formal | Vínculos | Estoque total de empregados celetistas formais (CAGED). |
| `Estoque_Empregos_Formais_Agropecuária` | 28764 | Emprego Formal | Vínculos | Estoque de postos formais no setor agropecuário (CAGED). |
| `Estoque_Empregos_Formais_Construção` | 28770 | Emprego Formal | Vínculos | Estoque de postos formais na construção civil (CAGED). |
| `QteOvos` | 1310 | Agropecuária | Dúzias (Mil) | Produção agropecuária de ovos de galinha (indicador de oferta de alimentos). |
| `Produção_Derivados_Petróleo` | 1391 | Energia | Mil m³ | Volume de derivados de petróleo produzidos no país. |
| `Consumo_Gasolina` | 1393 | Energia / Combustível| Mil m³ | Consumo aparente mensal de gasolina automotiva. |
| `Consumo_Óleo_Combustível` | 1395 | Energia / Combustível| Mil m³ | Consumo aparente mensal de óleo combustível industrial. |
| `Consumo_Energia_Comercial` | 1402 | Energia Elétrica | GWh | Consumo de energia elétrica na classe comercial. |
| `Consumo_Energia_Residencial` | 1403 | Energia Elétrica | GWh | Consumo de energia elétrica na classe residencial. |
| `Consumo_Energia_Total` | 1406 | Energia Elétrica | GWh | Consumo total de energia elétrica em todas as classes (comercial, residencial, industrial). |
