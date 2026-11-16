# Índices de Pobreza no Brasil — análise sob princípios FAIR

![Python](https://img.shields.io/badge/python-3.11+-blue) ![License: MIT](https://img.shields.io/badge/code-MIT-green) ![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey)

**Autores:** Yago Baltazar Ferreira, [PREENCHER 2º autor], [PREENCHER 3º autor]
**Disciplina:** Linguagem de Programação (Análise e Visualização de Dados com Python) — Bacharelado em Sistemas de Informação, 6º período, [PREENCHER semestre/ano]
**Instituição:** [PREENCHER]

## Resumo executivo
[PREENCHER: 3–5 linhas — tema, dados, método, principal achado.]

**Palavras-chave:** pobreza; extrema pobreza; vulnerabilidade social; indicadores públicos; Python; visualização de dados; FAIR.

## Artigo
Publicado em: https://[SEU-USUARIO].github.io/indices-pobreza-brasil/

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
