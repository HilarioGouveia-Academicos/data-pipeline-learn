# 📐 Especificação de Design do Sistema (SDD) – Data Pipeline Didático

## 1. Visão Geral e Arquitetura de Dados (Medallion Simplificada)

O sistema adota uma adaptação pedagógica da **Arquitetura Medallion**, projetada para que os alunos compreendam visual e fisicamente a progressão e linhagem dos dados (*Data Lineage*):

                 [Upload CSV / Sidebar]
                           │
                           ▼
```
┌─────────────────────────────────────────────────────────┐
│  Camada 01_raw (Bronze)                                 │
│  - Arquivo original imutável (.csv)                     │
│  - Diagnóstico estatístico e auditoria (YData-Profiling)│
└────────────────────────────┬────────────────────────────┘
│
│ Imputação de nulos & Deduplicação
▼
┌─────────────────────────────────────────────────────────┐
│  Camada 02_silver (Prata)                               │
│  - Dados qualificados e higienizados (.csv)             │
│  - Auditoria volumétrica e Schema Diff                  │
└────────────────────────────┬────────────────────────────┘
│
│ Discretização (Bins) & One-Hot Encoding
▼
┌─────────────────────────────────────────────────────────┐
│  Camada 03_gold (Ouro)                                  │
│  - Tabela analítica com features enriquecidas (.csv)    │
│  - Pronta para consumo analítico e modelagem de ML      │
└────────────────────────────┬────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│  Consumo / Visualização Analítica                       │
│  - Canvas multidimensional interativo (PyGWalker)       │
└─────────────────────────────────────────────────────────┘
```

* **`data/01_raw/`**: Armazena o ficheiro original intacto assim que o upload é realizado.
* **`data/02_silver/`**: Armazena o estado do dataset após o tratamento de valores faltantes (mediana/moda) e deduplicação de registros.
* **`data/03_gold/`**: Armazena a tabela enriquecida com faixas numéricas discretizadas e variáveis *dummy* (*One-Hot Encoding*).

---

## 2. Estrutura Modular do Repositório (`src/`)

Para garantir manutenibilidade, separação de responsabilidades e validade de nomenclatura em Python (evitando o erro `SyntaxError: invalid decimal literal`), a estrutura do projeto é organizada da seguinte forma:

```text
data-pipeline-learn/
├── data/
│   ├── 01_raw/                 # Camada Bronze: dados originais imutáveis
│   ├── 02_silver/              # Camada Silver: dados limpos e deduplicados
│   └── 03_gold/                # Camada Gold: tabela analítica com features
├── docs/
│   ├── manual-ydataprofiling.md # Guia prático de interpretação de EDA
│   ├── manual-pygwalker.md      # Manual de visualização multidimensional
│   └── images/                 # Prévias e diagramas arquiteturais
├── src/
│   ├── __init__.py
│   ├── pipeline_ops.py         # Lógica pura: transformações, imputação e schema diff
│   ├── ui_components.py        # Componentes visuais: upload fixo, CSS e botões de download
│   └── pages/
│       ├── __init__.py
│       ├── p01_ingestion.py    # Etapa 1: Ingestão & Profiling (Bronze)
│       ├── p02_cleaning.py     # Etapa 2: Limpeza e Tratamento (Silver)
│       ├── p03_wrangling.py    # Etapa 3: Engenharia de Features (Gold)
│       └── p04_viz.py          # Etapa 4: Visualização Analítica (PyGWalker)
├── app.py                      # Ponto de entrada (entrypoint) e orquestração do menu
├── requirements.txt            # Dependências fixadas
└── README.md                   # Documentação do projeto
```

---

## 3. Especificação dos Módulos do Sistema

### 3.1. Núcleo Lógico (`src/pipeline_ops.py`)

Módulo sem dependência de UI, contendo funções puras e auditáveis via `logging`:

