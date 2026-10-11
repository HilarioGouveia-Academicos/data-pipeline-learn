from pathlib import Path
import streamlit as st
import pandas as pd

RAW_DIR = Path("data/01_raw")
SILVER_DIR = Path("data/02_silver")
GOLD_DIR = Path("data/03_gold")

for folder in [RAW_DIR, SILVER_DIR, GOLD_DIR]:
    folder.mkdir(parents=True, exist_ok=True)


def inject_custom_css():
    """Força o bloco de upload a ficar no topo da sidebar acima do st.navigation

    e ajusta a estética do layout.
    """
    st.markdown("""
    <style>
        /* 1. Reordenação Flexbox na Sidebar */
        [data-testid="stSidebar"] > div:first-child {
            display: flex;
            flex-direction: column;
        }

        /* O container customizado do topo (order: -1 faz subir acima do menu) */
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > [data-testid="element-container"]:has(#top-uploader-anchor),
        [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:has(#top-uploader-anchor) {
            order: -1;
            margin-bottom: 1rem;
        }

        /* 2. Compactação estética do File Uploader */
        [data-testid="stSidebar"] [data-testid="stFileUploader"] {
            padding: 0.1rem 0;
        }
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section {
            padding: 0.6rem 0.4rem;
            border-radius: 8px;
            border: 1px dashed rgba(255, 255, 255, 0.25);
            background-color: rgba(255, 255, 255, 0.02);
        }
        [data-testid="stSidebar"] [data-testid="stFileUploader"] section:hover {
            border-color: #4CAF50;
        }

        /* 3. Badge discreto do dataset ativo */
        .dataset-badge {
            padding: 6px 12px;
            background-color: rgba(76, 175, 80, 0.12);
            border: 1px solid rgba(76, 175, 80, 0.35);
            border-radius: 6px;
            font-size: 0.82rem;
            color: #81C784;
            margin-bottom: 0.6rem;
            display: flex;
            align-items: center;
            gap: 6px;
            word-break: break-all;
        }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar_uploader():
    """Gerencia o upload no topo da barra lateral e persiste o arquivo raw."""
    # Âncora invisível que o seletor CSS usa para puxar este bloco para o topo (-1)
    st.markdown('<div id="top-uploader-anchor"></div>', unsafe_allow_html=True)
    
    st.markdown("### 📥 Entrada de Dados")

    if "raw_file_name" in st.session_state:
        st.markdown(
            f'<div class="dataset-badge">📄 <b>Ativo:</b> {st.session_state.raw_file_name}</div>',
            unsafe_allow_html=True
        )
        expander_title = "Trocar arquivo CSV"
        is_expanded = False
    else:
        expander_title = "Carregar arquivo CSV"
        is_expanded = True

    with st.expander(expander_title, expanded=is_expanded):
        uploaded_file = st.file_uploader(
            "Selecione um arquivo",
            type=["csv"],
            label_visibility="collapsed",
            help="Arraste ou selecione um dataset tabular em formato CSV."
        )

        if uploaded_file is not None:
            if (
                "raw_file_name" not in st.session_state
                or st.session_state.raw_file_name != uploaded_file.name
            ):
                df_uploaded = pd.read_csv(uploaded_file)
                st.session_state.raw_file_name = uploaded_file.name
                st.session_state.df_raw = df_uploaded.copy()
                st.session_state.df_silver = df_uploaded.copy()
                st.session_state.df_gold = df_uploaded.copy()

                raw_path = RAW_DIR / uploaded_file.name
                df_uploaded.to_csv(raw_path, index=False)
                st.toast(f"Carregado: {uploaded_file.name}", icon="✅")
                st.rerun()

    if "df_raw" not in st.session_state:
        st.warning("Envie um arquivo CSV acima para liberar o pipeline.")
        st.stop()

    st.markdown("---")


def render_download_button(df: pd.DataFrame, layer_name: str, filename: str):
    """Cria um botão de download para o estado atual da camada informada."""
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"⬇️ Baixar Dataset ({layer_name})",
        data=csv_bytes,
        file_name=f"{layer_name.lower()}_{filename}",
        mime="text/csv",
        use_container_width=True,
    )