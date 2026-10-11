from pathlib import Path
import streamlit as st
from src.pipeline_ops import impute_missing_values, compare_schemas
from src.ui_components import render_download_button

SILVER_DIR = Path("data/02_silver")

def render_cleaning():
    st.subheader("🧹 3. Tratamento e Qualificação - Camada Silver")
    df_raw = st.session_state.df_raw

    colunas_numericas = df_raw.select_dtypes(include="number").columns.tolist()
    colunas_categoricas = df_raw.select_dtypes(exclude="number").columns.tolist()

    st.markdown("#### Configurar Regras de Limpeza")
    col1, col2 = st.columns(2)
    with col1:
        col_num = st.selectbox("Imputar nulos numéricos (Mediana):", [None] + colunas_numericas)
    with col2:
        col_cat = st.selectbox("Imputar nulos categóricos (Moda):", [None] + colunas_categoricas)

    total_dupes = int(df_raw.duplicated().sum())
    remove_dupes = st.checkbox(
        f"Remover duplicatas ({total_dupes} registros identificados)",
        value=(total_dupes > 0),
    )

    if st.button("🚀 Aplicar Limpeza e Persistir na Silver", type="primary"):
        df_working = df_raw.copy()
        if remove_dupes:
            df_working = df_working.drop_duplicates()

        df_cleaned, _ = impute_missing_values(df_working, col_num=col_num, col_cat=col_cat)

        st.session_state.df_silver = df_cleaned
        st.session_state.df_gold = df_cleaned.copy()

        silver_path = SILVER_DIR / st.session_state.raw_file_name
        df_cleaned.to_csv(silver_path, index=False)
        st.success(f"Camada Silver atualizada e gravada em `{silver_path}`!")

    st.divider()

    st.markdown("#### Auditoria Volumétrica (Raw ➔ Silver)")
    rows_raw = len(df_raw)
    rows_silver = len(st.session_state.df_silver)
    delta_rows = rows_silver - rows_raw
    pct_change = (delta_rows / rows_raw) * 100 if rows_raw > 0 else 0

    nulls_raw = int(df_raw.isna().sum().sum())
    nulls_silver = int(st.session_state.df_silver.isna().sum().sum())
    delta_nulls = nulls_silver - nulls_raw

    m1, m2, m3 = st.columns(3)
    m1.metric("Linhas Finais", f"{rows_silver:,}", delta=f"{delta_rows} ({pct_change:.2f}%)")
    m2.metric("Nulos Restantes", f"{nulls_silver:,}", delta=f"{delta_nulls}", delta_color="inverse")
    m3.metric("Duplicatas Restantes", f"{st.session_state.df_silver.duplicated().sum():,}")

    st.markdown("#### Schema Comparativo")
    schema_diff = compare_schemas(df_raw, st.session_state.df_silver)
    st.dataframe(schema_diff, use_container_width=True, hide_index=True)

    render_download_button(st.session_state.df_silver, "silver", st.session_state.raw_file_name)
    st.dataframe(st.session_state.df_silver.head(10), use_container_width=True)