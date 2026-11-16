"""ETL do projeto: Índices de Pobreza no Brasil.

Fonte: https://www.kaggle.com/datasets/fidelissauro/indices-pobreza-brasil

Uso (a partir da raiz do repositório):
    python -m src.etl                    # limpa e salva parquet + csv.gz
    python -m src.etl --impute           # imputa mediana, com coluna-flag de rastreio
    python -m src.etl --dictionary       # gera rascunho do dicionário de dados

Princípio: nenhuma operação destrutiva sem rastreabilidade. Tudo o que é
removido ou imputado é contado em data/processed/etl_report.json.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
from pandas.api import types as pt

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROC_DIR = ROOT / "data" / "processed"
NULL_TOKENS = ["", "-", "--", "NA", "N/A", "n/a", "nan", "NaN", "null", "NULL", "ND", "..."]


def snake_case(name: str) -> str:
    """'Taxa de Pobreza (%)' -> 'taxa_de_pobreza'."""
    s = unicodedata.normalize("NFKD", str(name)).encode("ascii", "ignore").decode()
    s = re.sub(r"[^0-9a-zA-Z]+", "_", s).strip("_").lower()
    return s or "coluna"


def find_raw_file() -> Path:
    files = sorted(RAW_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"Coloque o CSV baixado do Kaggle em {RAW_DIR}")
    return files[0]


def read_raw(path: Path | None = None) -> pd.DataFrame:
    """Lê o CSV testando codificações; o separador é detectado automaticamente."""
    path = path or find_raw_file()
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return pd.read_csv(path, sep=None, engine="python", encoding=enc, na_values=NULL_TOKENS)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Não foi possível decodificar {path}")


def _ptbr_to_float(s: pd.Series) -> pd.Series:
    t = s.astype(str).str.replace(r"[R$%\s]", "", regex=True)
    both = t.str.contains(",") & t.str.contains(r"\.")
    t = t.where(~both, t.str.replace(".", "", regex=False))
    t = t.str.replace(",", ".", regex=False)
    return pd.to_numeric(t, errors="coerce")


def clean(df: pd.DataFrame, impute: bool = False) -> tuple[pd.DataFrame, dict]:
    report: dict = {"linhas_entrada": int(len(df)), "colunas_entrada": [str(c) for c in df.columns]}
    df = df.copy()

    # 1) nomes de colunas padronizados (sem duplicatas)
    novos, vistos = [], {}
    for c in df.columns:
        n = snake_case(c)
        vistos[n] = vistos.get(n, 0) + 1
        novos.append(n if vistos[n] == 1 else f"{n}_{vistos[n]}")
    df.columns = novos

    # 2) texto sem espaços; tipos numéricos (formato pt-BR) e datas
    conversoes = {}
    for c in list(df.columns):
        if not (pt.is_object_dtype(df[c]) or pt.is_string_dtype(df[c])):
            continue
        df[c] = df[c].astype("string").str.strip().replace(NULL_TOKENS, pd.NA)
        validos = int(df[c].notna().sum())
        num = _ptbr_to_float(df[c])
        if validos and num.notna().sum() / validos >= 0.9:
            df[c], conversoes[c] = num, "numerico"
        elif re.search(r"data|date|periodo|mes", c):
            dt = pd.to_datetime(df[c], errors="coerce", dayfirst=True)
            if validos and dt.notna().sum() / validos >= 0.9:
                df[c], conversoes[c] = dt, "datetime"
    report["conversoes_de_tipo"] = conversoes

    # 3) duplicatas exatas (contadas, não silenciosas)
    dup = int(df.duplicated().sum())
    df = df.drop_duplicates().reset_index(drop=True)
    report["duplicatas_removidas"] = dup

    # 4) nulos: por padrão mantidos; com --impute usa mediana + coluna-flag
    nulos = df.isna().sum()
    report["nulos_por_coluna"] = {k: int(v) for k, v in nulos.items() if v}
    if impute:
        for c in df.select_dtypes(include=np.number).columns:
            if df[c].isna().any():
                df[f"{c}_imputado"] = df[c].isna()
                df[c] = df[c].fillna(df[c].median())
        report["imputacao"] = "mediana (colunas *_imputado marcam as linhas alteradas)"
    else:
        report["imputacao"] = "nenhuma (nulos preservados)"

    report["linhas_saida"] = int(len(df))
    report["tipos"] = {k: str(v) for k, v in df.dtypes.items()}
    return df, report


def save(df: pd.DataFrame, report: dict) -> None:
    PROC_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(PROC_DIR / "dados_limpos.parquet", index=False)
    df.to_csv(PROC_DIR / "dados_limpos.csv.gz", index=False, compression="gzip")
    (PROC_DIR / "etl_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def build_dictionary(df: pd.DataFrame) -> str:
    linhas = ["| Variável | Tipo | Formato | Não nulos | Exemplo | Significado |", "|---|---|---|---|---|---|"]
    for c in df.columns:
        ex = df[c].dropna().iloc[0] if df[c].notna().any() else ""
        linhas.append(f"| `{c}` | {df[c].dtype} | [PREENCHER] | {int(df[c].notna().sum())} | {ex} | [PREENCHER] |")
    return "\n".join(linhas)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raw", type=Path, help="caminho do CSV bruto")
    ap.add_argument("--impute", action="store_true", help="imputa mediana com flag de rastreio")
    ap.add_argument("--dictionary", action="store_true", help="gera data/data_dictionary_rascunho.md")
    a = ap.parse_args()
    df, rep = clean(read_raw(a.raw), impute=a.impute)
    save(df, rep)
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    if a.dictionary:
        (ROOT / "data" / "data_dictionary_rascunho.md").write_text(build_dictionary(df), encoding="utf-8")
        print("Rascunho salvo em data/data_dictionary_rascunho.md")


if __name__ == "__main__":
    main()
