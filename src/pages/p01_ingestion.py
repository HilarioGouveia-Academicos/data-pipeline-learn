import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from src.ui_components import render_download_button

def render_dataset():
    st.subheader("📦 1. Ingestão & Diagnóstico - Camada Bronze (Raw)")
    st.caption("Recebimento dos dados brutos e auditoria inicial de saúde dos dados.")

    df = st.session_state.df_raw

    # Abas didáticas: Uma para ver os dados brutos e outra para o diagnóstico profundo
    tab_dados, tab_profiling = st.tabs(["📋 Visão Geral & Dados", "📑 Diagnóstico de Qualidade (Profiling)"])

    with tab_dados:
        # Métricas rápidas de cabeçalho
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total de Linhas", f"{df.shape[0]:,}")
        c2.metric("Total de Colunas", df.shape[1])
        c3.metric("Valores Nulos", f"{df.isna().sum().sum():,}")
        c4.metric("Registros Duplicados", f"{df.duplicated().sum():,}")

        render_download_button(df, "raw", st.session_state.raw_file_name)
        st.dataframe(df.head(20), use_container_width=True)

    with tab_profiling:
        st.markdown("#### Laudo Automatizado do Dataset")
        st.caption("Inspeção detalhada de distribuições estatísticas, tipos inferidos e correlações.")

        @st.cache_data
        def generate_profile(dataframe: pd.DataFrame):
            return ProfileReport(
                dataframe,
                title="Relatório de Diagnóstico de Qualidade",
                minimal=True,
                progress_bar=False,
            ).to_html()

        # Botão de geração sob demanda para não travar a aplicação automaticamente
        if st.checkbox("Gerar Relatório Completo (YData-Profiling)", value=False):
            with st.spinner("Processando diagnóstico estatístico..."):
                report_html = generate_profile(df)
                st.components.v1.html(report_html, height=750, scrolling=True)
        else:
            st.info("💡 Marque a opção acima para executar a análise aprofundada da camada Bronze.")