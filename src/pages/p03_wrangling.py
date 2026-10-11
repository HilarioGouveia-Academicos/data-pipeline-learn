from pathlib import Path
import streamlit as st
from src.pipeline_ops import apply_feature_engineering, compare_schemas
from src.ui_components import render_download_button

GOLD_DIR = Path("data/03_gold")

def render_wrangling():
    st.subheader("🔧 4. Engenharia de Features - Camada Gold")
    df_silver = st.session_state.df_silver

    colunas_numericas = df_silver.select_dtypes(include="number").columns.tolist()
    colunas_categoricas = df_silver.select_dtypes(exclude="number").columns.tolist()

    st.markdown("#### Configurar Enriquecimento de Features")
    col1, col2 = st.columns(2)
    with col1:
        col_disc = st.selectbox("Discretizar variável contínua (Bins):", [None] + colunas_numericas)
        bins = st.slider("Quantidade de intervalos (Bins):", min_value=2, max_value=10, value=4)
    with col2:
        col_encode = st.selectbox("One-Hot Encoding (Variáveis Dummy):", [None] + colunas_categoricas)

    if st.button("⚡ Processar Features e Persistir na Gold", type="primary"):
        df_gold, new_cols = apply_feature_engineering(
            df_silver, col_disc=col_disc, bins=bins, col_encode=col_encode
        )
        st.session_state.df_gold = df_gold

        gold_path = GOLD_DIR / st.session_state.raw_file_name
        df_gold.to_csv(gold_path, index=False)
        st.success(f"Camada Gold persistida em `{gold_path}`! Novas colunas: {len(new_cols)}")

    st.divider()

    st.markdown("#### Comparativo de Atributos (Silver ➔ Gold)")
    g1, g2 = st.columns(2)
    cols_silver = df_silver.shape[1]
    cols_gold = st.session_state.df_gold.shape[1]
    g1.metric("Colunas Silver", cols_silver)
    g2.metric("Colunas Gold (Enriquecidas)", cols_gold, delta=f"+{cols_gold - cols_silver} features")

    schema_diff_gold = compare_schemas(df_silver, st.session_state.df_gold)
    st.dataframe(schema_diff_gold, use_container_width=True, hide_index=True)

    render_download_button(st.session_state.df_gold, "gold", st.session_state.raw_file_name)
    st.dataframe(st.session_state.df_gold.head(10), use_container_width=True)