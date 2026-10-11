import streamlit as st
import pandas as pd
from pygwalker.api.streamlit import StreamlitRenderer

def render_viz():
    st.subheader("📊 5. Visualização Interativa por Camada")
    target_layer = st.radio(
        "Selecione a camada de dados a ser explorada:",
        ["01_raw", "02_silver", "03_gold"],
        horizontal=True,
    )

    layer_map = {
        "01_raw": st.session_state.df_raw,
        "02_silver": st.session_state.df_silver,
        "03_gold": st.session_state.df_gold,
    }

    selected_df = layer_map[target_layer]

    @st.cache_resource
    def get_pyg_renderer(dataset: pd.DataFrame, layer_id: str):
        return StreamlitRenderer(dataset, spec="./gw_config.json")

    st.caption(
        f"Canvas conectado à camada: **{target_layer}** ({selected_df.shape[0]} linhas x {selected_df.shape[1]} colunas)"
    )
    renderer = get_pyg_renderer(selected_df, target_layer)
    renderer.explorer()