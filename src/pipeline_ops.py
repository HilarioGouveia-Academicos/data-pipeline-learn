"""
Módulo de operações puras de transformação para o pipeline didático.
Responsável pelas regras de negócio e logs de execução.
"""
import logging
from typing import Optional, Tuple
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)


def impute_missing_values(
    df: pd.DataFrame,
    col_num: Optional[str] = None,
    col_cat: Optional[str] = None,
) -> Tuple[pd.DataFrame, dict]:
    """Imputa valores ausentes (mediana para numéricas, moda para categóricas)

    e retorna métricas do impacto.
    """
    df_out = df.copy()
    stats = {"num_imputed": 0, "cat_imputed": 0}

    if col_num and col_num in df_out.columns:
        n_missing = int(df_out[col_num].isna().sum())
        if n_missing > 0:
            median_val = df_out[col_num].median()
            df_out[col_num] = df_out[col_num].fillna(median_val)
            stats["num_imputed"] = n_missing
            logging.info(
                "Coluna '%s': %d nulos preenchidos com mediana (%.2f)",
                col_num,
                n_missing,
                median_val,
            )

    if col_cat and col_cat in df_out.columns:
        n_missing = int(df_out[col_cat].isna().sum())
        if n_missing > 0:
            modes = df_out[col_cat].mode()
            if not modes.empty:
                mode_val = modes[0]
                df_out[col_cat] = df_out[col_cat].fillna(mode_val)
                stats["cat_imputed"] = n_missing
                logging.info(
                    "Coluna '%s': %d nulos preenchidos com moda ('%s')",
                    col_cat,
                    n_missing,
                    str(mode_val),
                )

    return df_out, stats


def apply_feature_engineering(
    df: pd.DataFrame,
    col_disc: Optional[str] = None,
    bins: int = 5,
    col_encode: Optional[str] = None,
) -> Tuple[pd.DataFrame, list]:
    """Aplica discretização e One-Hot Encoding, retornando o DataFrame e novas features."""
    df_out = df.copy()
    new_features = []

    if col_disc and col_disc in df_out.columns:
        feature_name = f"{col_disc}_faixa"
        df_out[feature_name] = pd.cut(df_out[col_disc], bins=bins).astype(str)
        new_features.append(feature_name)
        logging.info("Coluna '%s' discretizada em %d faixas.", col_disc, bins)

    if col_encode and col_encode in df_out.columns:
        dummies = pd.get_dummies(
            df_out[col_encode], prefix=col_encode, dtype=int
        )
        dummy_cols = dummies.columns.tolist()
        df_out = pd.concat([df_out, dummies], axis=1)
        new_features.extend(dummy_cols)
        logging.info(
            "One-Hot Encoding aplicado em '%s': %d novas colunas geradas.",
            col_encode,
            len(dummy_cols),
        )

    return df_out, new_features


def compare_schemas(df_before: pd.DataFrame, df_after: pd.DataFrame) -> pd.DataFrame:
    """Gera tabela comparativa de schema e tipos de dados."""
    all_cols = sorted(list(set(df_before.columns) | set(df_after.columns)))
    diff_records = []

    for col in all_cols:
        dtype_before = (
            str(df_before[col].dtype) if col in df_before.columns else "Ausente"
        )
        dtype_after = (
            str(df_after[col].dtype) if col in df_after.columns else "Removida"
        )

        status = "Inalterada"
        if dtype_before == "Ausente":
            status = "✨ Nova Feature"
        elif dtype_after == "Removida":
            status = "🗑️ Removida"
        elif dtype_before != dtype_after:
            status = "🔄 Tipo Modificado"

        diff_records.append(
            {
                "Coluna": col,
                "Tipo Anterior": dtype_before,
                "Tipo Atual": dtype_after,
                "Status": status,
            }
        )

    return pd.DataFrame(diff_records)