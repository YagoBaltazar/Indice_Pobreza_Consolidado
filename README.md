# Índices de Pobreza no Brasil — análise sob princípios FAIR

![Python](https://img.shields.io/badge/python-3.11+-blue) ![License: MIT](https://img.shields.io/badge/code-MIT-green) ![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey)

**Autores:** Yago Baltazar Ferreira
**Disciplina:** Linguagem de Programação (Análise e Visualização de Dados com Python) — Bacharelado em Sistemas de Informação, 6º período, 2° semestre
**Instituição:** UniLasalle

## Resumo executivo
Análise da série mensal nacional de pobreza, extrema pobreza e vulnerabilidade (ago/2012 a set/2022, 122 meses), incluindo recortes de famílias, indígenas, quilombolas e ciganos. O pipeline em Python limpa, valida e recalcula os percentuais sobre a população estimada. A pobreza caiu de 9,99% para 4,46% da população, enquanto a extrema pobreza ficou em torno de 23%, com mínimo de 17,86% em 2016. Os grupos tradicionais registram crescimento expressivo na contagem em vulnerabilidade.

**Palavras-chave:** pobreza; extrema pobreza; vulnerabilidade social; indicadores públicos; Python; visualização de dados; FAIR.

## Artigo
Publicado em: https://github.com/YagoBaltazar/Indice_Pobreza_Consolidado/

## Fonte dos dados
Kaggle — Índices de Pobreza no Brasil: https://www.kaggle.com/datasets/fidelissauro/indices-pobreza-brasil

## Estrutura
```
├── README.md · LICENSE · requirements.txt · .gitignore
├── data/raw/ · data/processed/ · data/data_dictionary.md
├── notebooks/analise_exploratoria.ipynb
├── src/etl.py
└── docs/index.html · docs/assets/
```

## Como reproduzir
```bash
git clone https://github.com/[SEU-USUARIO]/indices-pobreza-brasil.git
cd indices-pobreza-brasil
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# coloque o CSV baixado do Kaggle em data/raw/
python -m src.etl --dictionary
jupyter lab notebooks/analise_exploratoria.ipynb
```

## Licenças
Código: MIT (`LICENSE`). Dados derivados, dicionário e texto: CC BY 4.0 (`data/LICENSE_DATA.txt`).
