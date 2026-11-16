# Dicionário de dados

**Fonte:** Kaggle — [Índices de Pobreza no Brasil](https://www.kaggle.com/datasets/fidelissauro/indices-pobreza-brasil)
**Arquivo processado:** `data/processed/dados_limpos.parquet` (também em `dados_limpos.csv.gz`)
**Granularidade:** [PREENCHER: uma linha = ?  ex.: um estado em um ano]

> Como preencher: rode `python -m src.etl --dictionary`, abra `data/data_dictionary_rascunho.md`,
> complete as colunas "Formato" e "Significado" e cole a tabela abaixo. Apague este aviso.

| Variável | Tipo | Formato | Não nulos | Exemplo | Significado |
|---|---|---|---|---|---|
| `[PREENCHER]` | [string/float/int/datetime] | [ex.: percentual 0–100] | [n] | [ex.] | [significado no domínio da pesquisa] |

## Tratamentos aplicados
Ver `data/processed/etl_report.json` (gerado a cada execução do ETL): colunas renomeadas para snake_case, valores `-`/`NA` convertidos em nulo, números em formato pt-BR convertidos para `float`, duplicatas exatas contadas e removidas, imputação (se usada) sinalizada em colunas `*_imputado`.

## Licença
Dicionário e dados derivados: CC BY 4.0 (ver `data/LICENSE_DATA.txt`).
