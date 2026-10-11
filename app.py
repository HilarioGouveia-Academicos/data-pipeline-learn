import streamlit as st
from src.ui_components import inject_custom_css, render_sidebar_uploader
from src.pages.p01_ingestion import render_dataset
from src.pages.p02_cleaning import render_cleaning
from src.pages.p03_wrangling import render_wrangling
from src.pages.p04_viz import render_viz

st.set_page_config(
    page_title="Data Pipeline Didático",
    page_icon="🔬",
    layout="wide",
)

inject_custom_css()

# 1. Definição das páginas
p_ingestion = st.Page(render_dataset, title="1. Ingestão (Bronze)", icon="📦", url_path="ingestion", default=True)
p_cleaning = st.Page(render_cleaning, title="3. Limpeza (Silver)", icon="🧹", url_path="cleaning")
p_wrangling = st.Page(render_wrangling, title="4. Features (Gold)", icon="🔧", url_path="wrangling")
p_viz = st.Page(render_viz, title="5. Visualização (Viz)", icon="📊", url_path="viz")

pages = [p_ingestion, p_cleaning, p_wrangling, p_viz]

# 2. Configura a navegação com position="hidden" para não injetar automaticamente no topo
pg = st.navigation(pages, position="hidden")

# 3. Montagem manual e sequencial da barra lateral (Upload SEMPRE no topo)
with st.sidebar:
    # O upload é executado em primeiro lugar:
    render_sidebar_uploader()

    # Em seguida, desenham-se os links de navegação:
    st.markdown("### 🧭 Ciclo de Dados")
    for p in pages:
        st.page_link(p, label=p.title, icon=p.icon)

# [RODAPÉ] Assinatura do desenvolvedor
    st.markdown("---")
    st.caption("Desenvolvido por **Hilário Gouveia**")
    st.markdown(
        "[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/hilário-gouveia-30a09b26b) "
        "[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/HilarioGouveia)"
    )

# 4. Executa a página ativa
pg.run()