* `impute_missing_values(df, col_num, col_cat)`: Trata valores faltantes com mediana para colunas numéricas e moda para colunas categóricas, retornando o DataFrame tratado e estatísticas de imputação.
* `apply_feature_engineering(df, col_disc, bins, col_encode)`: Aplica discretização por quantis/intervalos (`pd.cut`) e codificação dummy (`pd.get_dummies`), rastreando as novas features criadas.
* `compare_schemas(df_before, df_after)`: Gera um relatório diferencial de schema (*Schema Diff*), catalogando colunas como *Inalterada*, *Tipo Modificado*, *Removida* ou *Nova Feature*.

### 3.2. Camada de UI e Ingestão (`src/ui_components.py`)

* `inject_custom_css()`: Estilização do componente de upload e crachá do arquivo ativo.
* `render_sidebar_uploader()`: Controla o upload no topo da barra lateral, grava o arquivo na pasta `data/01_raw/` e inicializa o `st.session_state`.
* `render_download_button(df, layer_name, filename)`: Fornece botão de exportação direta em CSV para qualquer camada em análise.

### 3.3. Orquestrador (`app.py`)

* Inicializa as configurações de página e os diretórios Medallion.
* Controla a ordem rígida de renderização na barra lateral:

1. **Topo:** `render_sidebar_uploader()`
2. **Centro:** `st.page_link` sequencial
3. **Rodapé:** Assinatura do autor e links sociais.

* Executa a navegação controlada via `st.navigation(pages, position="hidden")`.

---

## 4. Telas e Fluxo Didático da Aplicação

### 📦 1. Ingestão & Profiling (Camada Bronze)

* **Aba 1 (Visão Geral & Dados):** Exibe métricas de cabeçalho (linhas, colunas, nulos e duplicatas), tabela interativa e botão de download da camada bruta.
* **Aba 2 (Diagnóstico de Qualidade):** Execução sob demanda com `st.checkbox` do **YData-Profiling** com `@st.cache_data`, apresentando o "laudo médico" dos dados (matriz de correlação, cardinalidade e alertas).

### 🧹 2. Limpeza & Tratamento (Camada Silver)

* Interface para seleção de estratégias de preenchimento de nulos e remoção de duplicatas.
* Botão de promoção de dados que grava o arquivo físico em `data/02_silver/`.
* **Painel de Auditoria Volumétrica:** Comparativo de linhas finais com cálculo de variação percentual ($\Delta\%$) e contagem de nulos eliminados.
* **Schema Diff:** Tabela comparativa de tipos de dados (*Raw vs. Silver*).

### 🔧 3. Engenharia de Features (Camada Gold)

* Configuração interativa de discretização contínua (*Bins*) e *One-Hot Encoding*.
* Promoção de dados gravando o artefato final em `data/03_gold/`.
* Auditoria de atributos gerados ($\Delta\text{ features}$) e mapeamento das novas colunas categóricas e dummies.

### 📊 4. Visualização Multidimensional (Viz)

* Seletor de camada (`01_raw`, `02_silver`, `03_gold`) permitindo aos alunos comparar visualmente a base antes e depois do tratamento.
* Canvas interativo **PyGWalker** armazenado em `@st.cache_resource` para criação ágil de gráficos de dispersão, barras, histogramas e cruzamento de variáveis.

---

## 5. Boas Práticas e Padrões Implementados

* **Logs Padronizados:** Substituição de comandos `print` pelo módulo padrão `logging`, registrando no console cada evento de ingestão, imputação e encoding.
* **Gerenciamento de Estado Persistente:** Uso de `st.session_state` (`df_raw`, `df_silver`, `df_gold`) garantindo que as transformações não se percam na alternância de páginas.
* **Prevenção de Gargalos de CPU/Memória:** Cacheamento estratégico de tarefas custosas (`@st.cache_data` para relatórios estatísticos e `@st.cache_resource` para instâncias do renderizador visual).
